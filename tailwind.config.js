/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.html"],
  theme: {
    extend: {
      keyframes: {
        'loader': {
          '0%': { transform: 'rotate(0deg)' },
          '100%': {transform: 'rotate(360deg)' }
        }
      },
      animation: {
        'loader': 'loader 1s linear infinite'
      }
    },
  },
  plugins: [],
}

