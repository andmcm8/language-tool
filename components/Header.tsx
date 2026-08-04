"use client";

import React, { useState } from "react";
import { MerchantConfig } from "@/types/merchant";
import { listMerchants } from "@/lib/merchants";
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
  Check
} from "lucide-react";

interface HeaderProps {
  merchant: MerchantConfig;
  lang: "es" | "en";
  setLang: (lang: "es" | "en") => void;
}

export default function Header({ merchant, lang, setLang }: HeaderProps) {
  const router = useRouter();
  const [showInfoModal, setShowInfoModal] = useState(false);
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
      <header className="sticky top-0 z-30 bg-surface/85 backdrop-blur-xl border-b border-surface-container-high px-4 py-2.5 shadow-2xs transition-all">
        <div className="max-w-md mx-auto flex items-center justify-between">
          {/* Left: Dynamic Brand Identity with Merchant Switcher Trigger */}
          <div className="relative">
            <button
              onClick={() => setShowMerchantMenu(!showMerchantMenu)}
              className="flex items-center gap-2.5 text-left group"
            >
              <div
                className="w-9 h-9 rounded-2xl text-white flex items-center justify-center shadow-xs group-hover:scale-105 transition-transform"
                style={{ backgroundColor: storeInfo.themeColor || "#003ec7" }}
              >
                {getLogoIcon(storeInfo.logoIcon)}
              </div>
              <div>
                <div className="flex items-center gap-1">
                  <h1 className="font-bold text-on-surface text-sm tracking-tight leading-none truncate max-w-[140px]">
                    {storeInfo.name}
                  </h1>
                  <ChevronDown className="w-3.5 h-3.5 text-on-surface-variant group-hover:text-primary transition-transform" />
                </div>
                <div className="flex items-center gap-1 mt-0.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                  <p className="text-[11px] text-on-surface-variant font-medium truncate max-w-[130px]">
                    {storeInfo.address.split(",")[1] || "Stamford, CT"}
                  </p>
                </div>
              </div>
            </button>

            {/* Merchant Switcher Dropdown Menu */}
            {showMerchantMenu && (
              <div className="absolute top-12 left-0 z-50 bg-surface-container-lowest border border-secondary-fixed shadow-2xl rounded-2xl p-2 w-64 animate-in fade-in zoom-in-95 duration-150">
                <div className="text-[10px] font-bold text-on-surface-variant uppercase px-2 py-1 tracking-wider border-b border-surface-container mb-1">
                  {lang === "es" ? "Demostración de Negocios:" : "Demo Merchant Storefronts:"}
                </div>
                {allMerchants.map((m) => (
                  <button
                    key={m.id}
                    onClick={() => {
                      setShowMerchantMenu(false);
                      router.push(`/${m.id}`);
                    }}
                    className={`w-full flex items-center justify-between p-2 rounded-xl text-left text-xs font-semibold transition-all ${
                      m.id === storeInfo.id
                        ? "bg-secondary-fixed text-primary font-bold"
                        : "hover:bg-surface-container text-on-surface-variant hover:text-on-surface"
                    }`}
                  >
                    <div>
                      <div>{m.name}</div>
                      <div className="text-[10px] text-on-surface-variant font-normal">{m.tagline}</div>
                    </div>
                    {m.id === storeInfo.id && <Check className="w-3.5 h-3.5 text-primary" />}
                  </button>
                ))}
              </div>
            )}
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
                <p className="text-xs text-primary font-medium">{storeInfo.tagline}</p>
              </div>
            </div>

            <div className="space-y-3 text-xs text-on-surface-variant">
              <div className="flex items-start gap-2">
                <MapPin className="w-3.5 h-3.5 text-primary shrink-0 mt-0.5" />
                <span>{storeInfo.address}</span>
              </div>

              <div className="flex items-start gap-2">
                <Phone className="w-3.5 h-3.5 text-primary shrink-0 mt-0.5" />
                <span>{storeInfo.phone}</span>
              </div>

              <div className="flex items-start gap-2">
                <Clock className="w-3.5 h-3.5 text-primary shrink-0 mt-0.5" />
                <div>
                  <p>Lun-Vie: {storeInfo.hours.monday_friday}</p>
                  <p>Sáb: {storeInfo.hours.saturday} | Dom: {storeInfo.hours.sunday}</p>
                </div>
              </div>

              <div className="flex items-start gap-2">
                <CreditCard className="w-3.5 h-3.5 text-primary shrink-0 mt-0.5" />
                <div className="flex flex-wrap gap-1">
                  {storeInfo.paymentMethods.map((pm, i) => (
                    <span key={i} className="px-2 py-0.5 bg-surface-container rounded-md text-[10px] text-on-surface">
                      {pm}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <button
              onClick={() => setShowInfoModal(false)}
              className="mt-5 w-full py-2 bg-primary text-white font-bold text-xs rounded-xl shadow-xs hover:bg-primary-container transition-all"
            >
              OK
            </button>
          </div>
        </div>
      )}
    </>
  );
}
