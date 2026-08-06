import { NextRequest, NextResponse } from "next/server";
import { GoogleGenerativeAI } from "@google/generative-ai";

/* ================================================================
   VISION TRANSLATE — extracts text from image + translates to Spanish
   1. Gemini Vision (if valid key)
   2. Returns empty → client falls back to Tesseract + /api/translate
   ================================================================ */

async function tryGeminiVision(
  base64Data: string
): Promise<{ original: string; translated: string }[]> {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    console.warn("No GEMINI_API_KEY found in environment");
    return [];
  }

  try {
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });

    const result = await model.generateContent([
      {
        inlineData: {
          mimeType: "image/jpeg",
          data: base64Data,
        },
      },
      {
        text: `You are an expert OCR and translation AI specialized in reading restaurant menus, store signs, product labels, notices, and printed documents.
CRITICAL TRANSLATION & LAYOUT INSTRUCTIONS:
1. Extract ALL visible text from the image with 100% accuracy.
2. Respect multi-column layouts, section headings, menu item names, ingredients, prices, and line breaks.
3. For multi-column menus, process Column 1 top-to-bottom first, then process Column 2 top-to-bottom.
4. Do NOT merge separate menu items or separate paragraphs together.
5. Provide the exact original English text and its accurate Spanish translation for every line or section.

Return ONLY a raw JSON array (no markdown code blocks, no explanation text):
[
  { "original": "English line or menu item", "translated": "Traducción al español" }
]
If no readable text is found in the image, return: []`,
      },
    ]);

    const raw = result.response.text().trim();
    const match = raw.match(/\[[\s\S]*\]/);
    if (match) {
      const parsed = JSON.parse(match[0]);
      if (Array.isArray(parsed) && parsed.length > 0) {
        return parsed;
      }
    }
    return [];
  } catch (err: any) {
    console.error("Gemini Vision API error:", err?.message || err);
    return [];
  }
}

export async function POST(req: NextRequest) {
  try {
    const { imageBase64 } = await req.json();
    if (!imageBase64) return NextResponse.json({ lines: [] });

    const base64Data = imageBase64.replace(/^data:image\/\w+;base64,/, "");
    const lines = await tryGeminiVision(base64Data);

    return NextResponse.json({ lines });
  } catch (error: any) {
    console.error("Vision-translate error:", error?.message);
    return NextResponse.json({ lines: [] });
  }
}
