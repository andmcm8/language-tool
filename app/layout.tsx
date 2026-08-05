import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "DuoTaps — Portal de Asistentes Comerciales Bilingües",
  description: "Plataforma inteligente DuoTaps de asistentes comerciales bilingües con catálogo interactivo, traductor de letreros por cámara y asistente de voz IA.",
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
      </body>
    </html>
  );
}
