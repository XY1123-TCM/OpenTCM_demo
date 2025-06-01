'use client';

import PropTypes from 'prop-types';

import { GuestGuard } from 'src/auth/guard';
import SearchLayout from 'src/layouts/search';
import BaseLayout from '../../layouts/base';

// ----------------------------------------------------------------------

export default function Layout({ children }) {
  return (
    <GuestGuard>
      <BaseLayout hideFooter={true}>{children}</BaseLayout>
    </GuestGuard>
  );
}

Layout.propTypes = {
  children: PropTypes.node,
};
