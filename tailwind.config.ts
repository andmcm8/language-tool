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
        "surface-container-lowest": "#ffffff",
        "surface-container-low": "#f2f4f6",
        "surface-container": "#eceef0",
        "surface-container-high": "#e6e8ea",
        "surface-container-highest": "#e0e3e5",
        "surface": "#f7f9fb",
        "surface-dim": "#d8dadc",
        "surface-bright": "#f7f9fb",
        "surface-variant": "#e0e3e5",
        "surface-tint": "#004ced",
        "primary": "#003ec7",
        "primary-container": "#0052ff",
        "on-primary": "#ffffff",
        "on-primary-container": "#dfe3ff",
        "primary-fixed-dim": "#b7c4ff",
        "primary-fixed": "#dde1ff",
        "secondary": "#505f76",
        "secondary-container": "#d0e1fb",
        "secondary-fixed": "#d3e4fe",
        "secondary-fixed-dim": "#b7c8e1",
        "on-secondary": "#ffffff",
        "on-secondary-container": "#54647a",
        "on-surface": "#191c1e",
        "on-surface-variant": "#434656",
        "tertiary": "#952200",
        "tertiary-container": "#bf3003",
        "on-tertiary": "#ffffff",
        "on-tertiary-container": "#ffddd5",
        "outline": "#737688",
        "outline-variant": "#c3c5d9",
        "background": "#f7f9fb",
        "on-background": "#191c1e",
      },
      borderRadius: {
        DEFAULT: "1rem",
        lg: "2rem",
        xl: "3rem",
        full: "9999px",
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
