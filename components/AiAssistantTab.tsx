"use client";

import React, { useState, useRef, useEffect } from "react";
import { MerchantConfig } from "@/types/merchant";
import {
  Mic,
  MicOff,
  Send,
  Volume2,
  VolumeX,
  RefreshCw,
  ShieldAlert,
  Trash2,
  MessageSquare,
  Sparkles,
  Radio
} from "lucide-react";

interface AiAssistantTabProps {
  merchant: MerchantConfig;
  lang: "es" | "en";
}

interface Message {
  id: string;
  sender: "user" | "ai";
  text: string;
}

export default function AiAssistantTab({ merchant, lang }: AiAssistantTabProps) {
  const storageKey = `chat_history_${merchant.storeInfo.id}`;

  const defaultInitialMessage: Message = {
    id: "msg-0",
    sender: "ai",
    text:
      lang === "es"
        ? `¡Hola! Soy el Asistente IA de ${merchant.storeInfo.name}. ¿En qué puedo ayudarle hoy?`
        : `Hello! I am the AI Assistant for ${merchant.storeInfo.name}. How can I help you today?`,
  };

  const [activeMode, setActiveMode] = useState<"chat" | "voice">("chat");
  // Start from the welcome state on both server and client (reading localStorage during the
  // first render caused a hydration mismatch); restore saved history right after mount.
  const [messages, setMessages] = useState<Message[]>([defaultInitialMessage]);
  const [historyLoaded, setHistoryLoaded] = useState(false);

  useEffect(() => {
    try {
      const saved = localStorage.getItem(storageKey);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) {
          setMessages(
            parsed.map((m: Message) => ({
              ...m,
              text: m.text
                ? m.text
                    .replace(/El Sol Market & Deli/gi, merchant.storeInfo.name)
                    .replace(/El Sol Market/gi, merchant.storeInfo.name)
                    .replace(/El Sol/gi, merchant.storeInfo.name)
                    .replace(/Demo Store/gi, merchant.storeInfo.name)
                : m.text,
            }))
          );
        }
      }
    } catch (e) {
      console.warn("Failed to load chat history:", e);
    }
    setHistoryLoaded(true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [storageKey]);

  const [inputQuery, setInputQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [autoSpeak, setAutoSpeak] = useState(false);
  const recognitionRef = useRef<any>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const threadRef = useRef<HTMLDivElement | null>(null);

  // Sync chat history to localStorage whenever messages change
  useEffect(() => {
    if (historyLoaded && typeof window !== "undefined" && messages.length > 0) {
      try {
        localStorage.setItem(storageKey, JSON.stringify(messages));
      } catch (e) {
        console.warn("Failed to save chat history:", e);
      }
    }
  }, [messages, storageKey, historyLoaded]);

  useEffect(() => {
    // Scroll only the thread (never the page), and not on the initial welcome state.
    const el = threadRef.current;
    if (el && (messages.length > 1 || loading)) el.scrollTo({ top: el.scrollHeight, behavior: "smooth" });
  }, [messages, loading, activeMode]);

  // Setup Web Speech Recognition API
  useEffect(() => {
    if (typeof window !== "undefined") {
      const SpeechRecognition =
        (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (SpeechRecognition) {
        const rec = new SpeechRecognition();
        rec.continuous = false;
        rec.interimResults = false;
        rec.lang = lang === "es" ? "es-US" : "en-US";

        rec.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript;
          if (transcript) {
            setInputQuery(transcript);
            sendMessage(transcript);
          }
          setIsListening(false);
        };

        rec.onerror = () => {
          setIsListening(false);
        };

        rec.onend = () => {
          setIsListening(false);
        };

        recognitionRef.current = rec;
      }
    }
  }, [lang]);

  const toggleListening = () => {
    if (!recognitionRef.current) {
      alert(
        lang === "es"
          ? "El reconocimiento de voz no está disponible en este navegador. Use la entrada de texto."
          : "Voice recognition is not supported in this browser. Please use text input."
      );
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      if (typeof window !== "undefined" && "speechSynthesis" in window) {
        window.speechSynthesis.cancel();
        setIsSpeaking(false);
      }
      recognitionRef.current.lang = lang === "es" ? "es-US" : "en-US";
      try {
        recognitionRef.current.start();
        setIsListening(true);
      } catch (e) {
        console.warn("Recognition start error:", e);
        setIsListening(false);
      }
    }
  };

  const toggleAutoSpeak = () => {
    const nextState = !autoSpeak;
    setAutoSpeak(nextState);
    if (!nextState && typeof window !== "undefined" && "speechSynthesis" in window) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  };

  const clearChatHistory = () => {
    setMessages([defaultInitialMessage]);
    if (typeof window !== "undefined") {
      try {
        localStorage.removeItem(storageKey);
        if ("speechSynthesis" in window) {
          window.speechSynthesis.cancel();
          setIsSpeaking(false);
        }
      } catch (e) {}
    }
  };

  const speakText = (text: string) => {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    const isEnglishText = /\b(the|is|are|you|have|where|when|what|hours|restroom|bathroom|wifi|welcome|safety|note|disclaimer|for|that|specific)\b/i.test(
      text
    );
    utterance.lang = isEnglishText ? "en-US" : "es-ES";
    utterance.rate = 0.95;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
  };

  const sendMessage = async (customText?: string) => {
    const textToSend = customText || inputQuery;
    if (!textToSend.trim() || loading) return;

    const userMsg: Message = {
      id: `msg-${Date.now()}`,
      sender: "user",
      text: textToSend,
    };

    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setInputQuery("");
    setLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: updatedMessages.map((m) => ({
            sender: m.sender,
            text: m.text,
            content: m.text,
          })),
          lang,
          merchantId: merchant.storeInfo.id,
        }),
      });

      const data = await res.json();
      const aiReplyText = data.reply || (lang === "es" ? "Lo siento, intente de nuevo." : "Sorry, try again.");

      const aiMsg: Message = {
        id: `msg-${Date.now() + 1}`,
        sender: "ai",
        text: aiReplyText,
      };

      setMessages((prev) => [...prev, aiMsg]);
      setLoading(false);

      if (autoSpeak || activeMode === "voice") {
        speakText(aiReplyText);
      }
    } catch (err) {
      console.error("Chat API error:", err);
      const fallbackMsg: Message = {
        id: `msg-${Date.now() + 1}`,
        sender: "ai",
        text:
          lang === "es"
            ? `Horarios de ${merchant.storeInfo.name}: ${merchant.storeInfo.hours.monday_friday}. Estamos ubicados en ${merchant.storeInfo.address}.`
            : `Hours for ${merchant.storeInfo.name}: ${merchant.storeInfo.hours.monday_friday}. Located at ${merchant.storeInfo.address}.`,
      };
      setMessages((prev) => [...prev, fallbackMsg]);
      setLoading(false);
      if (autoSpeak || activeMode === "voice") {
        speakText(fallbackMsg.text);
      }
    }
  };

  const hasGlutenOrVegan = (merchant.products || []).some((p) => {
    const tags = (p.tags || []).join(" ").toLowerCase();
    const desc = `${p.descriptionEn} ${p.descriptionEs}`.toLowerCase();
    return tags.includes("gluten") || tags.includes("vegan") || desc.includes("gluten") || desc.includes("vegan");
  });

  const quickPrompts = [
    { es: "¿Cuáles son sus horarios?", en: "What are your hours?" },
    { es: "¿Dónde están ubicados?", en: "Where are you located?" },
    {
      es: merchant.storeInfo.phone ? "¿Cuál es su teléfono?" : "¿Cómo contactarlos?",
      en: merchant.storeInfo.phone ? "What is your phone number?" : "How to contact you?",
    },
    { es: "¿Qué recomiendan del menú?", en: "What do you recommend?" },
    hasGlutenOrVegan
      ? { es: "¿Tienen opciones sin gluten o veganas?", en: "Are there vegan or gluten-free options?" }
      : { es: "¿Qué métodos de pago aceptan?", en: "What payment methods do you take?" },
  ];

  const lastAiMessage = messages.filter((m) => m.sender === "ai").slice(-1)[0]?.text || defaultInitialMessage.text;
  const lastUserMessage = messages.filter((m) => m.sender === "user").slice(-1)[0]?.text;

  return (
    <div className="w-full max-w-md lg:max-w-3xl mx-auto shrink-0 flex flex-col h-[calc(100dvh-72px)] lg:h-screen px-4 lg:px-8 pt-4 lg:pt-8 pb-24 lg:pb-8 gap-3">
      {/* Top Bar: Mode Switcher (Voice Mode vs Chat Mode) */}
      <div className="flex items-center justify-between bg-white p-1.5 rounded-full border border-white shadow-soft">
        <div className="flex items-center gap-1">
          <button
            onClick={() => setActiveMode("chat")}
            className={`px-4 h-10 rounded-full text-[13px] font-bold flex items-center gap-1.5 transition-all ${
              activeMode === "chat"
                ? "bg-brand-gradient text-white shadow-brand"
                : "text-on-surface-variant hover:text-on-surface"
            }`}
          >
            <MessageSquare className="w-3.5 h-3.5" />
            <span>{lang === "es" ? "Chat" : "Text Chat"}</span>
          </button>

          <button
            onClick={() => setActiveMode("voice")}
            className={`px-4 h-10 rounded-full text-[13px] font-bold flex items-center gap-1.5 transition-all ${
              activeMode === "voice"
                ? "bg-brand-gradient text-white shadow-brand"
                : "text-on-surface-variant hover:text-on-surface"
            }`}
          >
            <Radio className="w-3.5 h-3.5" />
            <span>{lang === "es" ? "Voz IA" : "Voice AI"}</span>
          </button>
        </div>

        <div className="flex items-center gap-1">
          <button
            onClick={clearChatHistory}
            className="w-10 h-10 grid place-items-center rounded-full text-on-surface-variant hover:text-rose-500 hover:bg-surface-container transition-colors"
            title="Clear Chat History"
          >
            <Trash2 className="w-4 h-4" />
          </button>

          <button
            onClick={toggleAutoSpeak}
            className={`w-10 h-10 grid place-items-center rounded-full transition-all ${
              autoSpeak ? "text-primary bg-primary-fixed" : "text-on-surface-variant hover:bg-surface-container"
            }`}
            title={autoSpeak ? "Mute Voice Output" : "Enable Voice Output"}
          >
            {autoSpeak ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* VIEW MODE 1: VOICE-FIRST INTERACTIVE ASSISTANT (MICROPHONE SPHERE & SOUNDWAVES) */}
      {activeMode === "voice" ? (
        <div className="flex-1 flex flex-col justify-between bg-white rounded-[32px] p-6 border border-white shadow-soft relative overflow-hidden text-center space-y-4">
          {/* Status */}
          <p className="flex items-center justify-center gap-2 text-[13px] font-semibold text-on-surface-variant">
            <span
              className={`h-2 w-2 rounded-full ${
                isListening ? "bg-rose-500 animate-pulse" : loading ? "bg-primary animate-pulse" : isSpeaking ? "bg-emerald-500 animate-pulse" : "bg-emerald-500"
              }`}
            />
            {isListening
              ? lang === "es" ? "Escuchando" : "Listening"
              : loading
              ? lang === "es" ? "Pensando" : "Thinking"
              : isSpeaking
              ? lang === "es" ? "Hablando" : "Speaking"
              : lang === "es" ? "Listo para escuchar" : "Ready to listen"}
          </p>

          {/* Dynamic Spoken Conversation Display (Streamlined & Compact) */}
          <div className="space-y-2 flex-1 flex flex-col justify-center max-w-xs mx-auto my-auto">
            {lastUserMessage && (
              <div className="p-3 bg-surface-container-low rounded-2xl text-[13px] font-medium text-on-surface-variant line-clamp-3 animate-in fade-in duration-200">
                <span className="text-[11px] uppercase tracking-wider font-bold text-on-surface-variant/70 block mb-0.5">
                  {lang === "es" ? "Usted dijo:" : "You said:"}
                </span>
                "{lastUserMessage}"
              </div>
            )}

            <div className="p-4 bg-primary-fixed/60 rounded-2xl text-[14px] font-semibold text-on-surface leading-snug line-clamp-5">
              {lastAiMessage}
            </div>
          </div>

          {/* CENTRAL INTERACTIVE ANIMATED MICROPHONE SPHERE & AUDIO SOUNDWAVES */}
          <div className="flex flex-col items-center justify-center py-2 relative my-auto">
            {/* Outer Glowing Pulsating Audio Rings when Listening */}
            {isListening && (
              <>
                <div className="absolute w-36 h-36 rounded-full bg-rose-500/20 animate-ping pointer-events-none" />
                <div className="absolute w-44 h-44 rounded-full bg-blue-500/10 animate-pulse pointer-events-none" />
              </>
            )}

            {/* Glowing Ring when Speaking */}
            {isSpeaking && (
              <div className="absolute w-36 h-36 rounded-full bg-emerald-500/20 animate-pulse pointer-events-none" />
            )}

            {/* Glowing Ring when Thinking */}
            {loading && (
              <div className="absolute w-36 h-36 rounded-full border-4 border-dashed border-[#0A5CFF] animate-spin pointer-events-none" />
            )}

            {/* Main Central Microphone Button Sphere */}
            <button
              onClick={toggleListening}
              className={`relative z-10 w-28 h-28 rounded-full flex flex-col items-center justify-center shadow-xl transition-all active:scale-95 ${
                isListening
                  ? "bg-rose-600 text-white shadow-rose-200 scale-105"
                  : loading
                  ? "bg-blue-600 text-white shadow-blue-200"
                  : isSpeaking
                  ? "bg-emerald-600 text-white shadow-emerald-200"
                  : "bg-[#0A5CFF] text-white hover:bg-blue-700 shadow-blue-200 hover:scale-105"
              }`}
            >
              {loading ? (
                <RefreshCw className="w-10 h-10 animate-spin" />
              ) : isListening ? (
                <MicOff className="w-10 h-10 animate-pulse" />
              ) : (
                <Mic className="w-10 h-10" />
              )}

              <span className="text-[11px] font-bold uppercase tracking-wider mt-1">
                {isListening
                  ? lang === "es" ? "Detener" : "Stop"
                  : loading
                  ? lang === "es" ? "Pensando" : "Thinking"
                  : isSpeaking
                  ? lang === "es" ? "Hablando" : "Speaking"
                  : lang === "es" ? "Hablar" : "Speak"}
              </span>
            </button>

            {/* Animated Equalizer Sound Bars */}
            <div className="flex items-center gap-1 mt-4 h-6">
              {[0, 1, 2, 3, 4, 5, 6].map((idx) => {
                const isActive = isListening || isSpeaking;
                return (
                  <div
                    key={idx}
                    className={`w-1 rounded-full transition-all duration-300 ${
                      isListening
                        ? "bg-rose-500 animate-bounce"
                        : isSpeaking
                        ? "bg-emerald-500 animate-pulse"
                        : "bg-slate-300 h-2"
                    }`}
                    style={{
                      height: isActive ? `${Math.floor(Math.random() * 18) + 8}px` : "6px",
                      animationDelay: `${idx * 120}ms`,
                    }}
                  />
                );
              })}
            </div>

            <p className="text-[11px] font-bold text-slate-500 mt-2">
              {isListening
                ? lang === "es" ? "Escuchando... Hable ahora" : "Listening... Speak now"
                : isSpeaking
                ? lang === "es" ? "Reproduciendo respuesta" : "Playing audio answer"
                : lang === "es" ? "Presione el micrófono para hablar" : "Tap microphone to speak"}
            </p>
          </div>
        </div>
      ) : (
        /* VIEW MODE 2: TRADITIONAL CHAT THREAD WITH TEXT INPUT */
        <div className="flex-1 flex flex-col gap-3 min-h-0">
          {/* Chat thread (welcome state until the guest asks something) */}
          <div ref={threadRef} className="flex-1 min-h-0 overflow-y-auto space-y-3 pr-0.5">
            {messages.length <= 1 && !loading ? (
              <div className="pt-4 pb-2">
                <span className="grid h-14 w-14 place-items-center rounded-2xl bg-brand-gradient text-white shadow-brand">
                  <Sparkles className="h-7 w-7" />
                </span>
                <h2 className="mt-4 text-[26px] font-extrabold leading-tight text-on-surface">
                  {lang === "es" ? `Pregúntame sobre ${merchant.storeInfo.name}` : `Ask me about ${merchant.storeInfo.name}`}
                </h2>
                <p className="mt-1.5 text-sm leading-relaxed text-on-surface-variant">
                  {lang === "es"
                    ? "Platillos, ingredientes, horarios y más, en español o inglés."
                    : "Dishes, ingredients, hours and more, in Spanish or English."}
                </p>
                <div className="mt-5 flex flex-col gap-2">
                  {quickPrompts.slice(0, 4).map((prompt, i) => (
                    <button
                      key={i}
                      onClick={() => sendMessage(lang === "es" ? prompt.es : prompt.en)}
                      className="flex items-center justify-between gap-3 rounded-2xl bg-white px-4 py-3.5 text-left text-[14px] font-semibold text-on-surface shadow-soft border border-white hover:shadow-lift active:scale-[0.99] transition-all"
                    >
                      <span>{lang === "es" ? prompt.es : prompt.en}</span>
                      <Send className="h-4 w-4 shrink-0 text-primary" />
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              messages.map((msg) => {
                const isAi = msg.sender === "ai";
                return (
                  <div key={msg.id} className={`flex flex-col ${isAi ? "items-start" : "items-end"}`}>
                    <div
                      className={`max-w-[86%] px-4 py-3 text-[14px] leading-relaxed ${
                        isAi
                          ? "bg-white text-on-surface shadow-soft border border-white rounded-[22px] rounded-bl-md"
                          : "bg-brand-gradient text-white shadow-brand rounded-[22px] rounded-br-md"
                      }`}
                    >
                      <span className="whitespace-pre-wrap">{msg.text}</span>
                    </div>
                  </div>
                );
              })
            )}
            {loading && (
              <div className="flex items-center gap-2 px-2 text-[13px] font-medium text-on-surface-variant">
                <RefreshCw className="h-3.5 w-3.5 animate-spin text-primary" />
                <span>{lang === "es" ? "Pensando..." : "Thinking..."}</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Quick prompts once a conversation has started */}
          {messages.length > 1 && (
            <div className="flex items-center gap-2 overflow-x-auto pb-0.5">
              {quickPrompts.map((prompt, i) => (
                <button
                  key={i}
                  onClick={() => sendMessage(lang === "es" ? prompt.es : prompt.en)}
                  className="chip shrink-0 bg-white text-primary border border-white shadow-soft"
                >
                  {lang === "es" ? prompt.es : prompt.en}
                </button>
              ))}
            </div>
          )}

          {/* Input */}
          <div className="flex items-center gap-2 rounded-full bg-white p-1.5 pl-1.5 shadow-lift border border-white">
            <button
              onClick={toggleListening}
              aria-label="Voice input"
              className={`grid h-11 w-11 shrink-0 place-items-center rounded-full transition-all ${
                isListening ? "bg-rose-600 text-white animate-pulse" : "bg-primary-fixed text-primary"
              }`}
            >
              {isListening ? <MicOff className="h-[18px] w-[18px]" /> : <Mic className="h-[18px] w-[18px]" />}
            </button>
            <input
              type="text"
              value={inputQuery}
              onChange={(e) => setInputQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              placeholder={lang === "es" ? "Escribe tu pregunta..." : "Type your question..."}
              className="min-w-0 flex-1 bg-transparent px-1 text-[15px] font-medium text-on-surface placeholder:text-on-surface-variant/60 focus:outline-none"
            />
            <button
              onClick={() => sendMessage()}
              disabled={!inputQuery.trim() || loading}
              aria-label="Send"
              className="grid h-11 w-11 shrink-0 place-items-center rounded-full bg-brand-gradient text-white shadow-brand transition active:scale-95 disabled:opacity-40 disabled:shadow-none"
            >
              <Send className="h-[18px] w-[18px]" />
            </button>
          </div>
        </div>
      )}

      {/* Disclaimer */}
      <p className="flex shrink-0 items-center justify-center gap-1.5 px-3 text-center text-[11.5px] font-medium leading-snug text-on-surface-variant/80">
        <ShieldAlert className="h-3.5 w-3.5 shrink-0" />
        {lang === "es"
          ? "Respuestas informativas. Confirma alergias con el personal."
          : "Informational only. Confirm allergies with staff."}
      </p>
    </div>
  );
}
