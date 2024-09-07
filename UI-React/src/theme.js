// src/theme.js
import { createTheme } from '@mui/material/styles';

// Light Theme
const lightTheme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2', // Blue for primary color
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#f50057', // Pink for secondary color
      contrastText: '#ffffff',
    },
    background: {
      default: '#f4f6f8', // Light gray background
      paper: '#ffffff', // White for paper elements
    },
    text: {
      primary: '#212121', // Dark color for primary text
      secondary: '#757575', // Medium gray for secondary text
      disabled: '#bdbdbd', // Light gray for disabled text
    },
  },
  typography: {
    fontFamily: "'Roboto', 'Arial', sans-serif",
    fontSize: 14,
    h1: {
      fontFamily: "'Montserrat', sans-serif",
      fontWeight: 700,
      fontSize: '2.5rem',
      lineHeight: 1.2,
      color: '#212121',
    },
    h2: {
      fontFamily: "'Montserrat', sans-serif",
      fontWeight: 600,
      fontSize: '2rem',
      lineHeight: 1.3,
      color: '#212121',
    },
    body1: {
      fontSize: '1rem',
      color: '#212121',
    },
    button: {
      textTransform: 'none',
      fontWeight: 600,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '8px',
          boxShadow: '0px 2px 4px -1px rgba(0,0,0,0.1)',
          '&:hover': {
            backgroundColor: '#1565c0',
            boxShadow: '0px 4px 8px -2px rgba(0,0,0,0.2)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundColor: '#ffffff',
          borderRadius: '8px',
          boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
        },
      },
    },
  },
});

// Dark Theme
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#64b5f6',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#ff4081',
      contrastText: '#ffffff',
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
    text: {
      primary: '#e0f7fa',
      secondary: '#b0bec5',
      disabled: '#757575',
    },
  },
  typography: {
    fontFamily: "'Roboto', 'Arial', sans-serif",
    fontSize: 14,
    h1: {
      fontFamily: "'Montserrat', sans-serif",
      fontWeight: 700,
      fontSize: '2.5rem',
      lineHeight: 1.2,
      color: '#ffffff',
    },
    h2: {
      fontFamily: "'Montserrat', sans-serif",
      fontWeight: 600,
      fontSize: '2rem',
      lineHeight: 1.3,
      color: '#e0f7fa',
    },
    body1: {
      fontSize: '1rem',
      color: '#e0f7fa',
    },
    button: {
      textTransform: 'none',
      fontWeight: 600,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '8px',
          boxShadow: '0px 3px 5px -1px rgba(0,0,0,0.2)',
          '&:hover': {
            backgroundColor: '#82b1ff',
            boxShadow: '0px 5px 8px -2px rgba(0,0,0,0.3)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundColor: '#1d1d1d',
          borderRadius: '8px',
          boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.2)',
        },
      },
    },
  },
});

export { lightTheme, darkTheme };
