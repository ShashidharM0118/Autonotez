// Tailwind v4 uses preset config; extend with theme tokens
/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ['class'],
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#0F0F0F',
        surface: '#151515',
        muted: '#1A1A1A',
        border: '#242424',
        text: '#E5E7EB',
        subtext: '#9CA3AF',
        primary: '#0D66CC',
        secondary: '#8B5CF6',
        accent: '#0EA5E9'
      },
      boxShadow: {
        subtle: '0 2px 8px rgba(0,0,0,0.25)',
      },
      transitionTimingFunction: {
        smooth: 'cubic-bezier(0.22, 1, 0.36, 1)',
      }
    }
  },
  plugins: [],
}
