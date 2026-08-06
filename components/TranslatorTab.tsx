"use client";

import React, { useState, useRef } from "react";
import {
  Languages,
  ArrowRightLeft,
  Mic,
  MicOff,
  Volume2,
  Copy,
  Check,
  X,
  Sparkles,
  ArrowRight,
  Loader2,
} from "lucide-react";

interface TranslatorTabProps {
  lang: "es" | "en";
}

const QUICK_PHRASES = [
  {
    en: "Do you accept EBT / SNAP cards?",
    es: "¿Aceptan tarjetas EBT / SNAP?",
  },
  {
    en: "Where is the deli section?",
    es: "¿Dónde está la sección de deli?",
  },
  {
    en: "What are your store hours today?",
    es: "¿Cuáles son sus horarios de atención hoy?",
  },
  {
    en: "Do you have fresh baked bread?",
    es: "¿Tienen pan fresco horneado?",
  },
  {
    en: "How much is this item?",
    es: "¿Cuánto cuesta este artículo?",
  },
  {
    en: "Can I pay with cash or debit?",
    es: "¿Puedo pagar con efectivo o débito?",
  },
];

export default function TranslatorTab({ lang }: TranslatorTabProps) {
  const [sourceLang, setSourceLang] = useState<"en" | "es">("en");
  const [inputText, setInputText] = useState("");
  const [translatedText, setTranslatedText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef<any>(null);

  const targetLang = sourceLang === "en" ? "es" : "en";

  /* ---------- Real-Time / On-Demand Translation ---------- */
  const handleTranslate = async (textToTranslate?: string) => {
    const text = (textToTranslate !== undefined ? textToTranslate : inputText).trim();
    if (!text) {
      setTranslatedText("");
      return;
    }

    setIsLoading(true);
    try {
      const res = await fetch("/api/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text,
          targetLang,
        }),
      });

      const data = await res.json();
      if (data.translated) {
        setTranslatedText(data.translated);
      } else {
        setTranslatedText(text);
      }
    } catch {
      setTranslatedText(text);
    } finally {
      setIsLoading(false);
    }
  };

  /* ---------- Language Direction Switcher ---------- */
  const swapLanguages = () => {
    const newSource = sourceLang === "en" ? "es" : "en";
    setSourceLang(newSource);

    // Swap input and translated text
    const currentInput = inputText;
    const currentTrans = translatedText;
    setInputText(currentTrans);
    setTranslatedText(currentInput);
  };

  /* ---------- Speech-to-Text (Voice Dictation) ---------- */
  const toggleListening = () => {
    if (typeof window === "undefined") return;

    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert(
        lang === "es"
          ? "Reconocimiento de voz no soportado en este navegador."
          : "Speech recognition not supported in this browser."
      );
      return;
    }

    if (isListening) {
      if (recognitionRef.current) recognitionRef.current.stop();
      setIsListening(false);
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.lang = sourceLang === "en" ? "en-US" : "es-ES";
      recognition.interimResults = true;
      recognition.continuous = false;

      recognition.onstart = () => setIsListening(true);

      recognition.onresult = (event: any) => {
        const transcript = Array.from(event.results)
          .map((result: any) => result[0].transcript)
          .join("");
        setInputText(transcript);
      };

      recognition.onerror = () => setIsListening(false);

      recognition.onend = () => {
        setIsListening(false);
        if (inputText.trim()) {
          handleTranslate();
        }
      };

      recognitionRef.current = recognition;
      recognition.start();
    } catch {
      setIsListening(false);
    }
  };

  /* ---------- Text-to-Speech (Audio Pronunciation) ---------- */
  const speakText = (text: string, speakLang: "es" | "en") => {
    if (typeof window === "undefined" || !("speechSynthesis" in window) || !text) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = speakLang === "es" ? "es-ES" : "en-US";
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
  };

  /* ---------- Copy to Clipboard ---------- */
  const copyTranslation = () => {
    if (!translatedText) return;
    navigator.clipboard.writeText(translatedText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="w-full max-w-md mx-auto p-4 pb-24 flex flex-col gap-4">
      {/* LANGUAGE DIRECTION BAR */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs p-2 flex items-center justify-between">
        <div className="flex-1 text-center font-extrabold text-xs text-slate-800 uppercase tracking-wide">
          {sourceLang === "en" ? "English" : "Español"}
        </div>

        <button
          onClick={swapLanguages}
          className="p-2 rounded-xl bg-slate-100 text-[#003ec7] hover:bg-blue-50 hover:scale-105 transition-all shadow-2xs"
          title="Swap Languages / Cambiar Idioma"
        >
          <ArrowRightLeft className="w-4 h-4" />
        </button>

        <div className="flex-1 text-center font-extrabold text-xs text-slate-800 uppercase tracking-wide">
          {targetLang === "es" ? "Español" : "English"}
        </div>
      </div>

      {/* INPUT CARD (Text + Voice Input) */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs p-3.5 space-y-3 relative">
        <div className="flex items-center justify-between text-xs font-bold text-slate-500">
          <span>{sourceLang === "en" ? "Source Text" : "Texto de Origen"}</span>
          {inputText && (
            <button
              onClick={() => {
                setInputText("");
                setTranslatedText("");
              }}
              className="text-slate-400 hover:text-slate-600 flex items-center gap-1 text-[11px]"
            >
              <X className="w-3.5 h-3.5" />
              <span>{lang === "es" ? "Borrar" : "Clear"}</span>
            </button>
          )}
        </div>

        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder={
            sourceLang === "en"
              ? "Type or speak text to translate..."
              : "Escriba o hable para traducir..."
          }
          rows={4}
          className="w-full text-base font-medium text-slate-900 placeholder:text-slate-400 bg-transparent border-0 focus:outline-none focus:ring-0 resize-none"
        />

        <div className="flex items-center justify-between pt-2 border-t border-slate-100">
          <div className="flex items-center gap-2">
            {/* Voice Dictation Button */}
            <button
              onClick={toggleListening}
              className={`p-2.5 rounded-xl text-xs font-bold flex items-center gap-1.5 transition-all ${
                isListening
                  ? "bg-rose-500 text-white animate-pulse"
                  : "bg-slate-100 text-slate-700 hover:bg-slate-200"
              }`}
            >
              {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4 text-[#003ec7]" />}
              <span>{isListening ? (lang === "es" ? "Escuchando…" : "Listening…") : (lang === "es" ? "Hablar" : "Voice")}</span>
            </button>

            {/* Audio Listen for Source */}
            {inputText && (
              <button
                onClick={() => speakText(inputText, sourceLang)}
                className="p-2.5 rounded-xl bg-slate-100 text-slate-600 hover:text-[#003ec7] transition-colors"
                title="Listen / Escuchar"
              >
                <Volume2 className="w-4 h-4" />
              </button>
            )}
          </div>

          {/* Action Translate Button */}
          <button
            onClick={() => handleTranslate()}
            disabled={isLoading || !inputText.trim()}
            className="px-4 py-2.5 rounded-xl bg-[#003ec7] text-white text-xs font-black flex items-center gap-1.5 shadow-md disabled:opacity-40 hover:brightness-110 transition-all"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <>
                <span>{lang === "es" ? "Traducir" : "Translate"}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </>
            )}
          </button>
        </div>
      </div>

      {/* OUTPUT TRANSLATION CARD */}
      <div className="bg-slate-900 text-white rounded-2xl border border-slate-800 shadow-md p-4 space-y-3">
        <div className="flex items-center justify-between text-xs font-black tracking-wider text-blue-400 uppercase">
          <span className="flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-blue-400" />
            <span>{targetLang === "es" ? "Traducción (Español)" : "Translation (English)"}</span>
          </span>

          {translatedText && (
            <div className="flex items-center gap-1">
              <button
                onClick={copyTranslation}
                className="p-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-slate-300 transition-colors"
                title="Copy / Copiar"
              >
                {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
              </button>

              <button
                onClick={() => speakText(translatedText, targetLang)}
                className="p-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-blue-400 transition-colors"
                title="Listen / Escuchar"
              >
                <Volume2 className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>

        <div className="min-h-[70px] text-base font-bold leading-relaxed text-slate-100">
          {translatedText ? (
            translatedText
          ) : (
            <span className="text-slate-500 font-normal italic text-sm">
              {lang === "es"
                ? "La traducción aparecerá aquí…"
                : "Translation will appear here…"}
            </span>
          )}
        </div>
      </div>

      {/* QUICK MERCHANT STORE PHRASES (1-Tap Chips) */}
      <div className="space-y-2 pt-1">
        <div className="text-xs font-black text-slate-700 uppercase tracking-wider">
          {lang === "es" ? "Frases Rápidas de Tienda" : "Quick Store Phrases"}
        </div>

        <div className="flex flex-wrap gap-1.5">
          {QUICK_PHRASES.map((phrase, idx) => {
            const displayPhrase = sourceLang === "en" ? phrase.en : phrase.es;
            return (
              <button
                key={idx}
                onClick={() => {
                  setInputText(displayPhrase);
                  handleTranslate(displayPhrase);
                }}
                className="px-3 py-1.5 bg-white border border-slate-200 rounded-full text-xs font-bold text-slate-700 hover:border-[#003ec7] hover:text-[#003ec7] hover:bg-blue-50 transition-all shadow-2xs text-left"
              >
                {displayPhrase}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
