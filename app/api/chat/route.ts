import { NextRequest, NextResponse } from "next/server";
import { GoogleGenerativeAI } from "@google/generative-ai";
import { getMerchantById } from "@/lib/merchants";

const LEGAL_HEALTH_DISCLAIMER_ES =
  "\n\n⚠️ DESCARGO DE RESPONSABILIDAD LEGAL Y DE SALUD: La información proporcionada por este asistente virtual es únicamente para fines informativos generales y NO constituye asesoramiento médico, nutricional ni profesional. Si usted padece de alergias alimentarias, condiciones de salud o dudas sobre medicamentos, DEBE VERIFICAR SIEMPRE directamente con el personal humano de la tienda antes de consumir o comprar.";

const LEGAL_HEALTH_DISCLAIMER_EN =
  "\n\n⚠️ LEGAL & HEALTH DISCLAIMER: Information provided by this virtual assistant is for general informational purposes only and does NOT constitute medical, nutritional, or professional advice. If you have food allergies, health conditions, or medication questions, ALWAYS verify directly with in-store human staff before consuming or purchasing.";

export async function POST(req: NextRequest) {
  try {
    const { messages, lang, merchantId } = await req.json();

    if (!messages || !Array.isArray(messages)) {
      return NextResponse.json({ error: "Invalid payload" }, { status: 400 });
    }

    const merchant = getMerchantById(merchantId || "elsol");
    const lastMessage = messages[messages.length - 1]?.content || "";
    const lowerMsg = lastMessage.toLowerCase();

    // Comprehensive check for health, food, ingredients, allergens, medical queries
    const isSensitiveHealthOrFoodQuery =
      lowerMsg.includes("ingrediente") ||
      lowerMsg.includes("ingredient") ||
      lowerMsg.includes("alergia") ||
      lowerMsg.includes("allergy") ||
      lowerMsg.includes("gluten") ||
      lowerMsg.includes("mani") ||
      lowerMsg.includes("peanut") ||
      lowerMsg.includes("lacteo") ||
      lowerMsg.includes("dairy") ||
      lowerMsg.includes("huevo") ||
      lowerMsg.includes("egg") ||
      lowerMsg.includes("cerdo") ||
      lowerMsg.includes("pork") ||
      lowerMsg.includes("salud") ||
      lowerMsg.includes("health") ||
      lowerMsg.includes("medicina") ||
      lowerMsg.includes("medicine") ||
      lowerMsg.includes("receta") ||
      lowerMsg.includes("prescription") ||
      lowerMsg.includes("dosis") ||
      lowerMsg.includes("dosage") ||
      lowerMsg.includes("empanada") ||
      lowerMsg.includes("paisa") ||
      lowerMsg.includes("pan") ||
      lowerMsg.includes("comida") ||
      lowerMsg.includes("food");

    const apiKey = process.env.GEMINI_API_KEY;

    if (apiKey) {
      try {
        const genAI = new GoogleGenerativeAI(apiKey);
        const model = genAI.getGenerativeModel({
          model: "gemini-2.5-flash",
          systemInstruction: `You are an informational virtual assistant for "${merchant.storeInfo.name}" in ${merchant.storeInfo.address}.
Language: ${lang === "en" ? "English" : "Spanish"}.
Ground ALL answers in the Store Metadata & Catalog JSON below.

Store JSON:
${JSON.stringify(merchant, null, 2)}

STRICT LEGAL & LIABILITY PROTECTION INSTRUCTIONS:
1. You are strictly an informational assistant. NEVER provide medical advice, drug dosage advice, or official health guarantees.
2. If asked about medical symptoms or prescription dosages, state clearly that you cannot provide medical advice and direct the user to consult a licensed pharmacist or physician.
3. State that prices, ingredients, and availability are subject to change in-store without notice.
4. MANDATORY LEGAL RULE: Whenever answering ANY question involving food, ingredients, allergens, dietary restrictions, or health/medical items, YOU MUST ALWAYS INCLUDE THIS EXACT LEGAL DISCLAIMER AT THE VERY END OF YOUR RESPONSE:
${lang === "en" ? LEGAL_HEALTH_DISCLAIMER_EN : LEGAL_HEALTH_DISCLAIMER_ES}`,
        });

        const result = await model.generateContent(lastMessage);
        let text = result.response.text().trim();

        // Enforce fallback legal disclaimer check if AI omitted it on a sensitive query
        if (isSensitiveHealthOrFoodQuery) {
          const disclaimer = lang === "en" ? LEGAL_HEALTH_DISCLAIMER_EN : LEGAL_HEALTH_DISCLAIMER_ES;
          if (!text.includes("DESCARGO DE RESPONSABILIDAD") && !text.includes("LEGAL & HEALTH DISCLAIMER")) {
            text += disclaimer;
          }
        }

        return NextResponse.json({ reply: text });
      } catch (err: any) {
        console.warn("Gemini API call failed, using intelligent fallback:", err?.message);
      }
    }

    // Context-grounded intelligent fallback per merchant query type
    let reply = "";
    const p = merchant.storeInfo.policies;

    if (lowerMsg.includes("baño") || lowerMsg.includes("restroom") || lowerMsg.includes("bathroom")) {
      reply = p?.restroomLocation
        ? `Ubicación del baño: ${p.restroomLocation} ${p.restroomCode ? `(${p.restroomCode})` : ""}`
        : `El baño de clientes está disponible al fondo del pasillo central.`;
    } else if (lowerMsg.includes("wifi") || lowerMsg.includes("internet")) {
      reply = p?.wifiName
        ? `WiFi para clientes: Red "${p.wifiName}" | Contraseña: "${p.wifiPassword}"`
        : `Ofrecemos WiFi gratuito en tienda para todos nuestros clientes.`;
    } else if (lowerMsg.includes("ebt") || lowerMsg.includes("snap")) {
      reply = p?.ebtPolicy || `Aceptamos EBT para abarrotes y panadería. Comida caliente del deli requiere efectivo o tarjeta.`;
    } else if (isSensitiveHealthOrFoodQuery) {
      reply = `En ${merchant.storeInfo.name} la información sobre productos e ingredientes es puramente informativa. Por favor consulte el catálogo o hable directamente con el personal.${lang === "en" ? LEGAL_HEALTH_DISCLAIMER_EN : LEGAL_HEALTH_DISCLAIMER_ES}`;
    } else {
      reply = `¡Hola! Bienvenido a ${merchant.storeInfo.name}. Asistente informativo virtual sobre horarios, productos y políticas. ¿En qué le puedo colaborar?`;
    }

    return NextResponse.json({ reply });
  } catch (error: any) {
    console.error("Error in /api/chat route:", error);
    return NextResponse.json({ error: "Error processing request" }, { status: 500 });
  }
}
