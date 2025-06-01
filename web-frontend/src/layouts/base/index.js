import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import { useBoolean } from 'src/hooks/use-boolean';
import { useResponsive } from 'src/hooks/use-responsive';
import { useSettingsContext } from 'src/components/settings';
import Main from './main';
import Header from '../search/header';
import NavHorizontal from '../search/nav-horizontal';
import NavVertical from '../search/nav-vertical';

// ----------------------------------------------------------------------

export default function BaseLayout({ children, hideFooter = false }) {
  const settings = useSettingsContext();
  const lgUp = useResponsive('up', 'lg');
  const nav = useBoolean();
  const isHorizontal = settings.themeLayout === 'horizontal';

  const renderHorizontal = <NavHorizontal />;
  const renderNavVertical = <NavVertical openNav={nav.value} onCloseNav={nav.onFalse} />;

  return (
    <>
      <Header onOpenNav={nav.onTrue} />
      <>
        <Main hideFooter={hideFooter}>{children}</Main>
      </>
    </>
  );
}

BaseLayout.propTypes = {
  children: PropTypes.node,
  hideFooter: PropTypes.bool,
};
