import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Brand
        primary: "#0A5CFF",
        "primary-container": "#2F7BFF",
        "on-primary": "#ffffff",
        "on-primary-container": "#E6EFFF",
        "primary-fixed": "#E4EDFF",
        "primary-fixed-dim": "#B9D0FF",
        "surface-tint": "#0A5CFF",
        // Ink
        "on-surface": "#0B1B33",
        "on-surface-variant": "#5A6B85",
        "on-background": "#0B1B33",
        navy: "#0B1B33",
        // Surfaces
        background: "#F2F7FE",
        surface: "#FFFFFF",
        "surface-bright": "#FFFFFF",
        "surface-container-lowest": "#FFFFFF",
        "surface-container-low": "#F6F9FE",
        "surface-container": "#EDF3FC",
        "surface-container-high": "#E3ECF9",
        "surface-container-highest": "#D8E3F5",
        "surface-dim": "#D8E3F5",
        "surface-variant": "#E3ECF9",
        // Supporting
        secondary: "#4A5D7A",
        "secondary-container": "#DCE8FB",
        "secondary-fixed": "#E1ECFD",
        "secondary-fixed-dim": "#BCD0F0",
        "on-secondary": "#ffffff",
        "on-secondary-container": "#3D5072",
        outline: "#7C8CA6",
        "outline-variant": "#CCD8EC",
        tertiary: "#D9480F",
        "tertiary-container": "#F76707",
        "on-tertiary": "#ffffff",
        "on-tertiary-container": "#FFE8D9",
      },
      borderRadius: {
        DEFAULT: "1rem",
        lg: "1.5rem",
        xl: "2rem",
        "2xl": "1.5rem",
        "3xl": "1.75rem",
        full: "9999px",
      },
      boxShadow: {
        soft: "0 1px 2px rgba(11,27,51,0.04), 0 10px 28px -10px rgba(10,60,140,0.16)",
        lift: "0 2px 4px rgba(11,27,51,0.05), 0 18px 40px -12px rgba(10,60,140,0.26)",
        float: "0 12px 40px -8px rgba(11,27,51,0.45)",
        brand: "0 10px 24px -8px rgba(10,92,255,0.55)",
      },
      backgroundImage: {
        "brand-gradient": "linear-gradient(135deg, #1F7BFF 0%, #0A5CFF 55%, #0847D6 100%)",
        "brand-gradient-soft": "linear-gradient(180deg, #38BDF8 0%, #0A5CFF 100%)",
      },
      fontFamily: {
        sans: ["var(--font-jakarta)", "Plus Jakarta Sans", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
