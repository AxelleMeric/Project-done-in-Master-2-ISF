// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxt/eslint',
    '@nuxt/ui',
    'nuxt-charts',
    '@nuxthub/core',
    '@nuxtjs/mdc'
  ],

  devtools: {
    enabled: true
  },

  app: {
    head: {
      templateParams: {
        separator: '•'
      },
      titleTemplate: '%s %separator %siteName',
      link: [
        { rel: 'icon', type: 'image/png', href: '/favicon.png' }
      ]
    }
  },

  css: ['~/assets/css/main.css'],

  ui: {
    theme: { colors: [
      'error',
      'info',
      'success',
      'warning',
      'purple',
      'violet'
    ] }
  },

  experimental: {
    viewTransition: true
  },

  compatibilityDate: '2024-07-11',

  nitro: {
    experimental: {
      openAPI: true
    }
  },

  hub: {
    db: {
      dialect: 'mysql',
      driver: 'mysql2'
    }
  },

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  }
})
