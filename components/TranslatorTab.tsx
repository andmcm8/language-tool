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
  Tv,
  Star,
  RotateCw,
  CreditCard,
  Utensils,
  Clock,
  HelpCircle,
} from "lucide-react";

interface TranslatorTabProps {
  lang: "es" | "en";
}

const PHRASE_CATEGORIES = [
  { id: "all", labelEs: "Todas", labelEn: "All", icon: Sparkles },
  { id: "payments", labelEs: "Pagos y EBT", labelEn: "Payments & EBT", icon: CreditCard },
  { id: "deli", labelEs: "Deli y Comida", labelEn: "Deli & Food", icon: Utensils },
  { id: "hours", labelEs: "Horarios", labelEn: "Store Hours", icon: Clock },
];

const CATEGORIZED_PHRASES = [
  {
    cat: "payments",
    en: "Do you accept EBT / SNAP cards for food?",
    es: "¿Aceptan tarjetas EBT / SNAP para comida?",
  },
  {
    cat: "payments",
    en: "Is there a minimum purchase for credit cards?",
    es: "¿Hay una compra mínima para tarjetas de crédito?",
  },
  {
    cat: "payments",
    en: "Can I pay with cash or debit?",
    es: "¿Puedo pagar con efectivo o tarjeta de débito?",
  },
  {
    cat: "deli",
    en: "I would like 1 pound of ham, sliced thin.",
    es: "Quisiera 1 libra de jamón, cortado fino.",
  },
  {
    cat: "deli",
    en: "Where is the deli counter?",
    es: "¿Dónde está el mostrador del deli?",
  },
  {
    cat: "deli",
    en: "Is this food hot and fresh?",
    es: "¿Esta comida está caliente y fresca?",
  },
  {
    cat: "hours",
    en: "What are your store hours today?",
    es: "¿Cuáles son sus horarios de atención hoy?",
  },
  {
    cat: "hours",
    en: "Are you open on Sundays and holidays?",
    es: "¿Abren los domingos y días festivos?",
  },
  {
    cat: "hours",
    en: "When do you restock fresh bakery items?",
    es: "¿Cuándo reponen los productos de panadería fresca?",
  },
];

export default function TranslatorTab({ lang }: TranslatorTabProps) {
  const [sourceLang, setSourceLang] = useState<"en" | "es">("en");
  const [inputText, setInputText] = useState("");
  const [translatedText, setTranslatedText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [starredPhrases, setStarredPhrases] = useState<string[]>([]);
  const [showCounterDisplay, setShowCounterDisplay] = useState(false);
  const [isFlipped, setIsFlipped] = useState(false);

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

  /* ---------- Star/Unstar Phrase ---------- */
  const toggleStar = (phrase: string) => {
    if (starredPhrases.includes(phrase)) {
      setStarredPhrases(starredPhrases.filter((p) => p !== phrase));
    } else {
      setStarredPhrases([...starredPhrases, phrase]);
    }
  };

  const filteredPhrases = CATEGORIZED_PHRASES.filter(
    (p) => selectedCategory === "all" || p.cat === selectedCategory
  );

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
          rows={3}
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

      {/* OUTPUT TRANSLATION CARD WITH FULL-SCREEN COUNTER DISPLAY BUTTON */}
      <div className="bg-slate-900 text-white rounded-2xl border border-slate-800 shadow-md p-4 space-y-3 relative">
        <div className="flex items-center justify-between text-xs font-black tracking-wider text-blue-400 uppercase">
          <span className="flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-blue-400" />
            <span>{targetLang === "es" ? "Traducción (Español)" : "Translation (English)"}</span>
          </span>

          {translatedText && (
            <div className="flex items-center gap-1.5">
              {/* Full-Screen Show Counter Display Button */}
              <button
                onClick={() => setShowCounterDisplay(true)}
                className="px-2.5 py-1 rounded-lg bg-blue-500/20 text-blue-300 border border-blue-500/40 text-[11px] font-extrabold flex items-center gap-1 hover:bg-blue-500/30 transition-all"
                title="Show giant text on counter display"
              >
                <Tv className="w-3.5 h-3.5 text-blue-400" />
                <span>{lang === "es" ? "Mostrar en Mostrador" : "Show Counter"}</span>
              </button>

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

      {/* CATEGORIZED STORE PHRASES WITH STAR FAVORITES */}
      <div className="space-y-2.5 pt-1">
        <div className="flex items-center justify-between">
          <span className="text-xs font-black text-slate-800 uppercase tracking-wider">
            {lang === "es" ? "Frases Útiles de Comercio" : "Useful Store Phrases"}
          </span>
        </div>

        {/* Category Filter Chips */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar">
          {PHRASE_CATEGORIES.map((cat) => {
            const Icon = cat.icon;
            const isSelected = selectedCategory === cat.id;
            return (
              <button
                key={cat.id}
                onClick={() => setSelectedCategory(cat.id)}
                className={`px-3 py-1.5 rounded-full text-xs font-bold flex items-center gap-1.5 shrink-0 transition-all ${
                  isSelected
                    ? "bg-[#003ec7] text-white shadow-2xs"
                    : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-100"
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{lang === "es" ? cat.labelEs : cat.labelEn}</span>
              </button>
            );
          })}
        </div>

        {/* Preset Phrase Cards */}
        <div className="space-y-1.5 max-h-56 overflow-y-auto pr-0.5">
          {filteredPhrases.map((phrase, idx) => {
            const displayPhrase = sourceLang === "en" ? phrase.en : phrase.es;
            const targetPhrase = sourceLang === "en" ? phrase.es : phrase.en;
            const isStarred = starredPhrases.includes(displayPhrase);

            return (
              <div
                key={idx}
                onClick={() => {
                  setInputText(displayPhrase);
                  setTranslatedText(targetPhrase);
                }}
                className="p-3 bg-white border border-slate-200 rounded-2xl flex items-center justify-between gap-2 hover:border-[#003ec7] cursor-pointer transition-all shadow-2xs group"
              >
                <div className="space-y-0.5 text-left">
                  <div className="text-xs font-extrabold text-slate-900 group-hover:text-[#003ec7] transition-colors">
                    {displayPhrase}
                  </div>
                  <div className="text-[11px] font-medium text-slate-500 italic">
                    {targetPhrase}
                  </div>
                </div>

                <div className="flex items-center gap-1 shrink-0">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      toggleStar(displayPhrase);
                    }}
                    className={`p-1.5 rounded-lg transition-colors ${
                      isStarred ? "text-amber-500 bg-amber-50" : "text-slate-300 hover:text-amber-400"
                    }`}
                  >
                    <Star className="w-4 h-4 fill-current" />
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      speakText(targetPhrase, targetLang);
                    }}
                    className="p-1.5 rounded-lg text-slate-400 hover:text-[#003ec7] hover:bg-blue-50 transition-colors"
                  >
                    <Volume2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* FULL-SCREEN COUNTER DISPLAY MODAL (GIANT TEXT FOR CASHIER/CUSTOMER) */}
      {showCounterDisplay && (
        <div className="fixed inset-0 z-50 bg-slate-950/95 backdrop-blur-xl flex flex-col justify-between p-6 animate-in fade-in zoom-in-95 duration-200">
          {/* Top Bar */}
          <div className="flex items-center justify-between text-white border-b border-white/10 pb-4">
            <div className="flex items-center gap-2">
              <Tv className="w-5 h-5 text-blue-400" />
              <span className="text-xs font-black uppercase tracking-widest text-blue-400">
                {lang === "es" ? "Pantalla de Mostrador" : "Counter Display"}
              </span>
            </div>

            <div className="flex items-center gap-2">
              {/* Flip Orientation 180° */}
              <button
                onClick={() => setIsFlipped(!isFlipped)}
                className={`px-3 py-1.5 rounded-xl text-xs font-extrabold flex items-center gap-1.5 transition-all ${
                  isFlipped
                    ? "bg-amber-400 text-slate-900 ring-2 ring-white"
                    : "bg-white/10 text-white hover:bg-white/20"
                }`}
                title="Flip text 180° for person across counter"
              >
                <RotateCw className="w-3.5 h-3.5" />
                <span>{lang === "es" ? "Girar 180°" : "Flip 180°"}</span>
              </button>

              <button
                onClick={() => setShowCounterDisplay(false)}
                className="p-2 rounded-full bg-white/10 text-white hover:bg-white/20 transition-all"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Main Giant Text Display */}
          <div
            className={`flex-1 flex flex-col items-center justify-center text-center px-4 transition-transform duration-300 ${
              isFlipped ? "rotate-180" : ""
            }`}
          >
            <span className="text-xs font-extrabold text-blue-400 uppercase tracking-widest mb-3">
              {targetLang === "es" ? "Traducción para el Cliente / Cajero:" : "Translation for Customer / Cashier:"}
            </span>

            <div className="text-3xl md:text-5xl font-black text-white leading-tight tracking-wide drop-shadow-md">
              {translatedText || inputText}
            </div>

            {inputText && (
              <div className="text-sm font-semibold text-slate-400 italic mt-6 border-t border-white/10 pt-3 max-w-lg">
                "{inputText}"
              </div>
            )}
          </div>

          {/* Bottom Action Controls */}
          <div className="flex items-center justify-center gap-3 pt-4 border-t border-white/10">
            <button
              onClick={() => speakText(translatedText || inputText, targetLang)}
              className="py-3 px-6 rounded-2xl bg-[#003ec7] text-white font-extrabold text-sm flex items-center gap-2 shadow-lg hover:brightness-110 transition-all"
            >
              <Volume2 className="w-5 h-5" />
              <span>{lang === "es" ? "Escuchar en Voz Alta" : "Speak Out Loud"}</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
