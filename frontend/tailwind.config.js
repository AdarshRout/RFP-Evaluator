/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        navy: { DEFAULT: "#002B7F", light: "#003B99" },
        brand: { DEFAULT: "#002B7F", light: "#00B2FE", lighter: "#5ce1e6" },
        surface: { DEFAULT: "#000000", card: "#0a0a0a", border: "#262626", hover: "#141414" },
        muted: { DEFAULT: "#E5E5E5", light: "#FFFFFF" },
        success: { DEFAULT: "#76D600", muted: "#224000" },
        danger: { DEFAULT: "#F85149", muted: "#4A1010" },
        warning: { DEFAULT: "#D29922", muted: "#3D2A00" },
        lime: { DEFAULT: "#76D600", light: "#8eff00" },
        cyan: { DEFAULT: "#00B2FE", light: "#33c1ff" },
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
