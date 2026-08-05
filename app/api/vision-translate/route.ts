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
  if (!apiKey || !apiKey.startsWith("AIza")) return [];

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
        text: `Extract ALL visible text from this image. For each text block, provide the original English text and its Spanish translation.
Return ONLY a raw JSON array (no markdown, no code fences):
[{"original":"English text","translated":"Texto en español"}]
If no text found, return: []`,
      },
    ]);

    const raw = result.response.text().trim();
    const match = raw.match(/\[[\s\S]*\]/);
    if (match) return JSON.parse(match[0]);
    return [];
  } catch {
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
