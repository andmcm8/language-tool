"use client";

import React, { useState } from "react";
import Link from "next/link";
import { MerchantConfig } from "@/types/merchant";
import { isValidPhone } from "@/lib/phone";
import { townFromAddress } from "@/lib/place";
import { useRouter } from "next/navigation";
import {
  Store,
  MapPin,
  Clock,
  Phone,
  X,
  CreditCard,
  Info,
  ChevronDown,
  Building2,
  HeartPulse,
  Smartphone,
  Check,
  Mail,
  Copy,
  Send,
  ExternalLink,
  Loader2,
  ChevronLeft
} from "lucide-react";

interface HeaderProps {
  merchant: MerchantConfig;
  lang: "es" | "en";
  setLang: (lang: "es" | "en") => void;
}

export default function Header({ merchant, lang, setLang }: HeaderProps) {
  const router = useRouter();
  const [showInfoModal, setShowInfoModal] = useState(false);
  const [showClaimModal, setShowClaimModal] = useState(false);
  const [showMerchantMenu, setShowMerchantMenu] = useState(false);
  const [copiedEmail, setCopiedEmail] = useState(false);
  const [contactInput, setContactInput] = useState("");
  const [messageInput, setMessageInput] = useState("");
  const [isSubmittingContact, setIsSubmittingContact] = useState(false);
  const [contactSubmitted, setContactSubmitted] = useState(false);
  const { storeInfo } = merchant;
  const town = townFromAddress(storeInfo.address);

  const handleCopyEmail = () => {
    navigator.clipboard.writeText("contact@duotaps.com");
    setCopiedEmail(true);
    setTimeout(() => setCopiedEmail(false), 2500);
  };

  const handleSendContact = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!contactInput.trim()) return;

    setIsSubmittingContact(true);
    try {
      await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          placeName: storeInfo.name,
          placeId: storeInfo.id,
          contactInfo: contactInput.trim(),
          message: messageInput.trim(),
        }),
      });
      setContactSubmitted(true);
      setContactInput("");
      setMessageInput("");
    } catch {
      setContactSubmitted(true);
    } finally {
      setIsSubmittingContact(false);
    }
  };

  const getLogoIcon = (iconName?: string) => {
    switch (iconName) {
      case "HeartPulse":
        return <HeartPulse className="w-5 h-5 text-white" />;
      case "Smartphone":
        return <Smartphone className="w-5 h-5 text-white" />;
      default:
        return <Store className="w-5 h-5 text-white" />;
    }
  };

  return (
    <>
      <header className="sticky top-0 z-30 glass border-x-0 border-t-0 border-b border-white/60 shadow-[0_1px_0_rgba(11,27,51,0.04)]">
        <div className="max-w-md mx-auto px-4 py-3 flex items-center justify-between gap-3">
          {/* Left: back to directory + place identity */}
          <div className="flex items-center gap-3 min-w-0">
            <Link
              href="/"
              aria-label={lang === "es" ? "Volver al directorio" : "Back to directory"}
              className="w-10 h-10 shrink-0 rounded-full bg-white shadow-soft border border-white flex items-center justify-center text-on-surface hover:text-primary transition-colors"
            >
              <ChevronLeft className="w-5 h-5" strokeWidth={2.4} />
            </Link>
            <div className="min-w-0">
              <h1 className="font-extrabold text-[17px] text-on-surface tracking-tight leading-tight truncate">
                {storeInfo.name}
              </h1>
              {town && (
                <p className="mt-0.5 flex items-center gap-1 text-xs text-on-surface-variant font-medium truncate">
                  <MapPin className="w-3 h-3 shrink-0" />
                  <span className="truncate">{town}</span>
                </p>
              )}
            </div>
          </div>

          {/* Right: language + info */}
          <div className="flex items-center gap-2 shrink-0">
            <div className="flex items-center p-1 rounded-full bg-white shadow-soft border border-white">
              {(["es", "en"] as const).map((code) => (
                <button
                  key={code}
                  onClick={() => setLang(code)}
                  aria-pressed={lang === code}
                  className={`px-3 h-8 rounded-full text-xs font-bold transition-all ${
                    lang === code ? "bg-brand-gradient text-white shadow-brand" : "text-on-surface-variant hover:text-on-surface"
                  }`}
                >
                  {code.toUpperCase()}
                </button>
              ))}
            </div>
            <button
              onClick={() => setShowInfoModal(true)}
              aria-label={lang === "es" ? "Información del lugar" : "Place info"}
              className="w-10 h-10 rounded-full bg-white shadow-soft border border-white flex items-center justify-center text-on-surface-variant hover:text-primary transition-colors"
            >
              <Info className="w-[18px] h-[18px]" />
            </button>
          </div>
        </div>
      </header>

      {/* Merchant Info Modal */}
      {showInfoModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs animate-in fade-in duration-200">
          <div className="bg-white rounded-[28px] max-w-xs w-full p-6 shadow-float border border-white relative overflow-hidden animate-in zoom-in-95 duration-200">
            <button
              onClick={() => setShowInfoModal(false)}
              className="absolute top-3.5 right-3.5 p-1.5 rounded-full bg-surface-container text-on-surface-variant hover:text-on-surface transition-all"
            >
              <X className="w-4 h-4" />
            </button>

            <div className="flex items-center gap-2.5 mb-4">
              <div
                className="w-10 h-10 rounded-2xl text-white flex items-center justify-center font-bold"
                style={{ backgroundColor: storeInfo.themeColor || "#0A5CFF" }}
              >
                {getLogoIcon(storeInfo.logoIcon)}
              </div>
              <div>
                <h2 className="font-bold text-base text-on-surface leading-tight">{storeInfo.name}</h2>
                <p className="text-xs text-primary font-medium">
                  {lang === "es"
                    ? "Menú bilingüe y asistente interactivo"
                    : "Bilingual menu & interactive assistant"}
                </p>
              </div>
            </div>

            <div className="space-y-3 text-xs text-on-surface-variant">
              <div className="flex items-start gap-2">
                <MapPin className="w-3.5 h-3.5 text-primary shrink-0 mt-0.5" />
                <span>{storeInfo.address}</span>
              </div>

              {isValidPhone(storeInfo.phone) && (
                <div className="flex items-start gap-2">
                  <Phone className="w-3.5 h-3.5 text-primary shrink-0 mt-0.5" />
                  <span>{storeInfo.phone}</span>
                </div>
              )}

              <div className="flex items-start gap-2">
                <Clock className="w-3.5 h-3.5 text-primary shrink-0 mt-0.5" />
                <div>
                  <p>
                    {lang === "es" ? "Lun-Vie: " : "Mon-Fri: "}
                    {storeInfo.hours.monday_friday}
                  </p>
                  <p>
                    {lang === "es" ? "Sáb: " : "Sat: "}
                    {storeInfo.hours.saturday}
                    {" | "}
                    {lang === "es" ? "Dom: " : "Sun: "}
                    {storeInfo.hours.sunday}
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-2">
                <CreditCard className="w-3.5 h-3.5 text-primary shrink-0 mt-0.5" />
                <div className="flex flex-wrap gap-1">
                  {storeInfo.paymentMethods.map((pm, i) => {
                    let translatedPm = pm;
                    if (lang === "es") {
                      if (pm.toLowerCase().includes("cash")) translatedPm = "Efectivo";
                      else if (pm.toLowerCase().includes("credit")) translatedPm = "Tarjetas de Crédito / Débito";
                    } else {
                      if (pm.toLowerCase().includes("efectivo")) translatedPm = "Cash";
                      else if (pm.toLowerCase().includes("tarjeta")) translatedPm = "Credit / Debit Cards";
                    }

                    return (
                      <span key={i} className="px-2 py-0.5 bg-surface-container rounded-md text-[10px] font-semibold text-on-surface">
                        {translatedPm}
                      </span>
                    );
                  })}
                </div>
              </div>
            </div>

            <button
              onClick={() => { setShowInfoModal(false); setShowClaimModal(true); }}
              className="mt-4 w-full py-2.5 bg-primary-fixed text-primary font-bold text-xs rounded-full hover:bg-secondary-fixed transition-all"
            >
              {lang === "es" ? "¿Es el dueño? Administrar menú" : "Own this place? Manage menu"}
            </button>
            <button
              onClick={() => setShowInfoModal(false)}
              className="mt-2 w-full py-3 btn-primary text-xs"
            >
              {lang === "es" ? "Entendido" : "Done"}
            </button>
          </div>
        </div>
      )}

      {/* Claim / Customize Modal */}
      {showClaimModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-xs animate-in fade-in duration-200">
          <div className="bg-white rounded-3xl max-w-sm w-full p-6 shadow-2xl border border-slate-200 relative overflow-hidden animate-in zoom-in-95 duration-200 text-slate-900">
            <button
              onClick={() => setShowClaimModal(false)}
              className="absolute top-4 right-4 p-1.5 rounded-full bg-slate-100 text-slate-500 hover:text-slate-800 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>

            <div className="flex items-center gap-2.5 mb-3">
              <div className="w-10 h-10 rounded-2xl bg-blue-50 text-[#0A5CFF] flex items-center justify-center font-bold">
                <Store className="w-5 h-5 text-[#0A5CFF]" />
              </div>
              <div>
                <h3 className="font-extrabold text-base leading-tight">
                  {lang === "es" ? "¿Es el dueño o administrador?" : "Are you the owner or manager?"}
                </h3>
                <p className="text-xs text-[#0A5CFF] font-semibold">
                  {storeInfo.name}
                </p>
              </div>
            </div>

            <div className="space-y-3 text-xs text-slate-600 leading-relaxed border-t border-slate-100 pt-3">
              <p>
                {lang === "es"
                  ? `DuoTaps proporciona este menú digital en español y asistente para ayudar a su establecimiento a atender cómodamente a clientes hispanohablantes.`
                  : `DuoTaps provides this digital Spanish menu and guest assistant to help your establishment welcome Spanish-speaking diners.`}
              </p>
              <p>
                {lang === "es"
                  ? `Si desea verificar este perfil, actualizar platillos y precios con su menú oficial, o solicitar soportes físicos de código QR gratuitos para sus mesas, contáctenos directamente:`
                  : `To verify this listing, update items and prices with your official menu, or request complimentary tabletop QR code stands for your restaurant, reach out directly:`}
              </p>
            </div>

            {contactSubmitted ? (
              <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-2xl text-emerald-800 text-xs text-center font-bold space-y-1 my-3 animate-in fade-in">
                <Check className="w-5 h-5 mx-auto text-emerald-600" />
                <p>{lang === "es" ? "¡Mensaje recibido!" : "Message received!"}</p>
                <p className="font-normal text-[11px] text-emerald-700">
                  {lang === "es"
                    ? "Nos pondremos en contacto a la brevedad."
                    : "The DuoTaps team will follow up with you shortly."}
                </p>
              </div>
            ) : (
              <form onSubmit={handleSendContact} className="mt-3 space-y-2 border-t border-slate-100 pt-3">
                <span className="text-[11px] font-bold text-slate-700 block">
                  {lang === "es" ? "Enviar solicitud directa:" : "Send quick request:"}
                </span>
                <input
                  type="text"
                  placeholder={lang === "es" ? "Su correo o teléfono..." : "Your email or phone..."}
                  value={contactInput}
                  onChange={(e) => setContactInput(e.target.value)}
                  className="w-full text-xs px-3 py-2 rounded-xl border border-slate-200 focus:outline-none focus:border-[#0A5CFF] bg-slate-50/50"
                  required
                />
                <textarea
                  placeholder={lang === "es" ? "Mensaje o cambios al menú..." : "Message or menu changes..."}
                  value={messageInput}
                  onChange={(e) => setMessageInput(e.target.value)}
                  rows={2}
                  className="w-full text-xs px-3 py-2 rounded-xl border border-slate-200 focus:outline-none focus:border-[#0A5CFF] bg-slate-50/50 resize-none"
                />
                <button
                  type="submit"
                  disabled={isSubmittingContact}
                  className="w-full py-2.5 bg-[#0A5CFF] text-white font-extrabold text-xs rounded-xl shadow-xs hover:brightness-110 transition-all flex items-center justify-center gap-1.5 disabled:opacity-50"
                >
                  {isSubmittingContact ? (
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  ) : (
                    <Send className="w-3.5 h-3.5" />
                  )}
                  <span>{lang === "es" ? "Enviar Solicitud" : "Send Request"}</span>
                </button>
              </form>
            )}

            <div className="pt-3 border-t border-slate-100 space-y-2">
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                {lang === "es" ? "O contáctenos por:" : "Or contact us via:"}
              </span>

              <div className="grid grid-cols-2 gap-2">
                {/* Open in Gmail */}
                <a
                  href={`https://mail.google.com/mail/?view=cm&fs=1&to=contact@duotaps.com&su=${encodeURIComponent("Manage Menu for " + storeInfo.name)}&body=${encodeURIComponent("Hi DuoTaps,\n\nI am contacting you regarding: " + storeInfo.name + "\n\n")}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="py-2.5 px-3 bg-red-50 text-red-700 border border-red-200/80 font-bold text-xs rounded-xl hover:bg-red-100 transition-all flex items-center justify-center gap-1.5 shadow-2xs"
                >
                  <Mail className="w-4 h-4 text-red-600" />
                  <span>Open Gmail</span>
                </a>

                {/* Default Mail app */}
                <a
                  href={`mailto:contact@duotaps.com?subject=Manage%20Menu%20for%20${encodeURIComponent(storeInfo.name)}`}
                  className="py-2.5 px-3 bg-slate-100 text-slate-700 border border-slate-200 font-bold text-xs rounded-xl hover:bg-slate-200 transition-all flex items-center justify-center gap-1.5 shadow-2xs"
                >
                  <ExternalLink className="w-4 h-4 text-slate-500" />
                  <span>Mail App</span>
                </a>
              </div>

              {/* 1-Click Copy Email */}
              <button
                type="button"
                onClick={handleCopyEmail}
                className="w-full py-2 bg-slate-50 border border-slate-200 text-slate-700 font-semibold text-xs rounded-xl hover:bg-slate-100 transition-all flex items-center justify-center gap-1.5"
              >
                {copiedEmail ? (
                  <>
                    <Check className="w-3.5 h-3.5 text-emerald-600" />
                    <span className="text-emerald-700 font-bold">contact@duotaps.com copiado!</span>
                  </>
                ) : (
                  <>
                    <Copy className="w-3.5 h-3.5 text-slate-400" />
                    <span>{lang === "es" ? "Copiar correo: contact@duotaps.com" : "Copy: contact@duotaps.com"}</span>
                  </>
                )}
              </button>

              {/* Instagram */}
              <a
                href="https://instagram.com/duotaps"
                target="_blank"
                rel="noopener noreferrer"
                className="w-full py-2 bg-slate-50 border border-slate-200 text-slate-700 font-bold text-xs rounded-xl hover:bg-slate-100 transition-all flex items-center justify-center gap-1.5"
              >
                <span>Instagram: @duotaps</span>
              </a>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
