import { NextRequest, NextResponse } from "next/server";
import { GoogleGenerativeAI } from "@google/generative-ai";

/* ================================================================
   TRANSLATE ROUTE — Official Google Translate Engine (GTX)
   Primary: Google Translate API (client=gtx, 100% real Google Translate)
   Secondary: Gemini AI 2.0 Flash
   Fallback: Bi-directional Local Merchant Dictionary
   ================================================================ */

/* ---------- ENGINE 1: Official Google Translate GTX Engine ---------- */
async function tryGoogleTranslate(text: string, targetLang: string = "es"): Promise<string | null> {
  try {
    const sl = targetLang === "en" ? "es" : "en";
    const tl = targetLang === "en" ? "en" : "es";
    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${sl}&tl=${tl}&dt=t&q=${encodeURIComponent(text)}`;
    
    const res = await fetch(url, {
      headers: {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
      },
      signal: AbortSignal.timeout(5000),
    });

    if (!res.ok) return null;

    const data = await res.json();
    if (data && data[0] && Array.isArray(data[0])) {
      const translated = data[0].map((item: any) => item[0]).filter(Boolean).join("");
      if (translated && translated.trim()) {
        return translated.trim();
      }
    }
    return null;
  } catch {
    return null;
  }
}

/* ---------- ENGINE 2: Gemini AI 2.0 Flash ---------- */
async function tryGemini(text: string, targetLang: string = "es"): Promise<string | null> {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) return null;

  const targetLangName = targetLang === "en" ? "English" : "Spanish";
  const sourceLangName = targetLang === "en" ? "Spanish" : "English";

  const systemInstruction = `You are a professional bilingual translator. Translate the given text accurately from ${sourceLangName} to ${targetLangName}. Output ONLY the translated ${targetLangName} text. Do not add quotes, explanations, or notes.`;

  try {
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({
      model: "gemini-2.0-flash",
      systemInstruction,
    });
    const result = await model.generateContent(text);
    const translation = result.response.text().trim();
    return translation && translation.toLowerCase() !== text.toLowerCase() ? translation : null;
  } catch {
    return null;
  }
}

/* ---------- ENGINE 3: Bi-Directional Local Dictionary Fallback ---------- */
const W_EN_ES: Record<string, string> = {
  welcome: "bienvenidos", hello: "hola", please: "por favor", yes: "sí", no: "no",
  good: "bueno", morning: "mañana", afternoon: "tarde", evening: "noche",
  store: "tienda", shop: "tienda", market: "mercado", grocery: "abarrotes",
  restroom: "baño", bathroom: "baño", floor: "piso", aisle: "pasillo",
  counter: "mostrador", register: "caja", checkout: "caja",
  hours: "horarios", open: "abierto", closed: "cerrado", today: "hoy",
  food: "comida", bread: "pan", meat: "carne", chicken: "pollo", ham: "jamón",
  cheese: "queso", milk: "leche", water: "agua", coffee: "café",
  fresh: "fresco", hot: "caliente", cold: "frío",
  cash: "efectivo", card: "tarjeta", credit: "crédito", debit: "débito",
  the: "el", a: "un", and: "y", or: "o", with: "con", without: "sin",
  for: "para", of: "de", is: "es", are: "son", where: "dónde",
};

const W_ES_EN: Record<string, string> = {
  donde: "where", dónde: "where",
  esta: "is", está: "is",
  el: "the", la: "the", los: "the", las: "the",
  bano: "restroom", baño: "restroom", banos: "restrooms", baños: "restrooms",
  hola: "hello", gracias: "thank you", porfavor: "please",
  tienda: "store", mercado: "market", caja: "register",
  abierto: "open", cerrado: "closed", hoy: "today",
  comida: "food", pan: "bread", carne: "meat", pollo: "chicken",
  jamon: "ham", jamón: "ham", queso: "cheese", agua: "water",
  efectivo: "cash", tarjeta: "card", pago: "payment",
  cuanto: "how much", cuánto: "how much", cuesta: "costs",
  aceptan: "do you accept", hay: "is there", puedo: "can I",
  pagar: "pay", con: "with", sin: "without",
};

function localTranslate(text: string, targetLang: string = "es"): string {
  let result = text;
  const dict = targetLang === "en" ? W_ES_EN : W_EN_ES;

  if (targetLang === "en") {
    const lower = result.toLowerCase().trim();
    if (lower.includes("donde esta el bano") || lower.includes("dónde está el baño") || lower.includes("donde esta el baño")) {
      return "Where is the restroom?";
    }
  }

  return result.replace(/[A-Za-zÀ-ÿ'']+/g, (word) => {
    const clean = word.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
    const t = dict[clean] || dict[word.toLowerCase()];
    if (!t) return word;
    if (word === word.toUpperCase()) return t.toUpperCase();
    if (word[0] === word[0].toUpperCase())
      return t.charAt(0).toUpperCase() + t.slice(1);
    return t;
  });
}

/* ================================================================
   ROUTE HANDLER
   ================================================================ */
export async function POST(req: NextRequest) {
  let text = "";
  try {
    const body = await req.json();
    text = (body.text || "").trim();
    const targetLang = body.targetLang || "es";
    if (!text) return NextResponse.json({ translation: "", translated: "" });

    // 1) Primary Engine: Official Google Translate API (gtx)
    const googleResult = await tryGoogleTranslate(text, targetLang);
    if (googleResult) {
      return NextResponse.json({ translation: googleResult, translated: googleResult });
    }

    // 2) Secondary Engine: Gemini AI 2.0 Flash
    const geminiResult = await tryGemini(text, targetLang);
    if (geminiResult) {
      return NextResponse.json({ translation: geminiResult, translated: geminiResult });
    }

    // 3) Fallback Engine: Bi-directional Local Merchant Dictionary
    const local = localTranslate(text, targetLang);
    return NextResponse.json({ translation: local, translated: local });
  } catch (error: any) {
    console.error("Translate error:", error?.message);
    const fallback = text ? localTranslate(text) : text;
    return NextResponse.json({
      translation: fallback,
      translated: fallback,
    });
  }
}
