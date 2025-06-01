import React from 'react';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';

const Footer = () => (
    <Box component="footer" sx={{ py: 1, px: 0, mt: 'auto', display: 'flex',
      textAlign: 'center' }}>
      <Container maxWidth="sm">
        <Typography variant="caption">
          © {new Date().getFullYear()} OpenTCM. All rights reserved.
        </Typography>
      </Container>
    </Box>
  );

export default Footer;
