/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        'blac': '#222831',
        'lblac': '#383E45',
        'dand': '#FFD369',
        'bone': '#EEEEEE',
        'ddand': '#D5B059',
        height: {
          '128': '32rem',
        }
    
      },
    },
  },
  plugins: [],
  corePlugins: {

  },
}

