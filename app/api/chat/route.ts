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
      /\b(what|where|when|how|is|are|the|do|you|have|restroom|bathroom|wifi|hours|open|closed|price|menu|beef|chicken|food|bread|ebt|snap|address|phone|who|can|i|get|buy|store|parking|park|return|deliver|delivery|fresh|made|baked|items|list|top|cost|allergies|warranty|pay|payment|card|apple|credit|call|number|hello|hi|hey|cheapest|cheap|item|product|sell)\b/i.test(
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

    // DIRECT GEMINI AI ENGINE (When Gemini API is available)
    if (apiKey) {
      const catalogSummary = merchant.products
        ?.map((p: any) => `${p.nameEs} / ${p.nameEn}: $${p.price}`)
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

      const candidateModels = ["gemini-flash-latest", "gemini-2.5-flash", "gemini-2.5-flash-lite"];
      const genAI = new GoogleGenerativeAI(apiKey);

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

      while (history.length > 0 && history[0].role === "model") {
        history.shift();
      }

      for (const modelName of candidateModels) {
        try {
          const model = genAI.getGenerativeModel({
            model: modelName,
            systemInstruction,
          });

          let text = "";
          if (history.length > 0) {
            const chat = model.startChat({ history });
            const result = await chat.sendMessage(lastMessage);
            text = result.response.text().trim();
          } else {
            const result = await model.generateContent(lastMessage);
            text = result.response.text().trim();
          }

          if (text) {
            if (isSensitiveQuery) {
              const disclaimer = isEnglish ? DISCLAIMER_EN : DISCLAIMER_ES;
              if (!text.includes("alergias") && !text.includes("allergies")) {
                text += disclaimer;
              }
            }
            return NextResponse.json({ reply: text });
          }
        } catch (err: any) {
          console.warn(`Gemini model ${modelName} call failed:`, err?.message);
        }
      }
    }

    // HIGH-ACCURACY DYNAMIC STORE AI KNOWLEDGE ENGINE
    let reply = "";
    const info = merchant.storeInfo;
    const p = info.policies;

    // Collect all items across categories for smart catalog search
    const allItems: { nameEs: string; nameEn: string; priceNum: number; priceStr: string }[] = [];
    if (merchant.products) {
      for (const item of merchant.products) {
        const priceNum = parseFloat(String(item.price).replace(/[^0-9.]/g, "")) || 0;
        allItems.push({
          nameEs: item.nameEs,
          nameEn: item.nameEn || item.nameEs,
          priceNum,
          priceStr: String(item.price),
        });
      }
    }

    // Sort items by price for "cheapest" queries
    const sortedItems = [...allItems].sort((a, b) => a.priceNum - b.priceNum);
    const cheapestItem = sortedItems[0];

    // 1. CHEAPEST ITEM / PRICING QUERY
    if (
      lowerMsg.includes("cheapest") ||
      lowerMsg.includes("barato") ||
      lowerMsg.includes("económico") ||
      lowerMsg.includes("lowest price") ||
      lowerMsg.includes("mas barato")
    ) {
      if (cheapestItem) {
        reply = isEnglish
          ? `Our cheapest item in stock is ${cheapestItem.nameEn} for $${cheapestItem.priceStr}. We also have several delicious bakery and grocery options under $5.00!`
          : `Nuestro producto más económico es ${cheapestItem.nameEs} por $${cheapestItem.priceStr}. ¡También tenemos varias opciones por menos de $5.00!`;
      } else {
        reply = isEnglish
          ? `Our bakery and deli items start as low as $1.50 per item!`
          : `¡Nuestros productos de panadería y charcutería comienzan desde $1.50!`;
      }
    }
    // 2. CATALOG / ITEMS / WHAT DO YOU SELL QUERY
    else if (
      lowerMsg.includes("items") ||
      lowerMsg.includes("products") ||
      lowerMsg.includes("catalog") ||
      lowerMsg.includes("menu") ||
      lowerMsg.includes("productos") ||
      lowerMsg.includes("que tienen") ||
      lowerMsg.includes("que venden") ||
      lowerMsg.includes("what do you sell") ||
      lowerMsg.includes("list") ||
      lowerMsg.includes("food") ||
      lowerMsg.includes("comida")
    ) {
      const topItemsStr = allItems
        .slice(0, 5)
        .map((i) => `${isEnglish ? i.nameEn : i.nameEs} ($${i.priceStr})`)
        .join(", ");

      reply = isEnglish
        ? `We carry fresh deli dishes, baked goods, groceries, and beverages! Popular items include: ${topItemsStr}. Ask me about any specific dish or category!`
        : `¡Ofrecemos platos de charcutería fresca, panadería, abarrotes y bebidas! Algunos productos populares son: ${topItemsStr}. ¡Pregúnteme por cualquier producto o categoría!`;
    }
    // 3. RESTROOM / BATHROOM QUERY
    else if (lowerMsg.includes("baño") || lowerMsg.includes("bano") || lowerMsg.includes("restroom") || lowerMsg.includes("bathroom")) {
      reply = isEnglish
        ? `Restroom: ${p?.restroomLocationEn || "Located at the back of the store."} ${p?.restroomCodeEn ? `(${p.restroomCodeEn})` : ""}`
        : `Baño: ${p?.restroomLocationEs || "Al fondo de la tienda."} ${p?.restroomCodeEs ? `(${p.restroomCodeEs})` : ""}`;
    }
    // 4. WIFI QUERY
    else if (lowerMsg.includes("wifi") || lowerMsg.includes("internet")) {
      reply = isEnglish
        ? `Guest WiFi: Network "${p?.wifiName || "Guest_WiFi"}" | Password: "${p?.wifiPassword || "free"}"`
        : `WiFi Clientes: Red "${p?.wifiName || "Guest_WiFi"}" | Contraseña: "${p?.wifiPassword || "free"}"`;
    }
    // 5. PAYMENT METHODS QUERY
    else if (
      lowerMsg.includes("apple pay") ||
      lowerMsg.includes("google pay") ||
      lowerMsg.includes("credit") ||
      lowerMsg.includes("card") ||
      lowerMsg.includes("tarjeta") ||
      lowerMsg.includes("zelle") ||
      lowerMsg.includes("payment") ||
      lowerMsg.includes("pago")
    ) {
      reply = isEnglish
        ? `Accepted Payments: ${info.paymentMethods.join(", ")}.`
        : `Métodos de Pago Aceptados: ${info.paymentMethods.join(", ")}.`;
    }
    // 6. PHONE NUMBER QUERY
    else if (
      lowerMsg.includes("phone") ||
      lowerMsg.includes("telefono") ||
      lowerMsg.includes("llamar") ||
      lowerMsg.includes("call") ||
      lowerMsg.includes("contacto")
    ) {
      reply = isEnglish
        ? `Phone Number: ${info.phone}.`
        : `Número de Teléfono: ${info.phone}.`;
    }
    // 7. EBT / SNAP QUERY
    else if (lowerMsg.includes("ebt") || lowerMsg.includes("snap")) {
      reply = isEnglish
        ? (p?.ebtPolicyEn || "EBT/SNAP is accepted for groceries and bakery items.")
        : (p?.ebtPolicyEs || "Aceptamos EBT/SNAP para abarrotes y panadería.");
    }
    // 8. HOURS QUERY
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
    // 9. ADDRESS / LOCATION QUERY
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
    // 10. GREETINGS ("hello", "hi", "hola", "hey")
    else if (
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
    // 11. GENERAL FALLBACK QUERY (Smart Store Summary Response)
    else {
      const sampleItems = allItems.slice(0, 3).map((i) => (isEnglish ? i.nameEn : i.nameEs)).join(", ");
      reply = isEnglish
        ? `At ${info.name}, we offer fresh groceries, deli specials (${sampleItems}), bakery items, and store services. How can I assist you with your visit today?`
        : `En ${info.name}, ofrecemos abarrotes frescos, especialidades de charcutería (${sampleItems}), panadería y servicios. ¿En qué le puedo asistir hoy?`;
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
