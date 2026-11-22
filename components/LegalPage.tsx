import React from "react";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

/** Shared shell for the Privacy Policy and Terms of Use pages. */
export default function LegalPage({
  title,
  updated,
  intro,
  children,
}: {
  title: string;
  updated: string;
  intro: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <main className="mx-auto w-full max-w-3xl px-5 pb-20 pt-6 md:pt-10">
      <Link
        href="/"
        className="inline-flex items-center gap-1.5 rounded-full bg-white px-3.5 py-2 text-sm font-semibold text-on-surface-variant shadow-soft transition-colors hover:text-primary"
      >
        <ArrowLeft className="h-4 w-4" /> DuoTaps
      </Link>

      <article className="mt-6 rounded-[28px] bg-white p-6 shadow-soft md:p-10">
        <p className="text-xs font-bold uppercase tracking-[0.14em] text-on-surface-variant">Last updated {updated}</p>
        <h1 className="mt-2 text-3xl font-extrabold leading-tight text-on-surface md:text-4xl">{title}</h1>
        <div className="mt-4 text-[15px] leading-relaxed text-on-surface-variant">{intro}</div>
        <div className="mt-8 space-y-8">{children}</div>
      </article>

      <nav className="mt-6 flex justify-center gap-5 text-sm font-semibold text-on-surface-variant">
        <Link href="/privacy" className="hover:text-primary">Privacy Policy</Link>
        <Link href="/terms" className="hover:text-primary">Terms of Use</Link>
        <a href="mailto:contact@duotaps.com" className="hover:text-primary">contact@duotaps.com</a>
      </nav>
    </main>
  );
}

export function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section>
      <h2 className="text-lg font-extrabold text-on-surface">{title}</h2>
      <div className="mt-2 space-y-3 text-[15px] leading-relaxed text-on-surface-variant [&_a]:font-semibold [&_a]:text-primary [&_strong]:text-on-surface [&_ul]:list-disc [&_ul]:space-y-1.5 [&_ul]:pl-5">
        {children}
      </div>
    </section>
  );
}
