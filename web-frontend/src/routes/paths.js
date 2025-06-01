// ----------------------------------------------------------------------

const ROOTS = {
  HOME: '/',
  SEARCH: '/search',
  DASHBOARD: '/dashboard',
  AUTH: '/auth',
  BLOG: '/blog',
  REF: '/ref',
  CHAT: '/chat',
};

// ----------------------------------------------------------------------

export const paths = {
  // minimalUI: 'https://mui.com/store/items/minimal-dashboard/',
  // Home: '/',

  home: {
    root: ROOTS.HOME,
  },

  blog: {
    root: ROOTS.BLOG,
  },

  chat: {
    root: ROOTS.CHAT,
  },

  // Pages of the herb
  ref: {
    herb: `${ROOTS.REF}/herb`,
    book: `${ROOTS.REF}/book`,
    treatment: `${ROOTS.REF}/treatment`,
    disclaimer: `${ROOTS.REF}/disclaimer`,
  },

  // ABOUT
  about: '/about-us',
  page403: '/error/403',
  page404: '/error/404',
  page500: '/error/500',

  // SEARCH
  search: {
    root: ROOTS.SEARCH,
    results: `${ROOTS.SEARCH}/result`,
  },

  // DASHBOARD
  dashboard: {
    root: ROOTS.DASHBOARD,
    one: `${ROOTS.DASHBOARD}/one`,
    two: `${ROOTS.DASHBOARD}/two`,
    three: `${ROOTS.DASHBOARD}/three`,
    group: {
      root: `${ROOTS.DASHBOARD}/group`,
      five: `${ROOTS.DASHBOARD}/group/five`,
      six: `${ROOTS.DASHBOARD}/group/six`,
    },
  },
  // AUTH
  auth: {
    jwt: {
      login: `${ROOTS.AUTH}/jwt/login`,
      register: `${ROOTS.AUTH}/jwt/register`,
    },
  },

};
