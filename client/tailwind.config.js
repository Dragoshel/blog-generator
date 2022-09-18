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
        'boxy': '3px 3px 0px 0px #B91C1C, 5px 5px 0px 0px #DC2626, 7px 7px 0px 0px #EF4444'
      }
    },
  },
  plugins: [],
}
