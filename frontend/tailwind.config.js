/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#b45309', // ambrato come il logo del bistrò
      },
    },
  },
  plugins: [],
}
