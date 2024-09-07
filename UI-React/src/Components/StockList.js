// StockList.js
import React, { useState, useEffect } from 'react';
import { Paper } from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import useApiService from '../Service/ApiService';
import { TextField,Box } from '@mui/material';
import './css/StockList.css'; // Import the CSS file

const StockList = ({ onStockSelect }) => {
    const apiService = useApiService();
    const [stocks, setStocks] = useState([]);
    const [paginationModel, setPaginationModel] = useState({ page: 0, pageSize: 50 });
  
    
        const getData = async () => {
            try {
               
                const data =await apiService.get('load_data');
                

                data.forEach((item, index) => {
                    item.ID = index + 1;
                });
                setStocks(data);
            } catch (error) {
                console.error('Error fetching stocks:', error);
            }
        };

       
        useEffect(() => {
            getData();
        }, []); 
  const handleSearch = async (searchValue) => {
    try {
       
        
        const data = await apiService.post('process_stock_code', { stock_code: searchValue });
        setStocks(data);
        
        
        onStockSelect(searchValue);
    } catch (error) {
        console.error('Error searching stocks:', error);
    }
};

  return (
    
    <Box>
    <TextField
    sx={{ marginBottom: '20px' }}
                label="Search"
                variant="outlined"
                fullWidth
                onKeyPress={(event) => {
                    if (event.key === 'Enter') {
                        handleSearch(event.target.value);
                    }
                }}
            />
   
   <Paper sx={{ height: 400, width: '100%', backgroundColor: '#ffffff', boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)', borderRadius: '8px', overflow: 'hidden' }}>
  <DataGrid
    rows={stocks}
    columns={[
      { field: 'Date', headerName: 'Date', width: 150 },
      { field: 'Symbol', headerName: 'Stock', width: 150 },
      { field: 'Uptrend', headerName: 'Up Trend', width: 100,cellClassName: (params) => {
        return params.value > 50 ?  'green-cell':'red-cell';
    } },
      { field: 'NeutralTrend', headerName: 'Neutral', width: 100,
        cellClassName: (params) => {
            return params.value > 20 ? 'red-cell' : 'green-cell';
        } },
      { field: 'Downtrend', headerName: 'Down Trend', width: 100,
        cellClassName: (params) => {
            return params.value > 20 ? 'red-cell' : 'green-cell';
        },
      },
      { field: 'rating', headerName: 'Rating', width: 100,
        cellClassName: (params) => {
            return params.value > 6 ?  'green-cell':'red-cell' ;
        }
        },
    ]}
    sortModel={[
      {
        field: 'Uptrend',
        sort: 'desc',
      },
    ]}
    getRowId={(row) => row.ID}
    paginationModel={paginationModel}
    onPaginationModelChange={(model) => setPaginationModel(model)}
    pageSizeOptions={[5, 10,100]}
    onRowClick={(params) => onStockSelect(params.row.Symbol)}
    sx={{
      border: 0,
      '& .MuiDataGrid-columnHeaders': {
        backgroundColor: '#f5f5f5', // Light gray for column headers
        color: '#212121', // Dark color for header text
        fontWeight: 'bold',
        fontSize: '14px',
        borderBottom: '1px solid #e0e0e0', // Subtle border below headers
      },
      '& .MuiDataGrid-cell': {
        
        fontSize: '13px',
        borderBottom: '1px solid #f0f0f0', // Subtle border for cells
      },
      '& .MuiDataGrid-row:hover': {
        backgroundColor: '#f0f8ff', // Light blue background on hover for better visibility
      },
      '& .MuiDataGrid-footerContainer': {
        backgroundColor: '#f5f5f5', // Light gray footer for pagination controls
        borderTop: '1px solid #e0e0e0', // Subtle top border for footer
      },
      '& .MuiDataGrid-columnSeparator': {
        display: 'none', // Hides column separators for a cleaner look
      },
      '& .MuiDataGrid-virtualScroller': {
        overflowX: 'hidden', // Prevents horizontal scrolling
      },
    }}
  />
</Paper>

     </Box>
  );
};

export default StockList;