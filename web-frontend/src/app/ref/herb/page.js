'use client';

import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import Grid from '@mui/material/Grid';
import Divider from '@mui/material/Divider';

function HerbInfo() {
  const searchParams = useSearchParams();
  const query = searchParams.get('herb');

  const [herbInfo, setHerbInfo] = useState(null);

  useEffect(() => {
    if (query) {
      fetch(`/api/herb/?herb=${query}`)
        .then((response) => response.json())
        .then((data) => setHerbInfo(data));
    }
  }, [query]);

  // if data is {'error': 'Herb not found'} then show herb not found page
  if (herbInfo && herbInfo.error) {
    return (
      <Container maxWidth="lg" sx={{ padding: '20px' }}>
        <Typography variant="h3">Herb Not Found</Typography>
        <Typography variant="body1">The herb you are looking for does not exist in our database.</Typography>
      </Container>
    );
  }

  if (!herbInfo) {
    return (
      <Container maxWidth="lg" sx={{ padding: '20px' }}>
        <Typography variant="h3">Herb List</Typography>

      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ padding: '20px' }}>
      <Grid container spacing={2}>
        <Grid item xs={12} md={3}>
          <Box sx={{ position: 'sticky', top: '20px' }}>
            <Typography variant="h6" sx={{ mb: 2 }}>Contents</Typography>
            <Divider />
            <Box sx={{ display: 'flex', flexDirection: 'column', mt: 2 }}>
              <Link href="#description" passHref>
                <Typography variant="body1" sx={{ mb: 1, cursor: 'pointer', color: 'blue' }}>Description</Typography>
              </Link>
              <Link href="#uses" passHref>
                <Typography variant="body1" sx={{ mb: 1, cursor: 'pointer', color: 'blue' }}>Treatment Uses</Typography>
              </Link>
            </Box>
          </Box>
        </Grid>

        <Grid item xs={12} md={9}>
          <Box sx={{ mb: 4 }}>
            <Typography variant="h2" sx={{ mb: 4 }}>{herbInfo.name}</Typography>

            <Box id="description" sx={{ mb: 4 }}>
              <Typography variant="h5" sx={{ mb: 2 }}>Description</Typography>
              <Typography variant="body1">{herbInfo.description || 'No description available.'}</Typography>
            </Box>

            <Box id="details" sx={{ mb: 4 }}>
              <Typography variant="h5" sx={{ mb: 2 }}>Herb Details</Typography>
              <Typography variant="body1"><strong>Pinyin Name:</strong> {herbInfo.herb_pinyin_name}</Typography>
              <Typography variant="body1"><strong>English Name:</strong> {herbInfo.herb_en_name}</Typography>
              <Typography variant="body1"><strong>Latin Name:</strong> {herbInfo.herb_latin_name}</Typography>
              <Typography variant="body1"><strong>Properties:</strong> {herbInfo.properties}</Typography>
              <Typography variant="body1"><strong>Meridians:</strong> {herbInfo.meridians}</Typography>
              <Typography variant="body1"><strong>Use Part:</strong> {herbInfo.UsePart}</Typography>
              <Typography variant="body1"><strong>Function:</strong> {herbInfo.function}</Typography>
              <Typography variant="body1"><strong>Indication:</strong> {herbInfo.indication}</Typography>
              <Typography variant="body1"><strong>Toxicity:</strong> {herbInfo.toxicity}</Typography>
              <Typography variant="body1"><strong>Clinical Manifestations:</strong> {herbInfo.clinical_manifestations}</Typography>
              <Typography variant="body1"><strong>Therapeutic Class (EN):</strong> {herbInfo.therapeutic_en_class}</Typography>
              <Typography variant="body1"><strong>Therapeutic Class (CN):</strong> {herbInfo.therapeutic_cn_class}</Typography>
              <Typography variant="body1"><strong>TCMID ID:</strong> {herbInfo.tcmid_id}</Typography>
              <Typography variant="body1"><strong>TCM ID:</strong> {herbInfo.tcm_id_id}</Typography>
              <Typography variant="body1"><strong>SymMap ID:</strong> {herbInfo.symmap_id}</Typography>
              <Typography variant="body1"><strong>TCMSP ID:</strong> {herbInfo.tcmsp_id}</Typography>
            </Box>


            <Box id="uses" sx={{ mb: 4 }}>
              <Typography variant="h5" sx={{ mb: 2 }}>Treatment Uses</Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Name</TableCell>
                      <TableCell>Dosage</TableCell>
                      <TableCell>Preparation</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {herbInfo.treatments.map((treatment, index) => (
                      <TableRow key={index}>
                        <TableCell>
                          <Link href={`/ref/treatment/?treatment=${treatment.name}`} passHref>
                            <Typography variant="body1"
                                        sx={{ cursor: 'pointer' }}>{treatment.name}</Typography>
                          </Link>
                        </TableCell>
                        <TableCell>{treatment.dosage}</TableCell>
                        <TableCell>{treatment.preparation || 'N/A'}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Box>
          </Box>
        </Grid>
      </Grid>
    </Container>
  );
}

export default function Page() {
  return <HerbInfo />;
}
