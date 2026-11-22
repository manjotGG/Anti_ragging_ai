export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        indigo: { 50: '#eef2ed', 100: '#e3ebe0', 400: '#a4b99e', 500: '#57765b', 600: '#46634f', 900: '#2a372f', 950: '#19211e' },
      },
      boxShadow: {
        soft: '0 20px 50px rgba(15, 23, 42, 0.08)',
      },
    },
  },
  plugins: [],
}
