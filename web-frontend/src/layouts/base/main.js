import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import { useResponsive } from 'src/hooks/use-responsive';
import { useSettingsContext } from 'src/components/settings';
import Footer from '../../components/footer/Footer';

// ----------------------------------------------------------------------

const SPACING = 8;

export const HEADER = {
  H_MOBILE: 80,
  H_DESKTOP: 64,
  H_MOBILE_OFFSET: 0,
  H_DESKTOP_OFFSET: 0,
};

export default function Main({ children, hideFooter = false, sx, ...other }) {
  const settings = useSettingsContext();
  const lgUp = useResponsive('up', 'lg');
  const isNavHorizontal = settings.themeLayout === 'horizontal';

  return (
    <Box
      component="main"
      sx={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        pt: `${HEADER.H_MOBILE_OFFSET}px`,
        pb: 0,
        ...(lgUp && {
          pt: `${HEADER.H_DESKTOP_OFFSET}px`,
          pb: 0,
        }),
        ...sx,
      }}
      {...other}
    >
      {children}
      {!hideFooter && <Footer />}
    </Box>
  );
}

Main.propTypes = {
  children: PropTypes.node,
  hideFooter: PropTypes.bool,
  sx: PropTypes.object,
};
