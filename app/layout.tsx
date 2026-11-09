import type { Metadata, Viewport } from "next";
import { Analytics } from "@vercel/analytics/react";
import { Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";

const jakarta = Plus_Jakarta_Sans({ subsets: ["latin"], variable: "--font-jakarta", display: "swap" });

export const metadata: Metadata = {
  title: "DuoTaps — Language Assistance Tool",
  description: "DuoTaps provides Connecticut restaurants and places with interactive bilingual Spanish menus and customer assistance.",
  icons: {
    icon: "/favicon.png",
    shortcut: "/favicon.png",
    apple: "/favicon.png",
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className={jakarta.variable}>
      <body className="text-on-surface min-h-screen flex flex-col selection:bg-primary selection:text-white font-sans antialiased">
        {children}
        <Analytics />
      </body>
    </html>
  );
}
