import parse from 'autosuggest-highlight/parse';
import match from 'autosuggest-highlight/match';
import { memo, useState, useCallback } from 'react';

import Box from '@mui/material/Box';
import List from '@mui/material/List';
import Stack from '@mui/material/Stack';
import { useTheme } from '@mui/material/styles';
import InputBase from '@mui/material/InputBase';
import IconButton from '@mui/material/IconButton';
import InputAdornment from '@mui/material/InputAdornment';
import Dialog, { dialogClasses } from '@mui/material/Dialog';

import { useRouter } from 'src/routes/hooks';

import { useBoolean } from 'src/hooks/use-boolean';
import { useResponsive } from 'src/hooks/use-responsive';
import { useEventListener } from 'src/hooks/use-event-listener';

import Label from 'src/components/label';
import Iconify from 'src/components/iconify';
import Scrollbar from 'src/components/scrollbar';
import SearchNotFound from 'src/components/search-not-found';

import ResultItem from './result-item';

// ----------------------------------------------------------------------

function Searchbar() {
  const theme = useTheme();

  const router = useRouter();

  const search = useBoolean();

  const lgUp = useResponsive('up', 'lg');

  const [searchQuery, setSearchQuery] = useState('');
  const [suggestions, setSuggestions] = useState({ herbs: [], treatments: [] });

  const handleClose = useCallback(() => {
    search.onFalse();
    setSearchQuery('');
  }, [search]);

  const handleKeyDown = (event) => {
    if (event.key === 'k' && event.metaKey) {
      search.onToggle();
      setSearchQuery('');
    }
  };

  useEventListener('keydown', handleKeyDown);

  const handleClick = useCallback(
    (path) => {
      if (path.includes('http')) {
        window.open(path);
      } else {
        router.push(path);
      }
      handleClose();
    },
    [handleClose, router]
  );

  const handleSearch = useCallback((event) => {
    const value = event.target.value;
    setSearchQuery(value);

    if (value.trim()) {
      fetch(`/api/suggestions?query=${encodeURIComponent(value.trim())}`)
        .then((response) => response.json())
        .then((data) => setSuggestions(data))
        .catch((error) => console.error('Error fetching suggestions:', error));
    } else {
      setSuggestions({ herbs: [], treatments: [] });
    }
  }, []);

  const handleEnterKeyPress = useCallback((event) => {
    if (event.key === 'Enter' && searchQuery.trim()) {
      router.push(`/search/result/?q=${encodeURIComponent(searchQuery.trim())}`);
      handleClose();
    }
  }, [searchQuery, router, handleClose]);

  const renderItems = (items, group) => (
    <List disablePadding>
      {items.map((item) => {
        const partsTitle = parse(item.name, match(item.name, searchQuery));
        const path = item.type === 'herb' ? `/ref/herb/?herb=${item.name}` : `/ref/treatment/?treatment=${item.name}`;
        return (
          <ResultItem
            key={`${item.name}${item.id}`}
            path={path}
            title={partsTitle}
            description={null}
            groupLabel={group}
            onClickItem={() => handleClick(path)}
          />
        );
      })}
    </List>
  );

  const renderButton = (
    <Stack direction="row" alignItems="center">
      <IconButton onClick={search.onTrue}>
        <Iconify icon="eva:search-fill" />
      </IconButton>

      {lgUp && <Label sx={{ px: 0.75, fontSize: 12, color: 'text.secondary' }}>⌘K</Label>}
    </Stack>
  );

  return (
    <>
      {renderButton}

      <Dialog
        fullWidth
        maxWidth="sm"
        open={search.value}
        onClose={handleClose}
        transitionDuration={{
          enter: theme.transitions.duration.shortest,
          exit: 0,
        }}
        PaperProps={{
          sx: {
            mt: 15,
            overflow: 'unset',
          },
        }}
        sx={{
          [`& .${dialogClasses.container}`]: {
            alignItems: 'flex-start',
          },
        }}
      >
        <Box sx={{ p: 3, borderBottom: `solid 1px ${theme.palette.divider}` }}>
          <InputBase
            fullWidth
            autoFocus
            placeholder="Search..."
            value={searchQuery}
            onChange={handleSearch}
            onKeyPress={handleEnterKeyPress}
            startAdornment={
              <InputAdornment position="start">
                <Iconify icon="eva:search-fill" width={24} sx={{ color: 'text.disabled' }} />
              </InputAdornment>
            }
            endAdornment={<Label sx={{ letterSpacing: 1, color: 'text.secondary' }}>esc</Label>}
            inputProps={{
              sx: { typography: 'h6' },
            }}
          />
        </Box>

        <Scrollbar sx={{ p: 3, pt: 2, height: 400 }}>
          {searchQuery && !suggestions.herbs.length && !suggestions.treatments.length ? (
            <SearchNotFound query={searchQuery} sx={{ py: 10 }} />
          ) : (
            <>
              {renderItems(suggestions.herbs, 'Herbs')}
              {renderItems(suggestions.treatments, 'Treatments')}
            </>
          )}
        </Scrollbar>
      </Dialog>
    </>
  );
}

export default memo(Searchbar);
