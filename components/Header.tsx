"use client";

import React, { useState } from "react";
import Link from "next/link";
import { MerchantConfig } from "@/types/merchant";
import { listMerchants, isValidPhone } from "@/lib/merchants";
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
  Mail
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
  const { storeInfo } = merchant;

  const allMerchants = listMerchants();

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
      <header className="sticky top-0 z-30 bg-surface/95 backdrop-blur-xl border-b border-surface-container-high shadow-2xs transition-all">
        {/* Concept Demo / Claim Notice Banner */}
        <div className="bg-slate-900 text-slate-100 px-3.5 py-1.5 text-xs flex items-center justify-between border-b border-slate-800">
          <div className="flex items-center gap-2 min-w-0 mr-2">
            <span className="bg-amber-400/20 text-amber-300 font-bold text-[10px] uppercase tracking-wider px-1.5 py-0.5 rounded shrink-0 border border-amber-400/30">
              {lang === "es" ? "Demostración" : "Concept Demo"}
            </span>
            <p className="text-[11px] leading-tight truncate text-slate-300">
              {lang === "es"
                ? `Vista previa de menú bilingüe para ${storeInfo.name}`
                : `Interactive bilingual preview for ${storeInfo.name}`}
            </p>
          </div>
          <button
            onClick={() => setShowClaimModal(true)}
            className="shrink-0 text-[11px] font-bold text-amber-300 hover:text-amber-200 underline whitespace-nowrap cursor-pointer"
          >
            {lang === "es" ? "¿Eres el dueño? Personalizar →" : "Owner? Claim menu →"}
          </button>
        </div>

        <div className="max-w-md mx-auto px-4 py-2.5 flex items-center justify-between">
          {/* Left: Dynamic Brand Identity (Clean & Focused on Current Merchant) */}
          <div className="flex items-center gap-2.5 text-left">
            <Link
              href="/"
              className="w-9 h-9 rounded-2xl text-white flex items-center justify-center shadow-xs hover:scale-105 transition-transform"
              style={{ backgroundColor: storeInfo.themeColor || "#003ec7" }}
              title="Back to All Merchants / Volver al Inicio"
            >
              {getLogoIcon(storeInfo.logoIcon)}
            </Link>
            <div>
              <h1 className="font-bold text-on-surface text-sm tracking-tight leading-none truncate max-w-[170px]">
                {storeInfo.name}
              </h1>
              <div className="flex items-center gap-1 mt-0.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                <p className="text-[11px] text-on-surface-variant font-medium truncate max-w-[150px]">
                  {storeInfo.address.split(",")[1] || "Stamford, CT"}
                </p>
              </div>
            </div>
          </div>

          {/* Right: Condensed Unified Controls (ES/EN + Info) */}
          <div className="flex items-center gap-1 bg-surface-container/70 p-1 rounded-full border border-outline-variant/30">
            <button
              onClick={() => setLang("es")}
              className={`px-2.5 py-1 rounded-full text-xs font-bold transition-all ${
                lang === "es"
                  ? "bg-primary text-white shadow-2xs"
                  : "text-on-surface-variant hover:text-on-surface"
              }`}
            >
              ES
            </button>
            <button
              onClick={() => setLang("en")}
              className={`px-2.5 py-1 rounded-full text-xs font-bold transition-all ${
                lang === "en"
                  ? "bg-primary text-white shadow-2xs"
                  : "text-on-surface-variant hover:text-on-surface"
              }`}
            >
              EN
            </button>

            <div className="w-px h-3.5 bg-outline-variant/40 mx-0.5" />

            <button
              onClick={() => setShowInfoModal(true)}
              className="p-1 rounded-full text-on-surface-variant hover:text-primary transition-colors"
              aria-label="Store Info"
            >
              <Info className="w-4 h-4" />
            </button>
          </div>
        </div>
      </header>

      {/* Merchant Info Modal */}
      {showInfoModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs animate-in fade-in duration-200">
          <div className="bg-surface-container-lowest rounded-3xl max-w-xs w-full p-5 shadow-2xl border border-secondary-fixed/60 relative overflow-hidden animate-in zoom-in-95 duration-200">
            <button
              onClick={() => setShowInfoModal(false)}
              className="absolute top-3.5 right-3.5 p-1.5 rounded-full bg-surface-container text-on-surface-variant hover:text-on-surface transition-all"
            >
              <X className="w-4 h-4" />
            </button>

            <div className="flex items-center gap-2.5 mb-4">
              <div
                className="w-10 h-10 rounded-2xl text-white flex items-center justify-center font-bold"
                style={{ backgroundColor: storeInfo.themeColor || "#003ec7" }}
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
              onClick={() => setShowInfoModal(false)}
              className="mt-5 w-full py-2 bg-primary text-white font-bold text-xs rounded-xl shadow-xs hover:bg-primary-container transition-all"
            >
              {lang === "es" ? "Entendido" : "OK"}
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
              <div className="w-10 h-10 rounded-2xl bg-amber-50 text-amber-700 flex items-center justify-center font-bold">
                <Store className="w-5 h-5 text-amber-600" />
              </div>
              <div>
                <h3 className="font-extrabold text-base leading-tight">
                  {lang === "es" ? "¿Es el dueño del negocio?" : "Are you the owner?"}
                </h3>
                <p className="text-xs text-[#003ec7] font-semibold">
                  {storeInfo.name}
                </p>
              </div>
            </div>

            <div className="space-y-3 text-xs text-slate-600 leading-relaxed border-t border-slate-100 pt-3">
              <p>
                {lang === "es"
                  ? `DuoTaps preparó esta demostración interactiva con menú en español y asistente por IA para ilustrar cómo su negocio puede recibir y atender comensales hispanohablantes.`
                  : `DuoTaps created this interactive preview with Spanish translations and AI assistance to show how your restaurant can easily welcome Spanish-speaking guests.`}
              </p>
              <p>
                {lang === "es"
                  ? `Para actualizar platillos y precios con su menú oficial, o solicitar soportes físicos de código QR gratuitos para sus mesas, contáctenos:`
                  : `To update items and prices with your official menu, or to request free tabletop QR code displays, reach out directly:`}
              </p>
            </div>

            <div className="pt-4 space-y-2">
              <a
                href={`mailto:contact@duotaps.com?subject=Update%20Menu%20for%20${encodeURIComponent(storeInfo.name)}`}
                className="w-full py-2.5 bg-[#003ec7] text-white font-extrabold text-xs rounded-xl shadow-sm hover:brightness-110 transition-all flex items-center justify-center gap-1.5"
              >
                <Mail className="w-4 h-4" />
                <span>{lang === "es" ? "Contactar por Email" : "Email Us (contact@duotaps.com)"}</span>
              </a>
              <a
                href="https://instagram.com/duotaps"
                target="_blank"
                rel="noopener noreferrer"
                className="w-full py-2.5 bg-slate-100 text-slate-800 font-bold text-xs rounded-xl hover:bg-slate-200 transition-all flex items-center justify-center gap-1.5"
              >
                <span>{lang === "es" ? "Enviar DM por Instagram" : "DM us on Instagram (@duotaps)"}</span>
              </a>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
