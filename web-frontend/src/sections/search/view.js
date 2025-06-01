'use client';

import Box from '@mui/material/Box';
import { alpha } from '@mui/material/styles';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Paper from '@mui/material/Paper';
import IconButton from '@mui/material/IconButton';
import { useState, useCallback } from 'react';
import { useSettingsContext } from 'src/components/settings';
import { useRouter } from 'next/navigation';
import Iconify from 'src/components/iconify';
import Button from '@mui/material/Button';

export default function SearchView() {
  const settings = useSettingsContext();
  const [searchQuery, setSearchQuery] = useState('');
  const [suggestions, setSuggestions] = useState({ herbs: [], treatments: [] });
  const router = useRouter();

  const fetchSuggestions = useCallback((query) => {
    if (query.trim()) {
      fetch(`/api/suggestions?query=${encodeURIComponent(query.trim())}`)
        .then((response) => response.json())
        .then((data) => setSuggestions(data))
        .catch((error) => console.error('Error fetching suggestions:', error));
    } else {
      setSuggestions({ herbs: [], treatments: [] });
    }
  }, []);

  const handleSearch = useCallback(() => {
    if (searchQuery.trim()) {
      router.push(`/search/result/?q=${encodeURIComponent(searchQuery)}`);
    }
  }, [searchQuery, router]);

  const handleChatWithMe = () => {
    if (searchQuery.trim()) {
      router.push(`/chat?query=${encodeURIComponent(searchQuery)}`);
    } else {
      router.push(`/chat`);
    }
  };

  const handleKeyDown = useCallback((event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  }, [handleSearch]);

  const handleInputChange = useCallback((event) => {
    const value = event.target.value;
    setSearchQuery(value);
    fetchSuggestions(value);
  }, [fetchSuggestions]);

  const handleClickSuggestion = useCallback((path) => {
    router.push(path);
  }, [router]);

  const renderSuggestions = () => {
    const { herbs, treatments } = suggestions;

    if (herbs.length === 0 && treatments.length === 0) {
      return null;
    }

    const renderList = (items, type) => (
      items.map((item) => {
        const path = type === 'herb' ? `/ref/herb/?herb=${item.name}` : `/ref/treatment/?treatment=${item.name}`;
        const icon = type === 'herb' ? 'mdi:leaf' : 'mdi:pill';
        return (
          <ListItem key={`${item.name}${item.id}`} disablePadding>
            <ListItemButton onClick={() => handleClickSuggestion(path)}>
              <Box sx={{ mr: 2 }}>
                <Iconify icon={icon} width={24} />
              </Box>
              <ListItemText primary={item.name} />
            </ListItemButton>
          </ListItem>
        );
      })
    );

    return (
      <Box sx={{
        width: '100%',
        maxWidth: 600,
        mt: 1,
        position: 'absolute',
        bgcolor: 'background.paper',
        zIndex: 2,
        top: '60px',
        borderRadius: 1,
        boxShadow: 3,
      }}>
        <List disablePadding>
          {renderList(herbs, 'herb')}
          {renderList(treatments, 'treatment')}
        </List>
      </Box>
    );
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '50vh' }}>
      <Container
        maxWidth={settings.themeStretch ? false : 'xl'}
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          flexGrow: 1,
          position: 'relative',
        }}
      >
        <Box
          component="img"
          src="/assets/icons/home/Home-Icon.jpg"
          alt="OpenTCM Home Icon"
          sx={{
            mb: 4,
            width: 500,
            boxShadow: 15,
            borderRadius: 0.5,
          }}
        />
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            width: '100%',
            maxWidth: 600,
            position: 'relative',
          }}
        >
          <TextField
            variant="outlined"
            placeholder="Search..."
            fullWidth
            value={searchQuery}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            sx={{
              mb: 2,
              '.MuiOutlinedInput-root': {
                borderRadius: '50px',
                padding: '5px 20px',
                bgcolor: (theme) => alpha(theme.palette.common.white, 0.25),
                '&.Mui-focused': {
                  bgcolor: (theme) => alpha(theme.palette.common.white, 0.35),
                },
              },
            }}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <IconButton>
                    <Iconify icon="eva:search-fill" width={24} sx={{ color: 'text.disabled' }} />
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />
          {renderSuggestions()}
          {/*  create two buttons: Search and Chat with me */}
          <Box sx={{ display: 'flex', gap: 2, zIndex: 1 }}>
            <Button variant="contained" sx={{ borderRadius: '50px', padding: '10px 30px' }}
                    onClick={handleSearch}>Search </Button>
            <Button variant="contained" sx={{ borderRadius: '50px', padding: '10px 30px' }}
                    onClick={handleChatWithMe}>Chat with me</Button>
          </Box>
        </Box>
      </Container>
    </Box>
  );
}
