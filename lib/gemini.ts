import { GoogleGenerativeAI, Content, Part } from "@google/generative-ai";

/* ================================================================
   SHARED GEMINI CLIENT
   Google retires Gemini model IDs regularly (gemini-2.0-flash and
   gemini-2.5-flash now return 404) and busy models return 503
   "high demand". Every AI route goes through this helper, which
   tries each model in order until one answers.

   To pin a specific model, set GEMINI_MODEL in .env.local / Vercel;
   it is tried first, before the defaults below.
   ================================================================ */
const DEFAULT_MODELS = [
  "gemini-3.5-flash",
  "gemini-3.8-flash",
  "gemini-flash-latest",
  "gemini-3.5-flash-lite",
  "gemini-flash-lite-latest",
];

export function getGeminiModels(): string[] {
  const pinned = process.env.GEMINI_MODEL?.trim();
  return pinned ? [pinned, ...DEFAULT_MODELS.filter((m) => m !== pinned)] : DEFAULT_MODELS;
}

interface GenerateOptions {
  systemInstruction?: string;
  /** Either a full multi-turn conversation or the parts of a single user turn. */
  contents: Content[] | (string | Part)[];
  timeoutMs?: number;
}

/**
 * Runs generateContent against each model in turn and returns the first
 * non-empty text, or null if no key is configured or every model failed.
 */
export async function generateWithFallback({
  systemInstruction,
  contents,
  timeoutMs = 20000,
}: GenerateOptions): Promise<string | null> {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    console.warn("GEMINI_API_KEY is not set; AI features are using local fallbacks.");
    return null;
  }

  const genAI = new GoogleGenerativeAI(apiKey);
  const isConversation =
    contents.length > 0 && typeof contents[0] === "object" && "role" in (contents[0] as object);

  for (const modelName of getGeminiModels()) {
    try {
      const model = genAI.getGenerativeModel(
        { model: modelName, ...(systemInstruction ? { systemInstruction } : {}) },
        { timeout: timeoutMs }
      );
      const result = isConversation
        ? await model.generateContent({ contents: contents as Content[] })
        : await model.generateContent(contents as (string | Part)[]);
      const text = result.response.text().trim();
      if (text) return text;
    } catch (err: any) {
      console.warn(`Gemini model ${modelName} failed:`, err?.message || err);
    }
  }
  return null;
}
