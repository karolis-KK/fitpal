/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [ 
    './templates/**/*.html', 
    './static/js/**/*.js',   
  ],
  theme: {
    screens: {
      'sm': '640px',
      'md': '768px',
      'lg': '1467px',
      'xl': '1500px',
      '2xl': '1536px',
    },
    extend: {
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}