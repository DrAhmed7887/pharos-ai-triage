/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'arabic': ['Cairo', 'sans-serif'],
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        triage: {
          1: '#ef4444', // Red
          2: '#f97316', // Orange
          3: '#eab308', // Yellow
          4: '#22c55e', // Green
          5: '#3b82f6', // Blue
        }
      }
    },
  },
  plugins: [],
}
