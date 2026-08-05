import React from "react";
import Link from "next/link";
import { getAllMerchants } from "@/lib/merchants";
import {
  ShoppingBag,
  Pill,
  Wrench,
  Camera,
  MessageSquare,
  Sparkles,
  MapPin,
  Clock,
  Phone,
  ArrowRight,
  ShieldCheck,
  Globe,
  Zap,
} from "lucide-react";

export const metadata = {
  title: "Language Tool - Merchant Assistant & Translation Portal",
  description:
    "Select your local business to launch their bilingual AI assistant, Google Translate camera mode, and interactive product directory.",
};

const MERCHANT_ICONS: Record<string, any> = {
  elsol: ShoppingBag,
  "clover-pharmacy": Pill,
  "stamford-repairs": Wrench,
};

const MERCHANT_GRADIENTS: Record<string, string> = {
  elsol: "from-amber-500 to-orange-600",
  "clover-pharmacy": "from-emerald-500 to-teal-600",
  "stamford-repairs": "from-blue-600 to-indigo-600",
};

const MERCHANT_BADGES: Record<string, string> = {
  elsol: "Supermarket & Deli",
  "clover-pharmacy": "Bilingual Pharmacy",
  "stamford-repairs": "Device & Phone Repair",
};

export default function HomePage() {
  const merchants = getAllMerchants();

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-primary selection:text-white">
      {/* BACKGROUND GRADIENT DECORATION */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute -top-40 -left-40 w-96 h-96 bg-primary/20 rounded-full blur-3xl" />
        <div className="absolute top-1/3 -right-40 w-96 h-96 bg-amber-500/15 rounded-full blur-3xl" />
        <div className="absolute -bottom-40 left-1/3 w-96 h-96 bg-emerald-500/15 rounded-full blur-3xl" />
      </div>

      {/* HEADER BAR */}
      <header className="relative z-10 border-b border-white/10 bg-slate-900/60 backdrop-blur-md sticky top-0">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-primary to-amber-400 flex items-center justify-center text-white shadow-md font-black text-lg">
              L
            </div>
            <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
              Language Tool Portal
            </span>
          </div>

          <div className="flex items-center gap-2 text-xs font-bold text-slate-400 bg-white/5 border border-white/10 px-3 py-1.5 rounded-full">
            <Globe className="w-3.5 h-3.5 text-primary" />
            <span>Bilingual EN / ES</span>
          </div>
        </div>
      </header>

      {/* HERO SECTION */}
      <section className="relative z-10 max-w-4xl mx-auto px-4 pt-12 pb-8 text-center space-y-4">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-extrabold shadow-xs">
          <Sparkles className="w-3.5 h-3.5" />
          <span>AI-Powered Merchant & Camera Assistant</span>
        </div>

        <h1 className="text-4xl md:text-5xl font-black tracking-tight text-white leading-tight">
          Select Your Local Business Below
        </h1>

        <p className="text-slate-400 text-sm md:text-base max-w-2xl mx-auto leading-relaxed">
          Access instant bilingual AI customer service, real-time Google Translate camera mode for signs & menus, and interactive store directories.
        </p>
      </section>

      {/* MERCHANT STORE CARDS GRID */}
      <section className="relative z-10 max-w-6xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {merchants.map((merchant) => {
            const id = merchant.storeInfo.id;
            const Icon = MERCHANT_ICONS[id] || ShoppingBag;
            const gradient = MERCHANT_GRADIENTS[id] || "from-primary to-blue-600";
            const categoryBadge = MERCHANT_BADGES[id] || "Local Business";

            return (
              <div
                key={id}
                className="group relative bg-slate-900/80 border border-white/10 hover:border-white/25 rounded-3xl p-6 flex flex-col justify-between transition-all duration-300 hover:-translate-y-1 shadow-xl hover:shadow-2xl overflow-hidden backdrop-blur-sm"
              >
                {/* Top Ambient Glow */}
                <div
                  className={`absolute top-0 inset-x-0 h-1.5 bg-gradient-to-r ${gradient}`}
                />

                <div className="space-y-4">
                  {/* Category & Icon */}
                  <div className="flex items-center justify-between">
                    <div
                      className={`w-12 h-12 rounded-2xl bg-gradient-to-br ${gradient} flex items-center justify-center text-white shadow-lg group-hover:scale-110 transition-transform`}
                    >
                      <Icon className="w-6 h-6" />
                    </div>
                    <span className="text-[11px] font-extrabold uppercase tracking-wider text-slate-400 bg-white/5 border border-white/10 px-2.5 py-1 rounded-full">
                      {categoryBadge}
                    </span>
                  </div>

                  {/* Name & Tagline */}
                  <div>
                    <h2 className="text-xl font-black text-white group-hover:text-amber-400 transition-colors">
                      {merchant.storeInfo.name}
                    </h2>
                    <p className="text-xs text-slate-400 mt-1 line-clamp-2 leading-relaxed">
                      {merchant.storeInfo.tagline}
                    </p>
                  </div>

                  {/* Store Details */}
                  <div className="space-y-2 pt-2 text-xs text-slate-300 border-t border-white/5">
                    <div className="flex items-start gap-2">
                      <MapPin className="w-3.5 h-3.5 text-primary shrink-0 mt-0.5" />
                      <span className="truncate">{merchant.storeInfo.address}</span>
                    </div>

                    <div className="flex items-center gap-2">
                      <Phone className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                      <span>{merchant.storeInfo.phone}</span>
                    </div>

                    <div className="flex items-center gap-2">
                      <Clock className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                      <span>Mon-Fri: {merchant.storeInfo.hours.monday_friday}</span>
                    </div>
                  </div>

                  {/* Amenities Badges */}
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {merchant.storeInfo.amenities?.map((item, idx) => (
                      <span
                        key={idx}
                        className="text-[10px] font-bold text-slate-300 bg-white/5 px-2 py-0.5 rounded-md border border-white/5"
                      >
                        {item}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Launch Button Link */}
                <div className="pt-6">
                  <Link
                    href={`/${id}`}
                    className={`w-full py-3 px-4 rounded-2xl bg-gradient-to-r ${gradient} text-white font-extrabold text-xs flex items-center justify-center gap-2 shadow-lg hover:brightness-110 transition-all group-hover:gap-3`}
                  >
                    <span>Launch Merchant Assistant</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* PORTAL FEATURES HIGHLIGHT */}
      <section className="relative z-10 max-w-5xl mx-auto px-4 py-12 border-t border-white/10 mt-8">
        <div className="text-center space-y-2 mb-10">
          <h2 className="text-2xl font-black text-white">Included Features</h2>
          <p className="text-slate-400 text-xs md:text-sm">
            Everything designed for fast, seamless bilingual commerce & communication.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-slate-900/50 border border-white/10 rounded-2xl p-5 space-y-3">
            <div className="w-10 h-10 rounded-xl bg-primary/20 text-primary flex items-center justify-center">
              <Camera className="w-5 h-5" />
            </div>
            <h3 className="font-extrabold text-sm text-white">Google Translate Camera</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Real-time paint-over OCR translation for store signs, menus, handwritten notes, and receipts.
            </p>
          </div>

          <div className="bg-slate-900/50 border border-white/10 rounded-2xl p-5 space-y-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
              <MessageSquare className="w-5 h-5" />
            </div>
            <h3 className="font-extrabold text-sm text-white">Bilingual AI Assistant</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Instant answers about store specials, payment methods (EBT/Cash), return policies, and hours.
            </p>
          </div>

          <div className="bg-slate-900/50 border border-white/10 rounded-2xl p-5 space-y-3">
            <div className="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center">
              <Zap className="w-5 h-5" />
            </div>
            <h3 className="font-extrabold text-sm text-white">Interactive Directory</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Browse products, prices, and services with 1-tap translation and search filters.
            </p>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="relative z-10 border-t border-white/10 py-6 text-center text-xs text-slate-500">
        <p>© {new Date().getFullYear()} Language Tool • Multi-Merchant Bilingual Assistant Portal</p>
      </footer>
    </main>
  );
}
