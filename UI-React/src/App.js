import React, { useState,useContext,useEffect } from 'react';
import { ThemeProvider, CssBaseline, Container, Box, AppBar, Toolbar, Typography ,CircularProgress} from '@mui/material';
import {darkTheme,lightTheme} from './theme';
import StockList from './Components/StockList';
import StockChart from './Components/StockChart';
import { LoadingProvider, LoadingContext } from './Service/LoadingContext';
import './Components/css/StockList.css';


const AppContent = () => {
  const [selectedStock, setSelectedStock] = useState(null);
  const { loading } = useContext(LoadingContext); 
  const handleStockSelect = (symbol) => {
    setSelectedStock(symbol);
  };
  const handleBack = () => {
    setSelectedStock(null);
  };

  return (
   
    <ThemeProvider theme={lightTheme}>
      
      <CssBaseline />
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">
            Stock Market
          </Typography>
        </Toolbar>
      </AppBar>
      <Container>
   
        <Box my={4}>
        {loading && (
                        <div className="loading-overlay">
                            <CircularProgress />
                        </div>
                    )}
        {selectedStock ? (
        <StockChart symbol={selectedStock} onBack={handleBack} />
      ) : (
        <StockList onStockSelect={handleStockSelect} />
      )}
    
        </Box>
         
       
      
   
      </Container>
    </ThemeProvider>
   
  );
};
const App = () => {
  return (
    <LoadingProvider>
      <AppContent />
    </LoadingProvider>
  );
};

export default App;