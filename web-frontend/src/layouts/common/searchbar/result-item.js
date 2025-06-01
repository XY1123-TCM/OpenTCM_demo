import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import { alpha } from '@mui/material/styles';
import ListItemText from '@mui/material/ListItemText';
import ListItemButton from '@mui/material/ListItemButton';
import Link from '@mui/material/Link';
import Label from 'src/components/label';

export default function ResultItem({ title, path, description, groupLabel, onClickItem }) {
  return (
    <ListItemButton
      onClick={onClickItem}
      sx={{
        borderWidth: 1,
        borderStyle: 'dashed',
        borderColor: 'transparent',
        borderBottomColor: (theme) => theme.palette.divider,
        '&:hover': {
          borderRadius: 1,
          borderColor: (theme) => theme.palette.primary.main,
          backgroundColor: (theme) =>
            alpha(theme.palette.primary.main, theme.palette.action.hoverOpacity),
        },
      }}
    >
      <ListItemText
        primary={
          <Link href={path} variant="subtitle2" underline="hover" sx={{ textTransform: 'capitalize' }}>
            {title.map((part, index) => (
              <Box
                key={index}
                component="span"
                sx={{
                  color: part.highlight ? 'primary.main' : 'text.primary',
                }}
              >
                {part.text}
              </Box>
            ))}
          </Link>
        }
        secondary={
          description && (
            <Box sx={{ display: 'flex', flexDirection: 'column' }}>
              {description.map((part, index) => (
                <Box
                  key={index}
                  component="span"
                  sx={{
                    color: part.highlight ? 'primary.main' : 'text.secondary',
                  }}
                >
                  {part.text}
                </Box>
              ))}
            </Box>
          )
        }
      />
      {groupLabel && <Label color="info">{groupLabel}</Label>}
    </ListItemButton>
  );
}

ResultItem.propTypes = {
  title: PropTypes.array.isRequired,
  path: PropTypes.string.isRequired,
  description: PropTypes.array,
  groupLabel: PropTypes.string,
  onClickItem: PropTypes.func,
};
