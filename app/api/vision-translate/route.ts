import { NextRequest, NextResponse } from "next/server";
import { GoogleGenerativeAI } from "@google/generative-ai";

export async function POST(req: NextRequest) {
  try {
    const { imageBase64 } = await req.json();

    if (!imageBase64) {
      return NextResponse.json({ lines: [] });
    }

    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      return NextResponse.json({ lines: [] });
    }

    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });

    // Strip the data URL prefix to get raw base64
    const base64Data = imageBase64.replace(/^data:image\/\w+;base64,/, "");

    const result = await model.generateContent([
      {
        inlineData: {
          mimeType: "image/jpeg",
          data: base64Data,
        },
      },
      {
        text: `You are an OCR and translation engine. Carefully analyze this image and extract EVERY piece of visible text — signs, menus, labels, notices, prices, handwritten text, anything.

For each distinct text block you find, provide:
1. "original" — the exact text as it appears in the image
2. "translated" — natural, accurate Spanish translation

Return ONLY a raw JSON array (no markdown fences, no explanation). Format:
[{"original":"English text","translated":"Texto en español"}]

Rules:
- Extract ALL text, even small labels or numbers
- Keep each text block as a separate array entry (don't merge separate signs/lines)
- If a piece of text is already in Spanish, keep it the same for both fields
- If no text found at all, return: []`,
      },
    ]);

    const responseText = result.response.text().trim();

    let lines: { original: string; translated: string }[] = [];
    try {
      // Extract JSON array from response (handles markdown fences if present)
      const jsonMatch = responseText.match(/\[[\s\S]*\]/);
      if (jsonMatch) {
        lines = JSON.parse(jsonMatch[0]);
      }
    } catch (e) {
      console.error("Failed to parse Gemini Vision response:", e, responseText);
    }

    return NextResponse.json({ lines });
  } catch (error: any) {
    console.error("Vision-translate error:", error?.message);
    return NextResponse.json({ lines: [] }, { status: 200 });
  }
}
