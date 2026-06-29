/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        navy: { DEFAULT: "#1A3A5C", light: "#1E4A73" },
        brand: { DEFAULT: "#2B6CB0", light: "#3182CE", lighter: "#4299E1" },
        surface: { DEFAULT: "#0D1117", card: "#161B22", border: "#21262D", hover: "#1C2128" },
        muted: { DEFAULT: "#8B949E", light: "#B0BAC5" },
        success: { DEFAULT: "#3FB950", muted: "#1A4731" },
        danger: { DEFAULT: "#F85149", muted: "#4A1010" },
        warning: { DEFAULT: "#D29922", muted: "#3D2A00" },
      },
      fontFamily: { sans: ["Inter", "system-ui", "sans-serif"], mono: ["JetBrains Mono", "monospace"] },
      animation: {
        "pulse-slow": "pulse 3s ease-in-out infinite",
        "fade-in": "fadeIn 0.4s ease-out",
        "slide-up": "slideUp 0.4s ease-out",
      },
      keyframes: {
        fadeIn: { from: { opacity: "0" }, to: { opacity: "1" } },
        slideUp: { from: { opacity: "0", transform: "translateY(12px)" }, to: { opacity: "1", transform: "translateY(0)" } },
      },
    },
  },
  plugins: [],
};
