import { paths } from 'src/routes/paths';

import { PATH_AFTER_LOGIN } from 'src/config-global';

import Iconify from 'src/components/iconify';

// ----------------------------------------------------------------------

export const navConfig = [
  {
    title: 'Home',
    icon: <Iconify icon="solar:home-2-bold-duotone" />,
    path: '/',
  },
  {
    title: 'Pages',
    path: '/pages',
    icon: <Iconify icon="solar:file-bold-duotone" />,
    children: [
      {
        subheader: 'Other',
        items: [
          { title: 'About us', path: paths.about },
        ],
      },
      {
        subheader: 'Error',
        items: [
          { title: 'Page 403', path: paths.page403 },
          { title: 'Page 404', path: paths.page404 },
          { title: 'Page 500', path: paths.page500 },
        ],
      },
    ],
  },
];
