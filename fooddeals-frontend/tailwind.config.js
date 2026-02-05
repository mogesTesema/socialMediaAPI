/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eef7ff',
          100: '#d9ecff',
          200: '#b6d9ff',
          300: '#86bfff',
          400: '#579aff',
          500: '#2f76ff',
          600: '#1c5bf5',
          700: '#1747c2',
          800: '#183d99',
          900: '#1a357a',
        },
      },
    },
  },
  plugins: [],
}

