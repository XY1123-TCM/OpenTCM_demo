'use client';

import PropTypes from 'prop-types';

import { GuestGuard } from 'src/auth/guard';
import SearchLayout from 'src/layouts/search';

// ----------------------------------------------------------------------

export default function Layout({ children }) {
  return (
    <GuestGuard>
      <SearchLayout>{children}</SearchLayout>
    </GuestGuard>
  );
}

Layout.propTypes = {
  children: PropTypes.node,
};
