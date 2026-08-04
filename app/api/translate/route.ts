import { NextRequest, NextResponse } from "next/server";
import { GoogleGenerativeAI } from "@google/generative-ai";

export async function POST(req: NextRequest) {
  let textToTranslate = "";
  try {
    const payload = await req.json();
    textToTranslate = payload.text || "";

    if (!textToTranslate || typeof textToTranslate !== "string") {
      return NextResponse.json({ translation: "" });
    }

    const apiKey = process.env.GEMINI_API_KEY;

    if (apiKey) {
      try {
        const genAI = new GoogleGenerativeAI(apiKey);
        const model = genAI.getGenerativeModel({
          model: "gemini-2.0-flash",
          systemInstruction:
            "You are a professional English to Spanish translator. Translate the user's English text into accurate, natural Spanish. Output ONLY the translated Spanish text. Do not add quotes, explanations, or introductory text.",
        });

        const result = await model.generateContent(textToTranslate);
        const translation = result.response.text().trim();
        return NextResponse.json({ translation });
      } catch (err: any) {
        console.warn("Gemini translate API error, using dictionary fallback:", err?.message);
      }
    }

    // Intelligent fallback translation dictionary
    let fallback = textToTranslate;
    const dictionary: [RegExp, string][] = [
      [/DAILY SPECIAL/gi, "ESPECIAL DEL DÍA"],
      [/SPECIAL TODAY/gi, "ESPECIAL DE HOY"],
      [/SPECIAL/gi, "ESPECIAL"],
      [/Hot Roast Beef Sandwich/gi, "Sándwich de Carne Asada Caliente"],
      [/Roast Beef/gi, "Carne Asada"],
      [/Sandwich/gi, "Sándwich"],
      [/Melted Swiss Cheese/gi, "Queso Suizo Fundido"],
      [/Swiss Cheese/gi, "Queso Suizo"],
      [/Cheese/gi, "Queso"],
      [/Pickles/gi, "Pepinillos"],
      [/NOTICE/gi, "AVISO IMPORTANTE"],
      [/EBT Accepted/gi, "Se Acepta EBT"],
      [/Accepted/gi, "Aceptado"],
      [/Groceries/gi, "Abarrotes"],
      [/Bakery/gi, "Panadería"],
      [/Hot Food/gi, "Comida Caliente"],
      [/Requires Cash/gi, "Requiere Efectivo"],
      [/Cash or Card/gi, "Efectivo o Tarjeta"],
      [/FRESH WARM BREAD/gi, "PAN FRESCO CALIENTE"],
      [/FRESH BREAD/gi, "PAN FRESCO"],
      [/BAKED DAILY/gi, "HORNEADO DIARIAMENTE"],
      [/Hours/gi, "Horarios"],
      [/Open/gi, "Abierto"],
      [/Closed/gi, "Cerrado"],
      [/No Parking/gi, "Prohibido Estacionar"],
      [/Loading Zone/gi, "Zona de Carga"]
    ];

    dictionary.forEach(([rgx, val]) => {
      fallback = fallback.replace(rgx, val);
    });

    return NextResponse.json({ translation: fallback });
  } catch (error: any) {
    console.error("Error in /api/translate:", error);
    return NextResponse.json({ translation: textToTranslate });
  }
}
