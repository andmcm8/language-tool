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

    const merchant = getMerchantById(merchantId || "demo");
    const rawLast = messages[messages.length - 1];
    const lastMessage = (rawLast?.text || rawLast?.content || "").trim();
    const lowerMsg = lastMessage.toLowerCase();

    // Language Detection: Check if user typed/spoke in English
    const isEnglish =
      lang === "en" ||
      /\b(what|where|when|how|is|are|the|do|you|have|restroom|bathroom|wifi|hours|open|closed|price|menu|beef|chicken|food|bread|ebt|snap|address|phone|who|can|i|get|buy|store|parking|park|return|deliver|delivery|fresh|made|baked|items|list|top|cost|allergies|warranty|pay|payment|card|apple|credit|call|number|hello|hi|hey)\b/i.test(
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
      lowerMsg.includes("pork");

    const apiKey = process.env.GEMINI_API_KEY;

    // DIRECT GEMINI AI ENGINE WITH MULTI-TURN CHAT HISTORY
    if (apiKey) {
      try {
        const catalogSummary = merchant.categories
          ?.map(
            (c: any) =>
              `${c.nameEs} / ${c.nameEn}: ${c.items
                .map((i: any) => `${i.nameEs} ($${i.price})`)
                .join(", ")}`
          )
          .join("\n");

        const systemInstruction = `You are the official, intelligent bilingual AI Assistant for "${merchant.storeInfo.name}".

Store Knowledge Base:
- Store Name: ${merchant.storeInfo.name}
- Slogan: ${merchant.storeInfo.tagline}
- Address: ${merchant.storeInfo.address}
- Phone: ${merchant.storeInfo.phone}
- Hours: Mon-Fri: ${merchant.storeInfo.hours.monday_friday}, Sat: ${merchant.storeInfo.hours.saturday}, Sun: ${merchant.storeInfo.hours.sunday}
- Payment Methods Accepted: ${merchant.storeInfo.paymentMethods.join(", ")}
- EBT / SNAP Policy: ${merchant.storeInfo.policies?.ebtPolicyEn || "Accepted for groceries & bakery. Cash/card required for hot prepared food."}
- Restroom Access: ${merchant.storeInfo.policies?.restroomLocationEn || "Back center aisle."} ${merchant.storeInfo.policies?.restroomCodeEn ? `(Code: ${merchant.storeInfo.policies.restroomCodeEn})` : ""}
- Guest WiFi: ${merchant.storeInfo.policies?.wifiName || "ElSol_Guest_WiFi"} (Password: ${merchant.storeInfo.policies?.wifiPassword || "elsolstamford"})
- Parking: ${merchant.storeInfo.policies?.parkingPolicyEn || "Free customer parking in rear lot"}
- Return Policy: ${merchant.storeInfo.policies?.returnPolicyEn || "7-day receipt return for sealed grocery items."}

Store Catalog & Menu Summary:
${catalogSummary || "Groceries, Deli, Bakery, Fresh Produce, Beverages"}

Behavior Guidelines:
- Primary Role: Answer customer questions accurately about store details, hours, address, phone, payment methods, EBT rules, restroom access, WiFi, and catalog products/prices.
- Open Conversational Intelligence: You are a smart, helpful AI. If the user asks general questions, greetings, recipe advice, product recommendations, or anything outside specific store data, respond naturally, warmly, and intelligently. Never refuse to answer or choke just because a question is general chat.
- Language Matching: Reply in whichever language (English or Spanish) the user speaks to you. If they talk in English, reply in English. If they talk in Spanish, reply in Spanish.
- Tone: Warm, helpful, natural, and concise (2 to 4 sentences).`;

        const genAI = new GoogleGenerativeAI(apiKey);
        const model = genAI.getGenerativeModel({
          model: "gemini-2.0-flash",
          systemInstruction,
        });

        // Convert previous conversation messages into Gemini Multi-Turn History
        const history: { role: string; parts: { text: string }[] }[] = [];
        if (messages.length > 1) {
          const previousMessages = messages.slice(0, -1);
          for (const m of previousMessages) {
            const role = m.sender === "user" || m.role === "user" ? "user" : "model";
            const text = (m.text || m.content || "").trim();
            if (text) {
              history.push({ role, parts: [{ text }] });
            }
          }
        }

        const chat = model.startChat({ history });
        const result = await chat.sendMessage(lastMessage);
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

    // High-Performance Bilingual Local Engine (Fallback)
    let reply = "";
    const info = merchant.storeInfo;
    const p = info.policies;

    // 0. Greetings ("hello", "hi", "hola")
    if (
      lowerMsg.includes("hello") ||
      lowerMsg.includes("hola") ||
      lowerMsg.includes("hi") ||
      lowerMsg.includes("hey") ||
      lowerMsg.includes("buenas")
    ) {
      reply = isEnglish
        ? `Hello! Welcome to ${info.name}. How can I help you today? You can ask me about our store hours, location, catalog items, or payment methods!`
        : `¡Hola! Bienvenido a ${info.name}. ¿En qué puedo ayudarle hoy? ¡Puede preguntarme sobre nuestros horarios, ubicación, productos o métodos de pago!`;
    }
    // 1. Restroom / Bathroom Query
    else if (lowerMsg.includes("baño") || lowerMsg.includes("restroom") || lowerMsg.includes("bathroom")) {
      reply = isEnglish
        ? `Restroom: ${p?.restroomLocationEn || "Located at the back of the store."} ${p?.restroomCodeEn ? `(${p.restroomCodeEn})` : ""}`
        : `Baño: ${p?.restroomLocationEs || "Al fondo de la tienda."} ${p?.restroomCodeEs ? `(${p.restroomCodeEs})` : ""}`;
    }
    // 2. WiFi Query
    else if (lowerMsg.includes("wifi") || lowerMsg.includes("internet")) {
      reply = isEnglish
        ? `Guest WiFi: Network "${p?.wifiName || "Guest_WiFi"}" | Password: "${p?.wifiPassword || "free"}"`
        : `WiFi Clientes: Red "${p?.wifiName || "Guest_WiFi"}" | Contraseña: "${p?.wifiPassword || "free"}"`;
    }
    // 3. Payment Methods / Apple Pay Query
    else if (
      lowerMsg.includes("apple pay") ||
      lowerMsg.includes("google pay") ||
      lowerMsg.includes("credit") ||
      lowerMsg.includes("card") ||
      lowerMsg.includes("tarjeta") ||
      lowerMsg.includes("zelle") ||
      lowerMsg.includes("metodos de pago") ||
      lowerMsg.includes("payment")
    ) {
      reply = isEnglish
        ? `Accepted Payments: ${info.paymentMethods.join(", ")}.`
        : `Métodos de Pago Aceptados: ${info.paymentMethods.join(", ")}.`;
    }
    // 4. Phone Number / Contact Query
    else if (
      lowerMsg.includes("phone number") ||
      lowerMsg.includes("telefono") ||
      lowerMsg.includes("llamar") ||
      lowerMsg.includes("call store") ||
      lowerMsg.includes("call in") ||
      lowerMsg.includes("contact number")
    ) {
      reply = isEnglish
        ? `Phone Number: ${info.phone}.`
        : `Número de Teléfono: ${info.phone}.`;
    }
    // 5. EBT / SNAP Query
    else if (lowerMsg.includes("ebt") || lowerMsg.includes("snap")) {
      reply = isEnglish
        ? (p?.ebtPolicyEn || "EBT/SNAP is accepted for groceries and bakery items.")
        : (p?.ebtPolicyEs || "Aceptamos EBT/SNAP para abarrotes y panadería.");
    }
    // 6. Hours Query
    else if (
      lowerMsg.includes("hours") ||
      lowerMsg.includes("open") ||
      lowerMsg.includes("close") ||
      lowerMsg.includes("schedule") ||
      lowerMsg.includes("horario") ||
      lowerMsg.includes("abierto") ||
      lowerMsg.includes("cierran")
    ) {
      const hoursStr = `Mon-Fri: ${info.hours?.monday_friday || "8am-9pm"}, Sat: ${info.hours?.saturday || "8am-9pm"}, Sun: ${info.hours?.sunday || "9am-8pm"}`;
      reply = isEnglish
        ? `Store Hours: ${hoursStr}.`
        : `Horario de Atención: ${hoursStr}.`;
    }
    // 7. Address / Location Query
    else if (
      lowerMsg.includes("where") ||
      lowerMsg.includes("address") ||
      lowerMsg.includes("location") ||
      lowerMsg.includes("direccion") ||
      lowerMsg.includes("donde") ||
      lowerMsg.includes("ubicacion")
    ) {
      reply = isEnglish
        ? `We are located at ${info.address}.`
        : `Estamos ubicados en ${info.address}.`;
    }
    // Default fallback
    else {
      reply = isEnglish
        ? `Welcome to ${info.name}! How can I help you today? Ask about our hours, location, catalog items, or store services!`
        : `¡Bienvenido a ${info.name}! ¿En qué puedo ayudarle hoy? ¡Pregunte sobre nuestros horarios, ubicación, productos o servicios!`;
    }

    if (isSensitiveQuery) {
      const disclaimer = isEnglish ? DISCLAIMER_EN : DISCLAIMER_ES;
      if (!reply.includes("alergias") && !reply.includes("allergies")) {
        reply += disclaimer;
      }
    }

    return NextResponse.json({ reply });
  } catch (error: any) {
    console.error("Chat error:", error?.message);
    return NextResponse.json({
      reply: "Lo sentimos, ocurrió un error. / Sorry, an error occurred.",
    });
  }
}
