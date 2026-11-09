"use client";

import React, { useState } from "react";
import Link from "next/link";
import { MerchantConfig } from "@/types/merchant";
import { isValidPhone } from "@/lib/phone";
import { townFromAddress, taglineFor, swatchFor, initialsOf } from "@/lib/place";
import { ChevronLeft, Info, MapPin, Phone, Navigation, Clock, Loader2, Check, Copy, ArrowUpRight } from "lucide-react";
import Sheet from "@/components/Sheet";
import { NAV_TABS, TabType } from "@/components/BottomNav";

interface HeaderProps {
  merchant: MerchantConfig;
  lang: "es" | "en";
  setLang: (lang: "es" | "en") => void;
  activeTab: TabType;
  setActiveTab: (tab: TabType) => void;
}

const EMAIL = "contact@duotaps.com";

function LangToggle({ lang, setLang }: { lang: "es" | "en"; setLang: (l: "es" | "en") => void }) {
  return (
    <div className="flex items-center rounded-full border border-white bg-white p-1 shadow-soft">
      {(["es", "en"] as const).map((code) => (
        <button
          key={code}
          onClick={() => setLang(code)}
          aria-pressed={lang === code}
          className={`h-8 rounded-full px-3 text-xs font-bold transition-all ${
            lang === code ? "bg-brand-gradient text-white shadow-brand" : "text-on-surface-variant hover:text-on-surface"
          }`}
        >
          {code.toUpperCase()}
        </button>
      ))}
    </div>
  );
}

export default function Header({ merchant, lang, setLang, activeTab, setActiveTab }: HeaderProps) {
  const { storeInfo } = merchant;
  const [showInfo, setShowInfo] = useState(false);
  const [showClaim, setShowClaim] = useState(false);
  const [copied, setCopied] = useState(false);
  const [contact, setContact] = useState("");
  const [message, setMessage] = useState("");
  const [sending, setSending] = useState(false);
  const [sent, setSent] = useState(false);

  const town = townFromAddress(storeInfo.address);
  const tagline = taglineFor(storeInfo.tagline, lang);
  const phoneOk = isValidPhone(storeInfo.phone);
  const hours = storeInfo.hours || ({} as MerchantConfig["storeInfo"]["hours"]);
  const hoursKnown = hours.monday_friday && !/call/i.test(hours.monday_friday);
  const mapsHref = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${storeInfo.name} ${storeInfo.address}`)}`;

  const t = {
    back: lang === "es" ? "Todos los lugares" : "All places",
    info: lang === "es" ? "Información del lugar" : "Place info",
    directions: lang === "es" ? "Cómo llegar" : "Directions",
  };

  const payment = (pm: string) => {
    const l = pm.toLowerCase();
    if (lang === "es") {
      if (l.includes("cash")) return "Efectivo";
      if (l.includes("credit")) return "Tarjetas de crédito / débito";
      if (l.includes("contactless")) return "Sin contacto";
    } else {
      if (l.includes("efectivo")) return "Cash";
      if (l.includes("tarjeta")) return "Credit / debit cards";
    }
    return pm;
  };

  const copyEmail = () => {
    navigator.clipboard?.writeText(EMAIL);
    setCopied(true);
    setTimeout(() => setCopied(false), 2200);
  };

  const sendContact = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!contact.trim()) return;
    setSending(true);
    try {
      await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          placeName: storeInfo.name,
          placeId: storeInfo.id,
          contactInfo: contact.trim(),
          message: message.trim(),
        }),
      });
    } catch {
      /* show the thank-you either way; the email address is also listed */
    } finally {
      setSending(false);
      setSent(true);
      setContact("");
      setMessage("");
    }
  };

  const row = "grid grid-cols-[88px_1fr] gap-4 py-3.5 border-b border-surface-container last:border-b-0";
  const label = "text-[12px] font-semibold uppercase tracking-wider text-on-surface-variant pt-0.5";

  return (
    <>
      {/* ---------- Phone / tablet top bar ---------- */}
      <header className="sticky top-0 z-30 glass border-x-0 border-t-0 border-b border-white/60 lg:hidden">
        <div className="mx-auto flex max-w-md items-center justify-between gap-3 px-4 py-3 md:max-w-2xl">
          <div className="flex min-w-0 items-center gap-3">
            <Link
              href="/"
              aria-label={t.back}
              className="grid h-10 w-10 shrink-0 place-items-center rounded-full border border-white bg-white text-on-surface shadow-soft transition-colors hover:text-primary"
            >
              <ChevronLeft className="h-5 w-5" strokeWidth={2.4} />
            </Link>
            <div className="min-w-0">
              <h1 className="truncate text-[17px] font-extrabold leading-tight tracking-tight text-on-surface">{storeInfo.name}</h1>
              {town && (
                <p className="mt-0.5 flex items-center gap-1 truncate text-xs font-medium text-on-surface-variant">
                  <MapPin className="h-3 w-3 shrink-0" />
                  <span className="truncate">{town}</span>
                </p>
              )}
            </div>
          </div>
          <div className="flex shrink-0 items-center gap-2">
            <LangToggle lang={lang} setLang={setLang} />
            <button
              onClick={() => setShowInfo(true)}
              aria-label={t.info}
              className="grid h-10 w-10 place-items-center rounded-full border border-white bg-white text-on-surface-variant shadow-soft transition-colors hover:text-primary"
            >
              <Info className="h-[18px] w-[18px]" />
            </button>
          </div>
        </div>
      </header>

      {/* ---------- Desktop sidebar ---------- */}
      <aside className="fixed bottom-4 left-4 top-4 z-30 hidden w-[300px] flex-col rounded-[32px] border border-white bg-white/90 p-5 shadow-lift backdrop-blur-xl lg:flex xl:w-[324px]">
        <Link href="/" className="inline-flex w-fit items-center gap-1.5 rounded-full py-1.5 pl-1 pr-3 text-[13px] font-semibold text-on-surface-variant transition-colors hover:text-primary">
          <ChevronLeft className="h-4 w-4" strokeWidth={2.4} />
          {t.back}
        </Link>

        <div className="mt-5 flex items-center gap-3.5">
          <span
            className="grid h-14 w-14 shrink-0 place-items-center rounded-2xl text-lg font-extrabold text-white shadow-soft"
            style={{ background: swatchFor(storeInfo.name) }}
          >
            {initialsOf(storeInfo.name)}
          </span>
          <div className="min-w-0">
            <h1 className="text-[19px] font-extrabold leading-tight text-on-surface">{storeInfo.name}</h1>
            {town && <p className="mt-0.5 truncate text-[13px] font-medium text-on-surface-variant">{town}</p>}
          </div>
        </div>
        {tagline && <p className="mt-3 text-[13px] leading-relaxed text-on-surface-variant line-clamp-3">{tagline}</p>}

        <ul className="mt-5 space-y-2.5 text-[13px] font-medium text-on-surface">
          {storeInfo.address && (
            <li className="flex items-start gap-2.5">
              <MapPin className="mt-0.5 h-4 w-4 shrink-0 text-primary" />
              <span>{storeInfo.address}</span>
            </li>
          )}
          {hoursKnown && (
            <li className="flex items-start gap-2.5">
              <Clock className="mt-0.5 h-4 w-4 shrink-0 text-primary" />
              <span>
                {lang === "es" ? "Lun–Vie " : "Mon–Fri "}
                {hours.monday_friday}
              </span>
            </li>
          )}
          {phoneOk && (
            <li className="flex items-start gap-2.5">
              <Phone className="mt-0.5 h-4 w-4 shrink-0 text-primary" />
              <a href={`tel:${storeInfo.phone}`} className="hover:text-primary">{storeInfo.phone}</a>
            </li>
          )}
        </ul>

        <a
          href={mapsHref}
          target="_blank"
          rel="noopener noreferrer"
          className="btn-primary mt-5 h-11 w-full text-[13px]"
        >
          <Navigation className="h-4 w-4" />
          {t.directions}
        </a>

        <nav className="mt-6 flex flex-col gap-1.5" aria-label="Primary">
          {NAV_TABS.map((tab) => {
            const Icon = tab.icon;
            const active = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                aria-current={active ? "page" : undefined}
                className={`flex h-12 items-center gap-3 rounded-full px-4 text-[14px] font-semibold transition-all ${
                  active ? "bg-navy text-white shadow-soft" : "text-on-surface-variant hover:bg-surface-container hover:text-on-surface"
                }`}
              >
                <Icon className="h-[19px] w-[19px]" strokeWidth={active ? 2.4 : 2} />
                {lang === "es" ? tab.labelEs : tab.labelEn}
              </button>
            );
          })}
        </nav>

        <div className="mt-auto flex items-center justify-between pt-5">
          <LangToggle lang={lang} setLang={setLang} />
          <button
            onClick={() => setShowInfo(true)}
            aria-label={t.info}
            className="grid h-10 w-10 place-items-center rounded-full border border-white bg-white text-on-surface-variant shadow-soft transition-colors hover:text-primary"
          >
            <Info className="h-[18px] w-[18px]" />
          </button>
        </div>
      </aside>

      {/* ---------- Place info ---------- */}
      <Sheet
        open={showInfo}
        onClose={() => setShowInfo(false)}
        eyebrow={town || (lang === "es" ? "Información" : "Info")}
        title={storeInfo.name}
        footer={
          <button
            onClick={() => {
              setShowInfo(false);
              setShowClaim(true);
            }}
            className="text-[13px] font-semibold text-on-surface-variant underline decoration-outline-variant underline-offset-4 transition-colors hover:text-primary"
          >
            {lang === "es" ? "¿Es el dueño? Administrar este menú" : "Own this place? Manage this menu"}
          </button>
        }
      >
        <dl>
          <div className={row}>
            <dt className={label}>{lang === "es" ? "Dirección" : "Address"}</dt>
            <dd className="text-[15px] font-medium text-on-surface">
              {storeInfo.address}
              <a href={mapsHref} target="_blank" rel="noopener noreferrer" className="mt-1 flex w-fit items-center gap-1 text-[13px] font-semibold text-primary">
                {t.directions} <ArrowUpRight className="h-3.5 w-3.5" />
              </a>
            </dd>
          </div>
          {phoneOk && (
            <div className={row}>
              <dt className={label}>{lang === "es" ? "Teléfono" : "Phone"}</dt>
              <dd className="text-[15px] font-medium">
                <a href={`tel:${storeInfo.phone}`} className="text-on-surface hover:text-primary">{storeInfo.phone}</a>
              </dd>
            </div>
          )}
          <div className={row}>
            <dt className={label}>{lang === "es" ? "Horario" : "Hours"}</dt>
            <dd className="space-y-1 text-[15px] font-medium text-on-surface">
              {([
                [lang === "es" ? "Lun–Vie" : "Mon–Fri", hours.monday_friday],
                [lang === "es" ? "Sáb" : "Sat", hours.saturday],
                [lang === "es" ? "Dom" : "Sun", hours.sunday],
              ] as const).map(([d, h]) => (
                <div key={d} className="flex justify-between gap-4">
                  <span className="text-on-surface-variant">{d}</span>
                  <span className="text-right tabular-nums">{h || "—"}</span>
                </div>
              ))}
            </dd>
          </div>
          {storeInfo.paymentMethods?.length > 0 && (
            <div className={row}>
              <dt className={label}>{lang === "es" ? "Pagos" : "Payment"}</dt>
              <dd className="text-[15px] font-medium text-on-surface">{storeInfo.paymentMethods.map(payment).join(" · ")}</dd>
            </div>
          )}
        </dl>
      </Sheet>

      {/* ---------- Owner contact ---------- */}
      <Sheet
        open={showClaim}
        onClose={() => setShowClaim(false)}
        eyebrow={lang === "es" ? "Para dueños" : "For owners"}
        title={lang === "es" ? "Administrar este menú" : "Manage this menu"}
      >
        <p className="text-[15px] leading-relaxed text-on-surface-variant">
          {lang === "es"
            ? `Si ${storeInfo.name} es suyo, podemos verificar el menú con sus platillos y precios oficiales, y enviarle soportes con código QR gratis para las mesas.`
            : `If ${storeInfo.name} is yours, we can match this menu to your official dishes and prices, and send you free QR stands for your tables.`}
        </p>

        {sent ? (
          <div className="mt-5 rounded-2xl bg-surface-container-low p-4">
            <p className="flex items-center gap-2 text-[15px] font-bold text-on-surface">
              <Check className="h-4 w-4 text-emerald-600" />
              {lang === "es" ? "Mensaje recibido" : "Message received"}
            </p>
            <p className="mt-1 text-sm text-on-surface-variant">
              {lang === "es" ? "Nos pondremos en contacto pronto." : "We'll be in touch shortly."}
            </p>
          </div>
        ) : (
          <form onSubmit={sendContact} className="mt-5 space-y-3">
            <input
              type="text"
              required
              value={contact}
              onChange={(e) => setContact(e.target.value)}
              placeholder={lang === "es" ? "Su correo o teléfono" : "Your email or phone"}
              className="h-12 w-full rounded-2xl border border-outline-variant/70 bg-white px-4 text-[15px] font-medium text-on-surface placeholder:text-on-surface-variant/60 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
            />
            <textarea
              rows={3}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder={lang === "es" ? "Cambios al menú (opcional)" : "Menu changes (optional)"}
              className="w-full resize-none rounded-2xl border border-outline-variant/70 bg-white px-4 py-3 text-[15px] font-medium text-on-surface placeholder:text-on-surface-variant/60 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
            />
            <button type="submit" disabled={sending} className="btn-primary h-12 w-full text-sm disabled:opacity-60">
              {sending && <Loader2 className="h-4 w-4 animate-spin" />}
              {lang === "es" ? "Enviar" : "Send"}
            </button>
          </form>
        )}

        <div className="mt-5 flex items-center justify-between gap-3 border-t border-surface-container pt-4 text-[13px] font-medium text-on-surface-variant">
          <span>
            {lang === "es" ? "O escríbanos: " : "Or email "}
            <a href={`mailto:${EMAIL}?subject=${encodeURIComponent("Manage menu for " + storeInfo.name)}`} className="font-semibold text-primary">
              {EMAIL}
            </a>
          </span>
          <button onClick={copyEmail} aria-label="Copy email" className="grid h-9 w-9 shrink-0 place-items-center rounded-full hover:bg-surface-container">
            {copied ? <Check className="h-4 w-4 text-emerald-600" /> : <Copy className="h-4 w-4" />}
          </button>
        </div>
      </Sheet>
    </>
  );
}
