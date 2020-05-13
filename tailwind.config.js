const defaultTheme = require("tailwindcss/defaultTheme")

module.exports = {
  purge: {
    enabled: true,
    content: ["./templates/**/*.html"],
  },
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", ...defaultTheme.fontFamily.sans]
      }
    },
  },
  variants: {},
  plugins: [
    require("@tailwindcss/custom-forms")
  ],
}
