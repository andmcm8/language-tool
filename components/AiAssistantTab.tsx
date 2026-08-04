"use client";

import React, { useState, useRef, useEffect } from "react";
import { MerchantConfig } from "@/types/merchant";
import { Mic, MicOff, Send, Volume2, VolumeX, RefreshCw, ShieldAlert } from "lucide-react";

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
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "msg-0",
      sender: "ai",
      text:
        lang === "es"
          ? `¡Hola! Soy el Asistente Informativo AI de ${merchant.storeInfo.name}. ¿En qué puedo ayudarle hoy?`
          : `Hello! I am the Informational AI Assistant for ${merchant.storeInfo.name}. How can I help you today?`,
    },
  ]);

  const [inputQuery, setInputQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [autoSpeak, setAutoSpeak] = useState(true);
  const recognitionRef = useRef<any>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

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
        rec.onend = () => setIsListening(false);
        recognitionRef.current = rec;
      }
    }
  }, [lang]);

  const toggleListening = () => {
    if (!recognitionRef.current) return;
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      recognitionRef.current.lang = lang === "es" ? "es-US" : "en-US";
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  const speakText = (text: string) => {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang === "es" ? "es-ES" : "en-US";
    utterance.rate = 0.95;
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

    setMessages((prev) => [...prev, userMsg]);
    setInputQuery("");
    setLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: [...messages, userMsg],
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

      if (autoSpeak) speakText(aiReplyText);
    } catch (err) {
      const fallbackMsg: Message = {
        id: `msg-${Date.now() + 1}`,
        sender: "ai",
        text:
          lang === "es"
            ? `Horarios de ${merchant.storeInfo.name}: ${merchant.storeInfo.hours.monday_friday}. Estamos a su servicio.`
            : `Hours for ${merchant.storeInfo.name}: ${merchant.storeInfo.hours.monday_friday}.`,
      };
      setMessages((prev) => [...prev, fallbackMsg]);
      setLoading(false);
      if (autoSpeak) speakText(fallbackMsg.text);
    }
  };

  const quickPrompts = [
    { es: "¿Tiene gluten o alérgenos?", en: "Gluten & allergy info?" },
    { es: "¿Dónde está el baño?", en: "Where is the restroom?" },
    { es: "¿Cuál es la clave del WiFi?", en: "What is the WiFi password?" },
    { es: "¿Aceptan EBT / SNAP?", en: "Do you accept EBT?" },
  ];

  return (
    <div className="w-full max-w-md mx-auto flex flex-col h-[calc(100vh-130px)] p-4 pb-24 space-y-2">
      {/* Controls Bar */}
      <div className="flex items-center justify-between bg-surface p-2.5 rounded-2xl border border-secondary-fixed/50">
        <span className="text-xs font-bold text-on-surface">
          {lang === "es" ? `Asistente AI (${merchant.storeInfo.name})` : `AI Assistant`}
        </span>
        <button
          onClick={() => setAutoSpeak(!autoSpeak)}
          className={`px-2.5 py-1 rounded-full text-[10px] font-bold flex items-center gap-1 transition-all ${
            autoSpeak ? "bg-emerald-100 text-emerald-800" : "bg-surface-container text-on-surface-variant"
          }`}
        >
          {autoSpeak ? <Volume2 className="w-3 h-3" /> : <VolumeX className="w-3 h-3" />}
          <span>{autoSpeak ? "Voz" : "Muted"}</span>
        </button>
      </div>

      {/* Quick Suggestion Chips */}
      <div className="flex items-center gap-1 overflow-x-auto pb-0.5 no-scrollbar">
        {quickPrompts.map((prompt, i) => (
          <button
            key={i}
            onClick={() => sendMessage(lang === "es" ? prompt.es : prompt.en)}
            className="px-2.5 py-1 bg-surface border border-secondary-fixed text-primary text-[10px] font-bold rounded-full shrink-0"
          >
            {lang === "es" ? prompt.es : prompt.en}
          </button>
        ))}
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto space-y-2 pr-0.5">
        {messages.map((msg) => {
          const isAi = msg.sender === "ai";
          return (
            <div key={msg.id} className={`flex flex-col ${isAi ? "items-start" : "items-end"}`}>
              <div
                className={`max-w-[88%] p-3 rounded-2xl text-xs font-medium ${
                  isAi ? "bg-surface border border-secondary-fixed text-on-surface" : "bg-primary text-white"
                }`}
              >
                <span className="whitespace-pre-wrap">{msg.text}</span>
              </div>
            </div>
          );
        })}
        {loading && (
          <div className="flex items-center gap-1.5 text-xs text-on-surface-variant p-2">
            <RefreshCw className="w-3.5 h-3.5 text-primary animate-spin" />
            <span>Consultando datos...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Permanent Legal & Health Liability Disclaimer Bar */}
      <div className="flex items-center justify-center gap-1 px-2 py-1 bg-amber-500/10 rounded-xl text-[9px] font-semibold text-amber-800 dark:text-amber-300 text-center">
        <ShieldAlert className="w-3 h-3 text-amber-600 shrink-0" />
        <span>
          {lang === "es"
            ? "Respuestas informativas. Verifique alergias o salud con el personal de la tienda."
            : "Informational only. Always verify allergies or health details with store staff."}
        </span>
      </div>

      {/* Input Row */}
      <div className="bg-surface p-2 rounded-2xl border border-secondary-fixed/50 flex items-center gap-1.5 shadow-md">
        <button
          onClick={toggleListening}
          className={`w-9 h-9 rounded-xl flex items-center justify-center transition-all ${
            isListening ? "bg-rose-500 text-white animate-pulse" : "bg-secondary-fixed text-primary"
          }`}
        >
          {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
        </button>
        <input
          type="text"
          value={inputQuery}
          onChange={(e) => setInputQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder={lang === "es" ? "Pregunte sobre alérgenos, baño, WiFi..." : "Ask about allergens, WiFi, restroom..."}
          className="flex-1 bg-surface-container-lowest border border-outline-variant/30 rounded-xl px-3 py-2 text-xs text-on-surface focus:outline-hidden"
        />
        <button
          onClick={() => sendMessage()}
          disabled={!inputQuery.trim() || loading}
          className="w-9 h-9 rounded-xl bg-primary text-white flex items-center justify-center disabled:opacity-40"
        >
          <Send className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
}
