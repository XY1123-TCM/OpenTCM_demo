import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import Divider from '@mui/material/Divider';
import Link from 'next/link';

export const metadata = {
  title: 'Disclaimer',
};

function DisclaimerPage() {
  return (
    <Container maxWidth="lg" sx={{ padding: '20px' }}>
      <Grid item xs={8} md={9}>
        <Box sx={{ mb: 4 }}>
          <Box id="disclaimer" sx={{ mb: 4 }}>
            <Typography variant="h2" sx={{ mb: 4 }}>Disclaimer</Typography>
            <Typography variant="body1">
              The responses provided by OpenTCM are based on existing knowledge of Traditional Chinese Medicine (TCM).
              While we strive to offer accurate and up-to-date information, TCM practices and knowledge can vary, and
              uncertainties may still exist. The information provided should not be considered as a substitute for
              professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider
              for any medical concerns or before starting any new treatment. OpenTCM disclaims any liability for
              decisions made based on the information provided.
            </Typography>
            <Typography variant="body1" sx={{ textAlign: 'right', mt: 4 }}>
              - OpenTCM Team
            </Typography>
          </Box>
        </Box>
      </Grid>
    </Container>
  );
}

export default function Page() {
  return <DisclaimerPage />;
}
