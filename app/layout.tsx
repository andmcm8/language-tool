import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "El Sol Market & Deli - Stamford Bilingual Assistant",
  description: "Mobile smart storefront app for El Sol Market & Deli in Stamford, CT with live catalog, camera translator, and voice AI assistant.",
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
