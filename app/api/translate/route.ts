import { NextRequest, NextResponse } from "next/server";
import { GoogleGenerativeAI } from "@google/generative-ai";

/* ================================================================
   TRANSLATE ROUTE — Robust Bi-Directional (EN ↔ ES) Translation Engine
   ================================================================ */

/* ---------- ENGINE 1: Gemini AI ---------- */
async function tryGemini(text: string, targetLang: string = "es"): Promise<string | null> {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) return null;

  const isEs = targetLang === "es";
  const targetLangName = isEs ? "Spanish" : "English";
  const sourceLangName = isEs ? "English" : "Spanish";

  const systemInstruction = `You are a professional bilingual translator between English and Spanish.
Translate the input text accurately into ${targetLangName}.
If the text is already in ${targetLangName}, translate it into ${sourceLangName}.
Output ONLY the final translated text without any quotation marks, commentary, or explanations.`;

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

/* ---------- ENGINE 2: MyMemory Translation API ---------- */
async function tryMyMemory(text: string, targetLang: string = "es"): Promise<string | null> {
  try {
    const langpair = targetLang === "en" ? "es|en" : "en|es";
    const url = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(
      text
    )}&langpair=${langpair}`;
    const res = await fetch(url, { signal: AbortSignal.timeout(6000) });
    const data = await res.json();
    const translated = data?.responseData?.translatedText;
    if (
      translated &&
      typeof translated === "string" &&
      translated.toUpperCase() !== text.toUpperCase() &&
      !translated.includes("PLEASE SELECT TWO LANGUAGES") &&
      !translated.includes("MYMEMORY WARNING")
    ) {
      if (text === text.toUpperCase()) return translated.toUpperCase();
      if (
        text[0] === text[0].toUpperCase() &&
        text.slice(1) === text.slice(1).toLowerCase()
      ) {
        return (
          translated.charAt(0).toUpperCase() +
          translated.slice(1).toLowerCase()
        );
      }
      return translated;
    }
    return null;
  } catch {
    return null;
  }
}

/* ---------- ENGINE 3: Bi-Directional Local Dictionary Fallback ---------- */
const W_EN_ES: Record<string, string> = {
  welcome:"bienvenidos",hello:"hola",please:"por favor",yes:"sí",no:"no",
  good:"bueno",morning:"mañana",afternoon:"tarde",evening:"noche",
  store:"tienda",shop:"tienda",market:"mercado",grocery:"abarrotes",
  entrance:"entrada",exit:"salida",parking:"estacionamiento",
  restroom:"baño",bathroom:"baño",floor:"piso",aisle:"pasillo",
  counter:"mostrador",register:"caja",checkout:"caja",
  hours:"horarios",hour:"hora",open:"abierto",closed:"cerrado",
  today:"hoy",daily:"diariamente",monday:"lunes",tuesday:"martes",
  wednesday:"miércoles",thursday:"jueves",friday:"viernes",
  saturday:"sábado",sunday:"domingo",until:"hasta",from:"desde",
  food:"comida",menu:"menú",meal:"comida",plate:"plato",
  bread:"pan",meat:"carne",beef:"res",steak:"bistec",pork:"cerdo",
  chicken:"pollo",ham:"jamón",fish:"pescado",cheese:"queso",
  milk:"leche",eggs:"huevos",egg:"huevo",rice:"arroz",beans:"frijoles",
  water:"agua",juice:"jugo",soda:"refresco",coffee:"café",tea:"té",
  fresh:"fresco",hot:"caliente",cold:"frío",warm:"tibio",
  cash:"efectivo",card:"tarjeta",credit:"crédito",debit:"débito",
  payment:"pago",accepted:"aceptado",required:"requerido",
  price:"precio",free:"gratis",discount:"descuento",
  the:"el",a:"un",and:"y",or:"o",with:"con",without:"sin",
  for:"para",of:"de",is:"es",are:"son",where:"dónde",how:"cómo",
};

const W_ES_EN: Record<string, string> = {
  donde: "where", dónde: "where",
  esta: "is", está: "is",
  el: "the", la: "the", los: "the", las: "the",
  bano: "bathroom", baño: "bathroom", banos: "restrooms", baños: "restrooms",
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

const SPANISH_PHRASES: [RegExp, string][] = [
  [/donde esta el bano/gi, "Where is the bathroom?"],
  [/dónde está el baño/gi, "Where is the bathroom?"],
  [/donde esta el deli/gi, "Where is the deli?"],
  [/dónde está el deli/gi, "Where is the deli?"],
  [/cuanto cuesta/gi, "How much does it cost?"],
  [/cuánto cuesta/gi, "How much does it cost?"],
  [/aceptan ebt/gi, "Do you accept EBT?"],
  [/aceptan tarjetas/gi, "Do you accept cards?"],
  [/puedo pagar con efectivo/gi, "Can I pay with cash?"],
  [/cuales son los horarios/gi, "What are the store hours?"],
];

function localTranslate(text: string, targetLang: string = "es"): string {
  let result = text;
  if (targetLang === "en") {
    for (const [p, r] of SPANISH_PHRASES) {
      if (p.test(result)) return r;
    }
    return result.replace(/[A-Za-zÀ-ÿ'']+/g, (word) => {
      const clean = word.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
      const t = W_ES_EN[clean] || W_ES_EN[word.toLowerCase()];
      if (!t) return word;
      if (word === word.toUpperCase()) return t.toUpperCase();
      if (word[0] === word[0].toUpperCase())
        return t.charAt(0).toUpperCase() + t.slice(1);
      return t;
    });
  }

  return result.replace(/[A-Za-zÀ-ÿ'']+/g, (word) => {
    const t = W_EN_ES[word.toLowerCase()];
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

    // 1) Try Gemini AI
    const gemini = await tryGemini(text, targetLang);
    if (gemini) return NextResponse.json({ translation: gemini, translated: gemini });

    // 2) Try MyMemory Translation API
    const myMemory = await tryMyMemory(text, targetLang);
    if (myMemory) return NextResponse.json({ translation: myMemory, translated: myMemory });

    // 3) Bi-directional Local dictionary fallback
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
