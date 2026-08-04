import { NextRequest, NextResponse } from "next/server";
import { GoogleGenerativeAI } from "@google/generative-ai";
import { getMerchantById } from "@/lib/merchants";

const DISCLAIMER_ES =
  "\n\n⚠️ Si tiene alergias o dudas de salud, confirme con el personal antes de consumir.";
const DISCLAIMER_EN =
  "\n\n⚠️ If you have food allergies or health concerns, please verify with store staff before consuming.";

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

    // Language Detection: Check if user typed/spoke in English
    const isEnglish =
      lang === "en" ||
      /\b(what|where|when|how|is|are|the|do|you|have|restroom|bathroom|wifi|hours|open|closed|price|menu|beef|chicken|food|bread|ebt|snap|address|phone|who|can|i|get|sell|buy|store|parking|return|deliver|much)\b/i.test(
        lowerMsg
      );

    const isSensitiveQuery =
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
      lowerMsg.includes("empanada") ||
      lowerMsg.includes("paisa") ||
      lowerMsg.includes("pan") ||
      lowerMsg.includes("comida") ||
      lowerMsg.includes("food");

    const apiKey = process.env.GEMINI_API_KEY;

    // Try Gemini AI if valid AI Studio key starts with AIza
    if (apiKey && apiKey.startsWith("AIza")) {
      try {
        const genAI = new GoogleGenerativeAI(apiKey);
        const model = genAI.getGenerativeModel({
          model: "gemini-2.0-flash",
          systemInstruction: `You are the bilingual AI Assistant for "${merchant.storeInfo.name}".
Language Rules:
- If user speaks/writes English, reply ONLY in concise English.
- If user speaks/writes Spanish, reply ONLY in concise Spanish.

Brevity Rule:
- Keep answers ultra-short (1 to 2 sentences MAX). No extra yapping.

Unknown Information Rule:
- If the question is about something not in the store data or unknown, reply warmly:
  - EN: "For that specific detail, please ask one of our team members at the register!"
  - ES: "Para ese detalle específico, ¡por favor pregunte a uno de nuestros compañeros en la caja!"

Store JSON:
${JSON.stringify(merchant, null, 2)}`,
        });

        const result = await model.generateContent(lastMessage);
        let text = result.response.text().trim();

        if (isSensitiveQuery) {
          const disclaimer = isEnglish ? DISCLAIMER_EN : DISCLAIMER_ES;
          if (!text.includes("alergias") && !text.includes("allergies")) {
            text += disclaimer;
          }
        }

        return NextResponse.json({ reply: text });
      } catch (err: any) {
        console.warn("Gemini API call skipped, using local smart engine:", err?.message);
      }
    }

    // High-performance Local Smart Engine (Language Adaptive, Ultra-Brief, No Yapping)
    let reply = "";
    const info = merchant.storeInfo;
    const p = info.policies;

    if (lowerMsg.includes("baño") || lowerMsg.includes("restroom") || lowerMsg.includes("bathroom")) {
      reply = isEnglish
        ? `Restroom location: ${p?.restroomLocation || "Back of the store."} ${p?.restroomCode ? `(${p.restroomCode})` : ""}`
        : `Ubicación del baño: ${p?.restroomLocation || "Al fondo de la tienda."} ${p?.restroomCode ? `(${p.restroomCode})` : ""}`;
    } else if (lowerMsg.includes("wifi") || lowerMsg.includes("internet")) {
      reply = isEnglish
        ? `WiFi: Network "${p?.wifiName || "Store_WiFi"}" | Password: "${p?.wifiPassword || "free"}"`
        : `WiFi: Red "${p?.wifiName || "Store_WiFi"}" | Contraseña: "${p?.wifiPassword || "free"}"`;
    } else if (lowerMsg.includes("ebt") || lowerMsg.includes("snap")) {
      reply = isEnglish
        ? (p?.ebtPolicy || "EBT accepted for groceries and bakery items.")
        : (p?.ebtPolicy || "Aceptamos EBT para abarrotes y panadería.");
    } else if (lowerMsg.includes("hora") || lowerMsg.includes("hours") || lowerMsg.includes("open") || lowerMsg.includes("abierto")) {
      reply = isEnglish
        ? `Store Hours: Mon-Fri ${info.hours.monday_friday}, Sat ${info.hours.saturday}, Sun ${info.hours.sunday}.`
        : `Horarios: Lun-Vie ${info.hours.monday_friday}, Sáb ${info.hours.saturday}, Dom ${info.hours.sunday}.`;
    } else if (lowerMsg.includes("direccion") || lowerMsg.includes("address") || lowerMsg.includes("where")) {
      reply = isEnglish
        ? `Address: ${info.address}. Phone: ${info.phone}.`
        : `Dirección: ${info.address}. Teléfono: ${info.phone}.`;
    } else if (lowerMsg.includes("estacionamiento") || lowerMsg.includes("parking") || lowerMsg.includes("parqueo")) {
      reply = isEnglish
        ? (p?.parkingPolicy || "Free customer parking is available.")
        : (p?.parkingPolicy || "Estacionamiento gratuito disponible para clientes.");
    } else {
      // Improved product search: match words in product names or tags
      const matchedProduct = merchant.products.find((prod) => {
        const nameEn = prod.nameEn.toLowerCase();
        const nameEs = prod.nameEs.toLowerCase();
        const cat = prod.categoryId.toLowerCase();
        return (
          lowerMsg.includes(nameEn) ||
          lowerMsg.includes(nameEs) ||
          lowerMsg.includes("empanada") ||
          lowerMsg.includes("paisa") ||
          lowerMsg.includes("bread") ||
          lowerMsg.includes("pan") ||
          lowerMsg.includes("cheese") ||
          lowerMsg.includes("beef") ||
          lowerMsg.includes("chicken") ||
          lowerMsg.includes(cat)
        );
      });

      if (matchedProduct) {
        reply = isEnglish
          ? `${matchedProduct.nameEn}: ${matchedProduct.price}.`
          : `${matchedProduct.nameEs}: ${matchedProduct.price}.`;
      } else {
        // Unknown question graceful response (Ask a worker at register)
        reply = isEnglish
          ? `For that specific detail, please ask one of our friendly team members at the register!`
          : `Para ese detalle específico, ¡por favor pregunte a uno de nuestros amables compañeros en la caja!`;
      }
    }

    if (isSensitiveQuery) {
      reply += isEnglish ? DISCLAIMER_EN : DISCLAIMER_ES;
    }

    return NextResponse.json({ reply });
  } catch (error: any) {
    console.error("Error in /api/chat route:", error);
    return NextResponse.json({ error: "Error processing request" }, { status: 500 });
  }
}
