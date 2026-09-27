import { NextRequest, NextResponse } from "next/server";
import { GoogleGenerativeAI } from "@google/generative-ai";
import { getMerchantById } from "@/lib/merchants";
import { MerchantConfig } from "@/types/merchant";

const DISCLAIMER_ES =
  "\n\n⚠️ Si tiene alergias o dudas de salud, confirme con el personal antes de consumir.";
const DISCLAIMER_EN =
  "\n\n⚠️ If you have food allergies or health concerns, please verify with store staff before consuming.";

/* ================================================================
   BUILD STRUCTURED STORE & MENU KNOWLEDGE PROMPT FOR GEMINI
   ================================================================ */
function buildStoreKnowledgePrompt(merchant: MerchantConfig): string {
  const { storeInfo, categories = [], products = [], faqs = [] } = merchant;
  const p = storeInfo.policies || {};

  // Build categorized menu items
  const menuLines: string[] = [];
  categories.forEach((cat) => {
    const catProducts = products.filter((prod) => prod.categoryId === cat.id);
    if (catProducts.length > 0) {
      menuLines.push(`\n[CATEGORY: ${cat.nameEn || cat.nameEs} / ${cat.nameEs}]`);
      catProducts.forEach((prod) => {
        let line = `• ${prod.nameEn || prod.nameEs} / ${prod.nameEs} — Price: ${prod.price}`;
        if (prod.descriptionEn || prod.descriptionEs) {
          line += `\n  Description: ${prod.descriptionEn || prod.descriptionEs}`;
          if (prod.descriptionEs && prod.descriptionEs !== prod.descriptionEn) {
            line += ` | ${prod.descriptionEs}`;
          }
        }
        if (prod.tags && prod.tags.length > 0) {
          line += `\n  Dietary / Tags: ${prod.tags.join(", ")}`;
        }
        if (prod.allergens && prod.allergens.length > 0) {
          line += `\n  Allergens: ${prod.allergens.join(", ")}`;
        }
        if (prod.popular || prod.badge) {
          line += ` (Featured / ${prod.badge || "Popular"})`;
        }
        menuLines.push(line);
      });
    }
  });

  // Handle uncategorized products if any
  const categorizedIds = new Set(categories.map((c) => c.id));
  const uncategorized = products.filter((prod) => !categorizedIds.has(prod.categoryId));
  if (uncategorized.length > 0) {
    menuLines.push(`\n[OTHER MENU ITEMS]`);
    uncategorized.forEach((prod) => {
      let line = `• ${prod.nameEn || prod.nameEs} / ${prod.nameEs} — Price: ${prod.price}`;
      if (prod.descriptionEn) line += ` - ${prod.descriptionEn}`;
      if (prod.tags && prod.tags.length > 0) line += ` [${prod.tags.join(", ")}]`;
      menuLines.push(line);
    });
  }

  // FAQs
  const faqLines: string[] = [];
  if (faqs && faqs.length > 0) {
    faqs.forEach((faq) => {
      faqLines.push(`Q: ${faq.qEn} / ${faq.qEs}`);
      faqLines.push(`A: ${faq.aEn} / ${faq.aEs}`);
    });
  }

  const hoursStr = `Monday – Friday: ${storeInfo.hours?.monday_friday || "Open"}\nSaturday: ${storeInfo.hours?.saturday || "Open"}\nSunday: ${storeInfo.hours?.sunday || "Open"}`;

  return `You are the official, intelligent bilingual AI Concierge & Assistant for "${storeInfo.name}".
Your role is to assist guests and answer questions using EXCLUSIVELY the verified knowledge base and official menu of ${storeInfo.name} provided below.

=== 1. VERIFIED BUSINESS DETAILS ===
- Business Name: ${storeInfo.name}
- Concept / Tagline: ${storeInfo.tagline || "Local dining & marketplace"}
- Location & Address: ${storeInfo.address}
- Phone Number: ${storeInfo.phone ? storeInfo.phone : "No public phone listed; guests can visit us at our address or inquire with staff."}
- Operating Hours:
${hoursStr}
- Accepted Payment Methods: ${storeInfo.paymentMethods?.join(", ") || "Cash, Credit/Debit"}
- Amenities: ${storeInfo.amenities?.join(", ") || "Dine-in, Takeout, Bilingual Menu"}
- Facilities & Policies:
  • Restroom: ${p.restroomLocationEn || "Available inside for guests."} ${p.restroomCodeEn ? `(Access code: ${p.restroomCodeEn})` : ""}
  • Guest WiFi: ${p.wifiName ? `Network "${p.wifiName}", Password "${p.wifiPassword || "welcome"}"` : `Network "${storeInfo.name}_Guest", Password "welcome"`}
  • Parking: ${p.parkingPolicyEn || "Customer parking available on site or nearby."}
  • Takeout & Delivery: ${p.deliveryPolicyEn || "Takeout available for orders placed in-store or by phone."}
  • Return / Satisfaction Policy: ${p.returnPolicyEn || "We prioritize guest satisfaction; please notify staff immediately if you have any questions."}

=== 2. COMPLETE OFFICIAL MENU & CATALOG (${products.length} ITEMS) ===
${menuLines.length > 0 ? menuLines.join("\n") : "Full menu available in-store."}

=== 3. FREQUENTLY ASKED QUESTIONS ===
${faqLines.length > 0 ? faqLines.join("\n") : "None specified."}

=== BEHAVIOR GUIDELINES ===
1. MENU & CATALOG QUESTIONS:
   - When asked what is on the menu, what dishes/items are sold, or what categories exist, answer using SPECIFIC items and exact prices from the catalog above!
   - When asked for recommendations, recommend top or popular dishes from THIS menu with their prices and descriptions.
   - When asked for the price of any item, provide the exact price listed in the catalog.
   - When asked about dietary restrictions (vegetarian, vegan, gluten-free, dairy, nuts), check the item descriptions, tags, and allergens listed in the catalog above.
2. BUSINESS QUESTIONS (HOURS, LOCATION, PHONE):
   - When asked where the place is located or for the address: state "${storeInfo.address}".
   - When asked for the phone number: state "${storeInfo.phone ? storeInfo.phone : "We do not have a public phone number listed; please visit us in person at " + storeInfo.address}".
   - When asked for hours: provide the exact hours for the relevant day or the full weekly schedule.
3. CONCISENESS & HOSPITALITY:
   - Keep answers clear, direct, and conversational (1 to 3 friendly sentences, or a clean bulleted list for menu items).
   - Avoid generic preamble or unnecessary fluff.
4. BILINGUAL RESPONSE:
   - Match the user's language: If the user speaks or writes in Spanish, reply fluently and warmly in Spanish. If they write in English, reply in English.`;
}

/* ================================================================
   LOCAL DETERMINISTIC FALLBACK STORE KNOWLEDGE ENGINE
   (Used when offline or during Gemini API rate limits/outages)
   ================================================================ */
function generateLocalStoreReply(merchant: MerchantConfig, message: string, lang: "es" | "en"): string {
  const info = merchant.storeInfo;
  const p = info.policies || {};
  const products = merchant.products || [];
  const categories = merchant.categories || [];
  const lowerMsg = message.toLowerCase().trim();

  // Language detection
  const hasSpanishIndicators =
    lang === "es" ||
    /[áéíóúñ¿¡]/.test(lowerMsg) ||
    /\b(donde|dónde|ubicacion|ubicación|direccion|dirección|horario|horarios|abren|cierran|telefono|teléfono|llamar|contacto|menu|menú|platos|carta|comida|que|qué|tienen|venden|cuanto|cuánto|cuesta|precio|recomienda|recomiendan|recomiendas|sin gluten|vegano|vegetariano|alergia|alergias|baño|clave|gracias|hola|buenas|tardes|noches)\b/i.test(
      lowerMsg
    );

  const isEnglish = !hasSpanishIndicators;

  // 1. LOCATION / ADDRESS
  if (
    lowerMsg.includes("where") ||
    lowerMsg.includes("address") ||
    lowerMsg.includes("location") ||
    lowerMsg.includes("direccion") ||
    lowerMsg.includes("dirección") ||
    lowerMsg.includes("donde") ||
    lowerMsg.includes("dónde") ||
    lowerMsg.includes("ubicacion") ||
    lowerMsg.includes("ubicación") ||
    lowerMsg.includes("llegar")
  ) {
    return isEnglish
      ? `${info.name} is located at ${info.address}.`
      : `${info.name} está ubicado en ${info.address}.`;
  }

  // 2. PHONE NUMBER
  if (
    lowerMsg.includes("phone") ||
    lowerMsg.includes("telefono") ||
    lowerMsg.includes("teléfono") ||
    lowerMsg.includes("llamar") ||
    lowerMsg.includes("call") ||
    lowerMsg.includes("contacto") ||
    lowerMsg.includes("numero") ||
    lowerMsg.includes("número") ||
    lowerMsg.includes("number")
  ) {
    if (info.phone && info.phone.trim()) {
      return isEnglish
        ? `You can reach ${info.name} by phone at ${info.phone}.`
        : `Puede comunicarse con ${info.name} por teléfono al ${info.phone}.`;
    } else {
      return isEnglish
        ? `${info.name} is located at ${info.address}. Please visit us in person or reach out through our digital storefront!`
        : `${info.name} se encuentra en ${info.address}. ¡Le invitamos a visitarnos en persona o contactarnos por nuestro menú digital!`;
    }
  }

  // 3. HOURS & SCHEDULE
  if (
    lowerMsg.includes("hour") ||
    lowerMsg.includes("open") ||
    lowerMsg.includes("close") ||
    lowerMsg.includes("schedule") ||
    lowerMsg.includes("horario") ||
    lowerMsg.includes("abierto") ||
    lowerMsg.includes("cierran") ||
    lowerMsg.includes("abren")
  ) {
    if (lowerMsg.includes("sunday") || lowerMsg.includes("domingo")) {
      return isEnglish
        ? `On Sundays, ${info.name} is open: ${info.hours?.sunday || "Open"}.`
        : `Los domingos, ${info.name} atiende en el horario de: ${info.hours?.sunday || "Abierto"}.`;
    }
    if (lowerMsg.includes("saturday") || lowerMsg.includes("sabado") || lowerMsg.includes("sábado")) {
      return isEnglish
        ? `On Saturdays, ${info.name} is open: ${info.hours?.saturday || "Open"}.`
        : `Los sábados, ${info.name} atiende en el horario de: ${info.hours?.saturday || "Abierto"}.`;
    }
    const fullHours = `Mon-Fri: ${info.hours?.monday_friday || "Open"}, Sat: ${info.hours?.saturday || "Open"}, Sun: ${info.hours?.sunday || "Open"}`;
    return isEnglish
      ? `Operating Hours for ${info.name}: ${fullHours}.`
      : `Horario de atención para ${info.name}: ${fullHours}.`;
  }

  // 4. DIETARY RESTRICTIONS (VEGAN, GLUTEN-FREE, VEGETARIAN, ALLERGIES)
  if (
    lowerMsg.includes("gluten") ||
    lowerMsg.includes("vegan") ||
    lowerMsg.includes("vegano") ||
    lowerMsg.includes("vegetarian") ||
    lowerMsg.includes("vegetariano") ||
    lowerMsg.includes("alergia") ||
    lowerMsg.includes("allergy")
  ) {
    const isGlutenQuery = lowerMsg.includes("gluten");
    const isVeganQuery = lowerMsg.includes("vegan") || lowerMsg.includes("vegano");

    let matched = products.filter((prod) => {
      const tags = (prod.tags || []).map((t) => t.toLowerCase());
      const desc = `${prod.descriptionEn} ${prod.descriptionEs}`.toLowerCase();

      if (isGlutenQuery && (tags.includes("sin gluten") || tags.includes("gluten-free") || desc.includes("gluten-free") || desc.includes("sin gluten"))) {
        return true;
      }
      if (isVeganQuery && (tags.includes("vegano") || tags.includes("vegan") || desc.includes("vegano") || desc.includes("vegan"))) {
        return true;
      }
      return tags.some((t) => t.includes("vegetariano") || t.includes("saludable"));
    });

    if (matched.length === 0) matched = products.slice(0, 3);
    const itemsList = matched.slice(0, 4).map((i) => `${isEnglish ? i.nameEn : i.nameEs} (${i.price})`).join(", ");

    return isEnglish
      ? `We offer options to accommodate dietary needs at ${info.name}! Recommended items: ${itemsList}. Please inform our team of any specific allergies when ordering.`
      : `¡En ${info.name} contamos con opciones para necesidades dietéticas! Recomendaciones: ${itemsList}. Por favor avise a nuestro personal sobre cualquier alergia al ordenar.`;
  }

  // 5. RECOMMENDATIONS & POPULAR DISHES
  if (
    lowerMsg.includes("recommend") ||
    lowerMsg.includes("recomiend") ||
    lowerMsg.includes("popular") ||
    lowerMsg.includes("best") ||
    lowerMsg.includes("especial") ||
    lowerMsg.includes("signature")
  ) {
    const populars = products.filter((prod) => prod.popular || prod.badge);
    const list = (populars.length > 0 ? populars : products).slice(0, 3);
    const listStr = list.map((i) => `${isEnglish ? i.nameEn : i.nameEs} (${i.price})`).join(", ");

    return isEnglish
      ? `Guest favorites at ${info.name} include: ${listStr}. Would you like more details on any of these dishes?`
      : `Los platos favoritos en ${info.name} incluyen: ${listStr}. ¿Desea más información sobre alguno de ellos?`;
  }

  // 6. SPECIFIC PRODUCT SEARCH
  for (const prod of products) {
    const nameEnLower = prod.nameEn.toLowerCase();
    const nameEsLower = prod.nameEs.toLowerCase();
    const words = [...nameEnLower.split(" "), ...nameEsLower.split(" ")].filter((w) => w.length > 3);
    const isDirectMatch = lowerMsg.includes(nameEnLower) || lowerMsg.includes(nameEsLower);
    const isKeywordMatch = words.some((w) => lowerMsg.includes(w) && !["fresh", "plato", "super", "house"].includes(w));

    if (isDirectMatch || isKeywordMatch) {
      const name = isEnglish ? prod.nameEn : prod.nameEs;
      const desc = isEnglish ? prod.descriptionEn : prod.descriptionEs;
      return isEnglish
        ? `${name} is available for ${prod.price}. ${desc}`
        : `${name} está disponible por ${prod.price}. ${desc}`;
    }
  }

  // 7. MENU / CATALOG OVERVIEW
  if (
    lowerMsg.includes("menu") ||
    lowerMsg.includes("menú") ||
    lowerMsg.includes("catalog") ||
    lowerMsg.includes("platos") ||
    lowerMsg.includes("carta") ||
    lowerMsg.includes("dishes") ||
    lowerMsg.includes("what do you have") ||
    lowerMsg.includes("que tienen") ||
    lowerMsg.includes("qué tienen") ||
    lowerMsg.includes("venden") ||
    lowerMsg.includes("sell")
  ) {
    const catNames = categories
      .map((c) => (isEnglish ? c.nameEn : c.nameEs))
      .filter((c) => !c.toLowerCase().includes("all") && !c.toLowerCase().includes("todos"));
    const catStr = catNames.length > 0 ? catNames.join(", ") : "our signature items";
    const sampleItems = products.slice(0, 3).map((i) => `${isEnglish ? i.nameEn : i.nameEs} (${i.price})`).join(", ");

    return isEnglish
      ? `Our menu at ${info.name} features ${catStr}. Top items include: ${sampleItems}. You can explore the full catalog in the Menu tab!`
      : `El menú de ${info.name} ofrece ${catStr}. Destacados: ${sampleItems}. ¡Puede explorar el catálogo completo en la pestaña Menú!`;
  }

  // 8. PAYMENT & POLICIES
  if (
    lowerMsg.includes("pay") ||
    lowerMsg.includes("card") ||
    lowerMsg.includes("cash") ||
    lowerMsg.includes("pago") ||
    lowerMsg.includes("tarjeta") ||
    lowerMsg.includes("efectivo") ||
    lowerMsg.includes("apple pay")
  ) {
    return isEnglish
      ? `${info.name} accepts: ${info.paymentMethods.join(", ")}.`
      : `${info.name} acepta los siguientes métodos de pago: ${info.paymentMethods.join(", ")}.`;
  }

  if (lowerMsg.includes("wifi") || lowerMsg.includes("internet")) {
    return isEnglish
      ? `Guest WiFi: Network "${p.wifiName || info.name + "_Guest"}", Password: "${p.wifiPassword || "welcome"}"`
      : `WiFi para clientes: Red "${p.wifiName || info.name + "_Guest"}", Contraseña: "${p.wifiPassword || "welcome"}"`;
  }

  if (lowerMsg.includes("restroom") || lowerMsg.includes("bathroom") || lowerMsg.includes("baño") || lowerMsg.includes("bano")) {
    return isEnglish
      ? `Restroom: ${p.restroomLocationEn || "Available inside for guests."} ${p.restroomCodeEn ? `(Code: ${p.restroomCodeEn})` : ""}`
      : `Baño: ${p.restroomLocationEs || "Disponible en el establecimiento para clientes."} ${p.restroomCodeEs ? `(Código: ${p.restroomCodeEs})` : ""}`;
  }

  // 9. GREETING
  if (
    lowerMsg.includes("hello") ||
    lowerMsg.includes("hi") ||
    lowerMsg.includes("hey") ||
    lowerMsg.includes("hola") ||
    lowerMsg.includes("buenos") ||
    lowerMsg.includes("buenas")
  ) {
    return isEnglish
      ? `Hello! Welcome to ${info.name}. How can I assist you with our menu, hours, or location today?`
      : `¡Hola! Bienvenido a ${info.name}. ¿En qué puedo ayudarle hoy con nuestro menú, horarios o ubicación?`;
  }

  // 10. DEFAULT SUMMARY
  const topDishes = products.slice(0, 3).map((i) => (isEnglish ? i.nameEn : i.nameEs)).join(", ");
  return isEnglish
    ? `Welcome to ${info.name}! We are located at ${info.address}. Feel free to ask about our hours (${info.hours?.monday_friday || "Open"}), recommendations like ${topDishes}, or any item on our menu!`
    : `¡Bienvenido a ${info.name}! Estamos ubicados en ${info.address}. Pregúnteme por nuestros horarios (${info.hours?.monday_friday || "Abierto"}), recomendaciones como ${topDishes}, o cualquier plato del menú.`;
}

/* ================================================================
   POST ROUTE HANDLER
   ================================================================ */
export async function POST(req: NextRequest) {
  try {
    const { messages, lang = "en", merchantId, merchantConfig } = await req.json();

    if (!messages || !Array.isArray(messages)) {
      return NextResponse.json({ error: "Invalid payload" }, { status: 400 });
    }

    // Resolve merchant: prioritize full client-passed config, fallback to registry
    const merchant: MerchantConfig =
      merchantConfig && merchantConfig.storeInfo
        ? merchantConfig
        : getMerchantById(merchantId || "demo");

    const rawLast = messages[messages.length - 1];
    const lastMessage = (rawLast?.text || rawLast?.content || "").trim();
    const lowerMsg = lastMessage.toLowerCase();

    // Check if query is in English
    const hasSpanishIndicators =
      lang === "es" ||
      /[áéíóúñ¿¡]/.test(lowerMsg) ||
      /\b(donde|dónde|ubicacion|ubicación|direccion|dirección|horario|horarios|abren|cierran|telefono|teléfono|llamar|contacto|menu|menú|platos|carta|comida|que|qué|tienen|venden|cuanto|cuánto|cuesta|precio|recomienda|recomiendan|recomiendas|sin gluten|vegano|vegetariano|alergia|alergias|baño|clave|gracias|hola|buenas|tardes|noches)\b/i.test(
        lowerMsg
      );
    const isEnglish = !hasSpanishIndicators;

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

    // DIRECT GEMINI AI ENGINE (Configured with complete place menu & details)
    if (apiKey) {
      const systemInstruction = buildStoreKnowledgePrompt(merchant);
      const candidateModels = ["gemini-3.8-flash", "gemini-flash-latest"];
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

    // HIGH-ACCURACY DYNAMIC STORE FALLBACK ENGINE
    let reply = generateLocalStoreReply(merchant, lastMessage, lang);

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
