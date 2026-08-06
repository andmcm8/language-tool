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
        ? `¡Hola! Soy el Asistente AI de ${merchant.storeInfo.name}. ¿En qué puedo ayudarle hoy?`
        : `Hello! I am the AI Assistant for ${merchant.storeInfo.name}. How can I help you today?`,
  };

  const [activeMode, setActiveMode] = useState<"chat" | "voice">("chat");
  const [messages, setMessages] = useState<Message[]>(() => {
    if (typeof window !== "undefined") {
      try {
        const saved = localStorage.getItem(storageKey);
        if (saved) {
          const parsed = JSON.parse(saved);
          if (Array.isArray(parsed) && parsed.length > 0) {
            return parsed.map((m: Message) => ({
              ...m,
              text: m.text
                ? m.text
                    .replace(/El Sol Market & Deli/gi, merchant.storeInfo.name)
                    .replace(/El Sol Market/gi, merchant.storeInfo.name)
                    .replace(/El Sol/gi, merchant.storeInfo.name)
                    .replace(/Demo Store/gi, merchant.storeInfo.name)
                : m.text,
            }));
          }
        }
      } catch (e) {
        console.warn("Failed to load chat history:", e);
      }
    }
    return [defaultInitialMessage];
  });

  const [inputQuery, setInputQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [autoSpeak, setAutoSpeak] = useState(true);
  const recognitionRef = useRef<any>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Sync chat history to localStorage whenever messages change
  useEffect(() => {
    if (typeof window !== "undefined" && messages.length > 0) {
      try {
        localStorage.setItem(storageKey, JSON.stringify(messages));
      } catch (e) {
        console.warn("Failed to save chat history:", e);
      }
    }
  }, [messages, storageKey]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
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
            ? `Horarios de ${merchant.storeInfo.name}: ${merchant.storeInfo.hours.monday_friday}.`
            : `Hours for ${merchant.storeInfo.name}: ${merchant.storeInfo.hours.monday_friday}.`,
      };
      setMessages((prev) => [...prev, fallbackMsg]);
      setLoading(false);
      if (autoSpeak || activeMode === "voice") {
        speakText(fallbackMsg.text);
      }
    }
  };

  const quickPrompts = [
    { es: "¿Dónde está el baño?", en: "Where is the restroom?" },
    { es: "¿Cuál es la clave del WiFi?", en: "What is the WiFi password?" },
    { es: "¿Tienen opciones sin gluten?", en: "Are there gluten free items?" },
    { es: "¿Aceptan EBT / SNAP?", en: "Do you accept EBT?" },
  ];

  const lastAiMessage = messages.filter((m) => m.sender === "ai").slice(-1)[0]?.text || defaultInitialMessage.text;
  const lastUserMessage = messages.filter((m) => m.sender === "user").slice(-1)[0]?.text;

  return (
    <div className="w-full max-w-md mx-auto flex-1 flex flex-col h-[calc(100dvh-125px)] p-3 pb-20 space-y-2.5">
      {/* Top Bar: Mode Switcher (Voice Mode vs Chat Mode) */}
      <div className="flex items-center justify-between bg-white p-1.5 rounded-2xl border border-slate-200 shadow-xs">
        <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl">
          <button
            onClick={() => setActiveMode("chat")}
            className={`px-3 py-1 rounded-lg text-xs font-black flex items-center gap-1.5 transition-all ${
              activeMode === "chat"
                ? "bg-[#003ec7] text-white shadow-2xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            <MessageSquare className="w-3.5 h-3.5" />
            <span>{lang === "es" ? "Chat" : "Text Chat"}</span>
          </button>

          <button
            onClick={() => setActiveMode("voice")}
            className={`px-3 py-1 rounded-lg text-xs font-black flex items-center gap-1.5 transition-all ${
              activeMode === "voice"
                ? "bg-[#003ec7] text-white shadow-2xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            <Radio className="w-3.5 h-3.5" />
            <span>{lang === "es" ? "Voz AI" : "Voice AI"}</span>
          </button>
        </div>

        <div className="flex items-center gap-1">
          <button
            onClick={clearChatHistory}
            className="p-1.5 rounded-xl text-slate-400 hover:text-rose-500 hover:bg-slate-100 transition-colors"
            title="Clear Chat History"
          >
            <Trash2 className="w-4 h-4" />
          </button>

          <button
            onClick={toggleAutoSpeak}
            className={`p-1.5 rounded-xl transition-all ${
              autoSpeak ? "text-[#003ec7] bg-blue-50" : "text-slate-400 hover:bg-slate-100"
            }`}
            title={autoSpeak ? "Mute Voice Output" : "Enable Voice Output"}
          >
            {autoSpeak ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* VIEW MODE 1: VOICE-FIRST INTERACTIVE ASSISTANT (MICROPHONE SPHERE & SOUNDWAVES) */}
      {activeMode === "voice" ? (
        <div className="flex-1 flex flex-col justify-between bg-white rounded-3xl p-5 border border-slate-200 shadow-sm relative overflow-hidden text-center space-y-4">
          {/* Header Status Badge */}
          <div className="flex items-center justify-center gap-2">
            <span className="flex items-center gap-1.5 text-xs font-black text-[#003ec7] bg-blue-50 px-3 py-1 rounded-full border border-blue-100">
              <Sparkles className="w-3.5 h-3.5 text-[#003ec7]" />
              {isListening
                ? lang === "es" ? "Escuchando voz..." : "Listening to voice..."
                : loading
                ? lang === "es" ? "Procesando respuesta..." : "Generating answer..."
                : isSpeaking
                ? lang === "es" ? "Hablando respuesta..." : "Speaking response..."
                : lang === "es" ? "Asistente de Voz Listo" : "Voice Assistant Ready"}
            </span>
          </div>

          {/* Dynamic Spoken Conversation Display (Streamlined & Compact) */}
          <div className="space-y-2 flex-1 flex flex-col justify-center max-w-xs mx-auto my-auto">
            {lastUserMessage && (
              <div className="p-2 bg-slate-50 rounded-2xl border border-slate-100 text-xs font-medium text-slate-600 animate-in fade-in duration-200">
                <span className="text-[9px] uppercase font-bold text-slate-400 block">
                  {lang === "es" ? "Usted dijo:" : "You said:"}
                </span>
                "{lastUserMessage}"
              </div>
            )}

            <div className="p-3 bg-blue-50/70 rounded-2xl border border-blue-100 text-xs font-bold text-slate-800 leading-snug shadow-2xs">
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
              <div className="absolute w-36 h-36 rounded-full border-4 border-dashed border-[#003ec7] animate-spin pointer-events-none" />
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
                  : "bg-[#003ec7] text-white hover:bg-blue-700 shadow-blue-200 hover:scale-105"
              }`}
            >
              {loading ? (
                <RefreshCw className="w-10 h-10 animate-spin" />
              ) : isListening ? (
                <MicOff className="w-10 h-10 animate-pulse" />
              ) : (
                <Mic className="w-10 h-10" />
              )}

              <span className="text-[10px] font-black uppercase tracking-wider mt-1">
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
        <div className="flex-1 flex flex-col justify-between space-y-2 overflow-hidden">
          {/* Quick Suggestion Chips */}
          <div className="flex items-center gap-1 overflow-x-auto pb-0.5 no-scrollbar">
            {quickPrompts.map((prompt, i) => (
              <button
                key={i}
                onClick={() => sendMessage(lang === "es" ? prompt.es : prompt.en)}
                className="px-2.5 py-1 bg-white border border-slate-200 hover:bg-blue-50 text-[#003ec7] text-[10px] font-extrabold rounded-full shrink-0 shadow-2xs"
              >
                {lang === "es" ? prompt.es : prompt.en}
              </button>
            ))}
          </div>

          {/* Chat Messages Thread */}
          <div className="flex-1 overflow-y-auto space-y-2 pr-0.5">
            {messages.map((msg) => {
              const isAi = msg.sender === "ai";
              return (
                <div key={msg.id} className={`flex flex-col ${isAi ? "items-start" : "items-end"}`}>
                  <div
                    className={`max-w-[88%] p-3 rounded-2xl text-xs font-medium leading-relaxed ${
                      isAi
                        ? "bg-white border border-slate-200 text-slate-800 shadow-2xs"
                        : "bg-[#003ec7] text-white shadow-xs"
                    }`}
                  >
                    <span className="whitespace-pre-wrap">{msg.text}</span>
                  </div>
                </div>
              );
            })}
            {loading && (
              <div className="flex items-center gap-1.5 text-xs text-slate-500 p-2">
                <RefreshCw className="w-3.5 h-3.5 text-[#003ec7] animate-spin" />
                <span>{lang === "es" ? "Consultando información..." : "Searching store details..."}</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Row */}
          <div className="bg-white p-2 rounded-2xl border border-slate-200 flex items-center gap-1.5 shadow-md">
            <button
              onClick={toggleListening}
              className={`w-9 h-9 rounded-xl flex items-center justify-center transition-all ${
                isListening ? "bg-rose-600 text-white animate-pulse" : "bg-blue-50 text-[#003ec7]"
              }`}
              title="Voice Input / Hablar"
            >
              {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
            </button>
            <input
              type="text"
              value={inputQuery}
              onChange={(e) => setInputQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              placeholder={lang === "es" ? "Pregunte sobre alérgenos, baño, WiFi..." : "Ask about allergens, WiFi, restroom..."}
              className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-900 focus:outline-none focus:ring-1 focus:ring-[#003ec7]"
            />
            <button
              onClick={() => sendMessage()}
              disabled={!inputQuery.trim() || loading}
              className="w-9 h-9 rounded-xl bg-[#003ec7] text-white flex items-center justify-center disabled:opacity-40 hover:brightness-110 transition-all"
            >
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}

      {/* Permanent Legal Disclaimer Bar */}
      <div className="flex items-center justify-center gap-1 px-2 py-1 bg-amber-50 rounded-xl border border-amber-100 text-[9px] font-semibold text-amber-800 text-center shrink-0">
        <ShieldAlert className="w-3 h-3 text-amber-600 shrink-0" />
        <span>
          {lang === "es"
            ? "Respuestas informativas. Verifique alergias o salud con el personal de la tienda."
            : "Informational only. Always verify allergies or health details with store staff."}
        </span>
      </div>
    </div>
  );
}
