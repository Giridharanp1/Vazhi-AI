/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{js,jsx,ts,tsx}", "./components/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#1E293B",
        secondary: "#334155",
        accent: "#3B82F6",
        danger: "#EF4444",
        warning: "#F59E0B",
        success: "#10B981"
      }
    },
  },
  plugins: [],
}
