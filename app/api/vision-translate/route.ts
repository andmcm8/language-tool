import { NextRequest, NextResponse } from "next/server";
import { generateWithFallback } from "@/lib/gemini";

/* ================================================================
   VISION TRANSLATE — extracts text from image + translates to Spanish
   1. Gemini Vision (if valid key)
   2. Returns empty → client falls back to Tesseract + /api/translate
   ================================================================ */

async function tryGeminiVision(
  base64Data: string,
  mimeType: string,
  targetLang: "es" | "en"
): Promise<{ original: string; translated: string }[]> {
  const source = targetLang === "en" ? "Spanish (or any non-English language)" : "English (or any non-Spanish language)";
  const target = targetLang === "en" ? "English" : "Spanish";
  const example =
    targetLang === "en"
      ? '{ "original": "Línea o plato original", "translated": "English translation" }'
      : '{ "original": "English line or menu item", "translated": "Traducción al español" }';

  try {
    const raw = await generateWithFallback({
      timeoutMs: 30000,
      contents: [
      {
        inlineData: {
          mimeType,
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
5. Provide the exact original ${source} text and its accurate ${target} translation for every line or section.
6. Preserve time designations like "12 pm - 4 pm" as "12 pm - 4 pm" (or "12:00 PM - 4:00 PM"). NEVER translate "pm" into "pie", "pastel", or "tarta".

Return ONLY a raw JSON array (no markdown code blocks, no explanation text):
[
  ${example}
]
If no readable text is found in the image, return: []`,
      },
      ],
    });

    if (!raw) return [];
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
    const { imageBase64, targetLang } = await req.json();
    if (!imageBase64) return NextResponse.json({ lines: [] });

    const mimeMatch = imageBase64.match(/^data:(image\/[\w.+-]+);base64,/);
    const mimeType = mimeMatch ? mimeMatch[1] : "image/jpeg";
    const base64Data = imageBase64.replace(/^data:image\/[\w.+-]+;base64,/, "");
    const lines = await tryGeminiVision(base64Data, mimeType, targetLang === "en" ? "en" : "es");

    return NextResponse.json({ lines });
  } catch (error: any) {
    console.error("Vision-translate error:", error?.message);
    return NextResponse.json({ lines: [] });
  }
}
