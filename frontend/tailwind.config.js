module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        sky: {
          100: '#e0f7fa', // Couleur personnalisée pour bg-sky-100
        },
      },
    },
  },
  plugins: [],
};
