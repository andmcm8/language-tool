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
    const rawLast = messages[messages.length - 1];
    const lastMessage = (rawLast?.text || rawLast?.content || "").trim();
    const lowerMsg = lastMessage.toLowerCase();

    // Detect if user asked in English or Spanish
    const isEnglishQuery =
      lang === "en" ||
      /\b(what|where|when|how|is|are|the|do|you|have|restroom|bathroom|wifi|hours|open|closed|price|menu|beef|chicken|food|bread|ebt|snap|address|phone)\b/i.test(
        lowerMsg
      );

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
          systemInstruction: `You are the bilingual informational virtual assistant for "${merchant.storeInfo.name}" in ${merchant.storeInfo.address}.

CRITICAL LANGUAGE ADAPTABILITY RULE:
Always detect the language of the user's latest query:
- If the user writes or speaks in English, YOU MUST RESPOND IN ENGLISH.
- If the user writes or speaks in Spanish, YOU MUST RESPOND IN SPANISH.
Match the user's language dynamically.

Store Context JSON:
${JSON.stringify(merchant, null, 2)}

STRICT INSTRUCTIONS:
1. Answer customer questions about store hours, address, bathroom location/key, WiFi password, parking, EBT rules, return policy, delivery, and menu items/ingredients accurately based on the store JSON.
2. Keep answers concise and direct (2-3 sentences max).
3. MANDATORY LEGAL RULE: Whenever answering ANY question involving food, ingredients, allergens, dietary restrictions, or health/medical items, YOU MUST ALWAYS INCLUDE THIS EXACT LEGAL DISCLAIMER AT THE VERY END OF YOUR RESPONSE:
${isEnglishQuery ? LEGAL_HEALTH_DISCLAIMER_EN : LEGAL_HEALTH_DISCLAIMER_ES}`,
        });

        const result = await model.generateContent(lastMessage);
        let text = result.response.text().trim();

        // Enforce legal disclaimer if missing on sensitive queries
        if (isSensitiveHealthOrFoodQuery) {
          const disclaimer = isEnglishQuery ? LEGAL_HEALTH_DISCLAIMER_EN : LEGAL_HEALTH_DISCLAIMER_ES;
          if (!text.includes("DESCARGO DE RESPONSABILIDAD") && !text.includes("LEGAL & HEALTH DISCLAIMER")) {
            text += disclaimer;
          }
        }

        return NextResponse.json({ reply: text });
      } catch (err: any) {
        console.warn("Gemini API call failed, using fallback:", err?.message);
      }
    }

    // Dynamic Intelligent Fallbacks (Language Adaptive)
    let reply = "";
    const p = merchant.storeInfo.policies;

    if (lowerMsg.includes("baño") || lowerMsg.includes("restroom") || lowerMsg.includes("bathroom")) {
      reply = isEnglishQuery
        ? `Restroom location: ${p?.restroomLocation || "Located at the back center aisle."} ${p?.restroomCode ? `(${p.restroomCode})` : ""}`
        : `Ubicación del baño: ${p?.restroomLocation || "Al fondo del pasillo central."} ${p?.restroomCode ? `(${p.restroomCode})` : ""}`;
    } else if (lowerMsg.includes("wifi") || lowerMsg.includes("internet")) {
      reply = isEnglishQuery
        ? `Guest WiFi: Network "${p?.wifiName || "Store_WiFi"}" | Password: "${p?.wifiPassword || "free"}"`
        : `WiFi para clientes: Red "${p?.wifiName || "Store_WiFi"}" | Contraseña: "${p?.wifiPassword || "free"}"`;
    } else if (lowerMsg.includes("ebt") || lowerMsg.includes("snap")) {
      reply = p?.ebtPolicy || (isEnglishQuery ? "EBT is accepted for groceries and bakery. Hot food requires cash/card." : "Aceptamos EBT para abarrotes y panadería. Comida caliente del deli requiere efectivo o tarjeta.");
    } else if (isSensitiveHealthOrFoodQuery) {
      reply = isEnglishQuery
        ? `At ${merchant.storeInfo.name}, product and ingredient information is for general guidance. Please consult our catalog or speak directly with store staff.${LEGAL_HEALTH_DISCLAIMER_EN}`
        : `En ${merchant.storeInfo.name} la información sobre productos e ingredientes es puramente informativa. Por favor consulte el catálogo o hable con el personal.${LEGAL_HEALTH_DISCLAIMER_ES}`;
    } else {
      reply = isEnglishQuery
        ? `Hello! Welcome to ${merchant.storeInfo.name}. I am your virtual assistant for store hours, products, WiFi, and policies. How can I help you today?`
        : `¡Hola! Bienvenido a ${merchant.storeInfo.name}. Asistente informativo virtual sobre horarios, productos y políticas. ¿En qué le puedo colaborar hoy?`;
    }

    return NextResponse.json({ reply });
  } catch (error: any) {
    console.error("Error in /api/chat route:", error);
    return NextResponse.json({ error: "Error processing request" }, { status: 500 });
  }
}
