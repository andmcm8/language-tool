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
      /\b(what|where|when|how|is|are|the|do|you|have|restroom|bathroom|wifi|hours|open|closed|price|menu|beef|chicken|food|bread|ebt|snap|address|phone|who|can|i|get|buy|store|parking|park|return|deliver|delivery|fresh|made|baked|items|list|top|cost|allergies|warranty|pay|payment|card|apple|credit|call|number)\b/i.test(
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

    // Direct Gemini AI Engine Call if valid key is set
    if (apiKey && apiKey.startsWith("AIza")) {
      try {
        const genAI = new GoogleGenerativeAI(apiKey);
        const model = genAI.getGenerativeModel({
          model: "gemini-2.0-flash",
          systemInstruction: `You are the bilingual AI Assistant for "${merchant.storeInfo.name}".
Language Rules:
- If user speaks/writes English, reply ONLY in 100% natural, clear English.
- If user speaks/writes Spanish, reply ONLY in 100% natural, clear Spanish.

Brevity Rule:
- Keep answers ultra-short (1 to 2 sentences MAX). No extra yapping.

Unknown Information Rule:
- If asked about something not in the store data or unknown, reply warmly:
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

    // High-Performance Bilingual Local Engine
    let reply = "";
    const info = merchant.storeInfo;
    const p = info.policies;

    // 1. Restroom / Bathroom Query
    if (lowerMsg.includes("baño") || lowerMsg.includes("restroom") || lowerMsg.includes("bathroom")) {
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
    // 6. Hours / Open Query
    else if (lowerMsg.includes("hora") || lowerMsg.includes("hours") || lowerMsg.includes("open") || lowerMsg.includes("abierto")) {
      reply = isEnglish
        ? `Hours: Mon-Fri ${info.hours.monday_friday}, Sat ${info.hours.saturday}, Sun ${info.hours.sunday}.`
        : `Horarios: Lun-Vie ${info.hours.monday_friday}, Sáb ${info.hours.saturday}, Dom ${info.hours.sunday}.`;
    }
    // 7. Address / Location Query
    else if (lowerMsg.includes("direccion") || lowerMsg.includes("address") || lowerMsg.includes("where is the store")) {
      reply = isEnglish
        ? `Address: ${info.address}. Phone: ${info.phone}.`
        : `Dirección: ${info.address}. Teléfono: ${info.phone}.`;
    }
    // 8. Parking Query
    else if (lowerMsg.includes("park") || lowerMsg.includes("parqueo") || lowerMsg.includes("estacionamiento")) {
      reply = isEnglish
        ? (p?.parkingPolicyEn || "Free customer parking is available.")
        : (p?.parkingPolicyEs || "Estacionamiento gratuito disponible para clientes.");
    }
    // 9. Delivery Query
    else if (lowerMsg.includes("deliver") || lowerMsg.includes("delivery") || lowerMsg.includes("envio") || lowerMsg.includes("domicilio")) {
      reply = isEnglish
        ? (p?.deliveryPolicyEn || "Home delivery is available for orders in Stamford.")
        : (p?.deliveryPolicyEs || "Entregas a domicilio disponibles para Stamford.");
    }
    // 10. Warranty / Return Query
    else if (lowerMsg.includes("warranty") || lowerMsg.includes("garantia") || lowerMsg.includes("return") || lowerMsg.includes("refund")) {
      reply = isEnglish
        ? (p?.returnPolicyEn || "All products and services include store warranty.")
        : (p?.returnPolicyEs || "Todos los productos y servicios incluyen garantía.");
    }
    // 11. Menu / Item List Query ("What are three items on the menu?", "What items do you sell?")
    else if (
      lowerMsg.includes("items") ||
      lowerMsg.includes("menu") ||
      lowerMsg.includes("catalog") ||
      lowerMsg.includes("list") ||
      (lowerMsg.includes("sell") && !lowerMsg.includes("ps5") && !lowerMsg.includes("playstation"))
    ) {
      const topProducts = merchant.products.slice(0, 3);
      if (isEnglish) {
        const itemNames = topProducts.map((prod) => `${prod.nameEn} (${prod.price})`).join(", ");
        reply = `Popular menu items include: ${itemNames}.`;
      } else {
        const itemNames = topProducts.map((prod) => `${prod.nameEs} (${prod.price})`).join(", ");
        reply = `Los productos principales incluyen: ${itemNames}.`;
      }
    }
    // 12. Specific Product Query
    else {
      // Find matching product with exact score priority
      const matchedProduct = merchant.products.find((prod) => {
        const nameEn = prod.nameEn.toLowerCase();
        const nameEs = prod.nameEs.toLowerCase();
        return (
          lowerMsg.includes(nameEn) ||
          lowerMsg.includes(nameEs) ||
          (lowerMsg.includes("bono") && nameEn.includes("bono")) ||
          (lowerMsg.includes("empanada") && nameEn.includes("empanada")) ||
          (lowerMsg.includes("paisa") && nameEn.includes("paisa")) ||
          (lowerMsg.includes("bateria") && nameEn.includes("battery")) ||
          (lowerMsg.includes("pantalla") && nameEn.includes("screen")) ||
          (lowerMsg.includes("receta") && nameEn.includes("prescription")) ||
          (lowerMsg.includes("vacuna") && nameEn.includes("vaccine"))
        );
      }) || merchant.products.find((prod) => {
        const nameEn = prod.nameEn.toLowerCase();
        const nameEs = prod.nameEs.toLowerCase();
        return lowerMsg.split(/\s+/).some((w: string) => w.length > 3 && (nameEn.includes(w) || nameEs.includes(w)));
      });

      if (matchedProduct) {
        // Query Intent: Freshness / Preparation / Baking
        if (
          lowerMsg.includes("fresh") ||
          lowerMsg.includes("fresco") ||
          lowerMsg.includes("made") ||
          lowerMsg.includes("bake") ||
          lowerMsg.includes("baked") ||
          lowerMsg.includes("cook") ||
          lowerMsg.includes("hot")
        ) {
          reply = isEnglish
            ? `Yes! Our ${matchedProduct.nameEn} are ${matchedProduct.descriptionEn.toLowerCase()}`
            : `¡Sí! Nuestras ${matchedProduct.nameEs} son ${matchedProduct.descriptionEs.toLowerCase()}`;
        }
        // Query Intent: Ingredients
        else if (lowerMsg.includes("ingredient") || lowerMsg.includes("ingrediente")) {
          reply = isEnglish
            ? `${matchedProduct.nameEn} ingredients: ${matchedProduct.ingredientsEn || matchedProduct.descriptionEn}`
            : `Ingredientes de ${matchedProduct.nameEs}: ${matchedProduct.ingredientsEs || matchedProduct.descriptionEs}`;
        }
        // Query Intent: Price / Cost
        else if (lowerMsg.includes("cost") || lowerMsg.includes("price") || lowerMsg.includes("cuanto") || lowerMsg.includes("cuesta") || lowerMsg.includes("how much")) {
          reply = isEnglish
            ? `${matchedProduct.nameEn} cost ${matchedProduct.price}.`
            : `${matchedProduct.nameEs} cuestan ${matchedProduct.price}.`;
        }
        // General product query
        else {
          reply = isEnglish
            ? `${matchedProduct.nameEn} (${matchedProduct.price}): ${matchedProduct.descriptionEn}`
            : `${matchedProduct.nameEs} (${matchedProduct.price}): ${matchedProduct.descriptionEs}`;
        }
      } else {
        // Unknown question graceful response
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
