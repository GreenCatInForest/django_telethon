/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../django_telethon/templates/**/*.html',
    '../chats/templates/**/*.html',
    './static/**/*.js',                       
    './static/**/*.css', 
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

