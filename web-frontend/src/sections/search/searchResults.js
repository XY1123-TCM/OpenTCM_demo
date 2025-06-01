'use client';

import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';

export default function SearchResults() {
  const searchParams = useSearchParams();
  const query = searchParams.get('q');

  const [results, setResults] = useState({ herbs: [], treatments: [] });

  useEffect(() => {
    if (query) {
      fetch(`/api/search?query=${query}`)
        .then((response) => response.json())
        .then((data) => setResults(data));
    }
  }, [query]);

  const renderResults = (title, items) => (
    <Box sx={{ mb: 4 }}>
      <Typography variant="h5" sx={{ mb: 2 }}>{title}</Typography>
      {items.length ? (
        items.map((item) => (
          <Box key={item.id} sx={{ mb: 2 }}>
            <Link href={item.link} variant="h6" sx={{ display: 'block', mb: 1 }}>
              {item.name}
            </Link>
            <Typography variant="body2">{item.description}</Typography>
          </Box>
        ))
      ) : (
        <Typography>No results found</Typography>
      )}
    </Box>
  );

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '50vh' }}>
      <Container maxWidth="xl" sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        flexGrow: 1,
      }}>
        <Typography variant="h2" sx={{ mb: 4 }}>Search Results for "{query}"</Typography>
        <Box sx={{ width: '100%', maxWidth: 800 }}>
          {renderResults('Herbs', results.herbs)}
          {renderResults('Treatments', results.treatments)}
        </Box>
      </Container>
    </Box>
  );
}
