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

function TreatmentInfo() {
  const searchParams = useSearchParams();
  const query = searchParams.get('treatment');

  const [treatmentInfo, setTreatmentInfo] = useState(null);

  useEffect(() => {
    if (query) {
      fetch(`/api/treatment/?treatment=${query}`)
        .then((response) => response.json())
        .then((data) => setTreatmentInfo(data));
    }
  }, [query]);

  if (treatmentInfo && treatmentInfo.error) {
    return (
      <Container maxWidth="lg" sx={{ padding: '20px' }}>
        <Typography variant="h3">Treatment Not Found</Typography>
        <Typography variant="body1">The treatment you are looking for does not exist in our database.</Typography>
      </Container>
    );
  }

  if (!treatmentInfo) {
    return (
      <Container maxWidth="lg" sx={{ padding: '20px' }}>
        <Typography variant="h3">Loading...</Typography>
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
              <Link href="#herbs" passHref>
                <Typography variant="body1" sx={{ mb: 1, cursor: 'pointer', color: 'blue' }}>Herbs Used</Typography>
              </Link>
            </Box>
          </Box>
        </Grid>

        <Grid item xs={12} md={9}>
          <Box sx={{ mb: 4 }}>
            <Typography variant="h2" sx={{ mb: 4 }}>{treatmentInfo.name}</Typography>

            <Box id="description" sx={{ mb: 4 }}>
              <Typography variant="h5" sx={{ mb: 2 }}>Description</Typography>
              <Typography variant="body1">{treatmentInfo.notes || 'No description available.'}</Typography>
            </Box>

            <Box id="herbs" sx={{ mb: 4 }}>
              <Typography variant="h5" sx={{ mb: 2 }}>Herbs Used</Typography>
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
                    {treatmentInfo.herbs.map((herb, index) => (
                      <TableRow key={index}>
                        {/*<TableCell>{herb.name}</TableCell>*/}
                        {/*Add link to the herb /ref/herb/?herb=herb_name */}
                        <TableCell>
                          <Link href={`/ref/herb/?herb=${herb.name}`} passHref>
                            <Typography variant="body1" sx={{ cursor: 'pointer', color: 'blue' }}>{herb.name}</Typography>
                          </Link>
                        </TableCell>
                        <TableCell>{herb.dosage}</TableCell>
                        <TableCell>{herb.preparation || 'N/A'}</TableCell>
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
  return <TreatmentInfo />;
}
