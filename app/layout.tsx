import type { Metadata, Viewport } from "next";
import { Analytics } from "@vercel/analytics/react";
import "./globals.css";

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
    <html lang="es">
      <body className="bg-surface text-on-surface min-h-screen flex flex-col selection:bg-primary-container selection:text-on-primary font-sans antialiased">
        {children}
        <Analytics />
      </body>
    </html>
  );
}
