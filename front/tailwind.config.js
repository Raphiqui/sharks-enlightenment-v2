module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,vue}",
    // include Django templates so Tailwind can find classes in backend templates
    "../back/**/*.html",
    "../back/**/templates/**/*.html"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
