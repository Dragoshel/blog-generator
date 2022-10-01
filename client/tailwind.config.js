/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme');
const colors = require('tailwindcss/colors');

module.exports = {
  content: ["./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        'mono': ['"3270 Medium"', ...defaultTheme.fontFamily.mono]
      },
      boxShadow: {
        'boxy': '4px 4px 0px 0px #B91C1C, 6px 6px 0px 0px #DC2626, 8px 8px 0px 0px #EF4444'
      }
    },
  },
  plugins: [],
}
