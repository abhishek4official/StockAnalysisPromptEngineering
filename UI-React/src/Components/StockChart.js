// StockChart.js
import React, { useState, useEffect, useRef } from 'react';
import Plot from 'react-plotly.js';
import useApiService from '../Service/ApiService';
import { Button, Box,Paper,Typography,Chip ,LinearProgress} from '@mui/material';
import ReactMarkdown from 'react-markdown';
import LightweightChart from './LightweightChart';
import PlottyStockChart from './PlottyChart';

const StockChart = ({ symbol ,onBack}) => {
    const apiService = useApiService();
  const [data, setData] = useState([]);
  const [markdownText, setmarkdownText] = useState("")
const [CurrentPrice, setCurrentPrice] = useState(0);
const [CurrentChange, setCurrentChange] = useState(0);
const [CurrentChangePer, setCurrentChangePer] = useState(0);
const [UpTrend, setUpTrend] = useState(0);
const [DownTrend, setDownTrend] = useState(0);
const [NeutralTrend, setNeutralTrend] = useState(0);
const [Rateing, setRateing] = useState(0);
const [Summery, setSummery] = useState("");
  const [candlestickData, setcandlestickData] = useState([]);
  const [layout, setlayout] = useState([]);
  const chartRef = useRef(null);
  
  
  let isrunning = false;

  useEffect(() => {
    
   console.log(symbol);
    const fetchStockData = async () => {
      
      const response = await apiService.post('get_stock_data', { stock_code: symbol });
      if(response.prompt.length > 0){
        try {
            const sortedPrompt = response.prompt.sort((a, b) => new Date(b.date) - new Date(a.date));
            setUpTrend(sortedPrompt[0].Uptrend);
            setNeutralTrend(sortedPrompt[0].NeutralTrend);
            setDownTrend(sortedPrompt[0].Downtrend);
            setRateing(sortedPrompt[0].rating);
            setSummery(sortedPrompt[0].Summary);
            if (sortedPrompt[0] && sortedPrompt[0].Markdown) {
                setmarkdownText(sortedPrompt[0].Markdown);
            } else {
              console.error("No valid Markdown found in the sorted prompt.");
            }
           
          } catch (error) {
            console.error("Error sorting prompts or setting markdown text:", error);
          }
      } 
      const formattedData = response.stock.map(item => ({
        date: new Date(item.Date),
        open: item.Open,
        high: item.High,
        low: item.Low,
        close: item.Close
      }));
    const sortedData = formattedData.sort((a, b) => b.date - a.date);
    const lastTwoItems = sortedData.slice(0, 2);
      setCurrentPrice(lastTwoItems[0].close);
      setCurrentChangePer(((lastTwoItems[0].close - lastTwoItems[1].close) / lastTwoItems[1].close) * 100);
      setCurrentChange(lastTwoItems[0].close - lastTwoItems[1].close);
      
      console.log(formattedData);
      setData(formattedData);
      isrunning = false;
      console.log("1", isrunning);
    };

    fetchStockData();

  }, [symbol]);

  useEffect(() => {
   
    if (data.length === 0) return;
    const filteredData = data;
    console.log(symbol);
    const candlestickData = [
      {
        x: filteredData.map(item => item.date),
        close: filteredData.map(item => item.close),
        decreasing: { line: { color: 'red' } },
        high: filteredData.map(item => item.high),
        increasing: { line: { color: 'green' } },
        low: filteredData.map(item => item.low),
        open: filteredData.map(item => item.open),
        type: 'candlestick',
        xaxis: 'x',
        yaxis: 'y'
      }
    ];
    
    const layout = {
        xaxis: {
          title: {
            text: 'Date',
            font: {
              family: 'Roboto, Arial, sans-serif',
              size: 12,
              color: '#212121', // Darker color for axis title
            },
          },
          showgrid: true,
          gridcolor: '#e0e0e0', // Light grid color for better contrast on light background
          tickcolor: '#757575', // Subtle tick color
          tickfont: {
            family: 'Roboto, Arial, sans-serif',
            size: 10,
            color: '#757575', // Medium gray for tick labels
          },
        },
        yaxis: {
          title: {
            text: 'Price',
            font: {
              family: 'Roboto, Arial, sans-serif',
              size: 12,
              color: '#212121', // Darker color for axis title
            },
          },
          showgrid: true,
          gridcolor: '#e0e0e0', // Light grid color for better contrast
          tickcolor: '#757575', // Subtle tick color
          tickfont: {
            family: 'Roboto, Arial, sans-serif',
            size: 10,
            color: '#757575', // Medium gray for tick labels
          },
        },
        plot_bgcolor: '#f4f6f8', // Matches the light theme background color
        paper_bgcolor: '#ffffff', // White paper background for contrast
        margin: {
          l: 60, // Slightly increased left margin for y-axis title
          r: 20,
          t: 50, // Increased top margin for better title spacing
          b: 40, // Increased bottom margin for x-axis labels
        },
        font: {
          family: 'Roboto, Arial, sans-serif',
          size: 12,
          color: '#212121', // Darker font color for all texts
        },
        title: {
          text: 'Stock Price Chart',
          font: {
            family: 'Montserrat, sans-serif',
            size: 16,
            color: '#212121', // Dark color for the title to match light theme
          },
          x: 0.5,
          xanchor: 'center',
        },
      };
      
      setcandlestickData(candlestickData);
      setlayout(layout);
    chartRef.current = { candlestickData, layout };
  }, [data]);
  return (
    <Box display="grid" gridTemplateColumns="1fr" gap={4} padding={4}>
     
        <Box display="grid" gridTemplateColumns="1fr 1fr" gap={4}>
            <Box>
            <Button variant="contained" onClick={onBack} style={{ float: 'left', marginTop: '21px' }}>
                Back
            </Button>
            <Box style={{height:"85px"}}>
                <h2 style={{ float: 'right' }}><a href={`https://www.tradingview.com/chart/?symbol=${symbol}`} target='_blank'> {symbol}</a> 
                <Chip 
                            label={`Rating: ${Rateing}`} 
                            color={Rateing > 7 ? "success" : "error"} 
                            size="small" 
                            style={{ marginLeft: '10px' }} 
                        /></h2>
              </Box>
                <Box
                    sx={{
                        display: 'flex',
                        flexWrap: 'wrap',
                        gap: 2,
                        '& > :not(style)': {
                            width: '100%',
                            maxWidth: '30%',
                            height: '100px',
                        },
                    }}
                >
                    <Paper elevation={3} sx={{ padding: 2, marginBottom: 2 }}>
                        <Typography variant="h6">Price</Typography>
                        <Typography variant="body1" style={{ color: CurrentChange > 0 ? 'green' : 'red' }}>
                            {CurrentPrice.toFixed(2)}
                        </Typography>
                    </Paper>
                    <Paper elevation={3} sx={{ padding: 2, marginBottom: 2 }}>
                        <Typography variant="h6">Change</Typography>
                        <Typography variant="body1" style={{ color: CurrentChange > 0 ? 'green' : 'red' }}>
                            {CurrentChange.toFixed(2)}
                        </Typography>
                    </Paper>
                    <Paper elevation={3} sx={{ padding: 2, marginBottom: 2 }}>
                        <Typography variant="h6">Change %</Typography>
                        <Typography variant="body1" style={{ color: CurrentChange > 0 ? 'green' : 'red' }}>
                            {CurrentChangePer.toFixed(2)}%
                        </Typography>
                    </Paper>
                </Box>
                <Box
                    sx={{
                        display: 'flex',
                        flexWrap: 'wrap',
                        gap: 2,
                        '& > :not(style)': {
                            width: '100%',
                            maxWidth: '30%',
                            height: '100px',
                        },
                    }}
                >
                    <Paper elevation={3} sx={{ padding: 2, marginBottom: 2 }}>
                        <Typography variant="h6">Up Trend</Typography>
                        <Typography variant="body1" style={{ color: 'green' }}>
                            {UpTrend.toFixed(0)}%
                        </Typography>
                        <Typography variant="body1">
                        <LinearProgress
                            variant="determinate"
                            value={UpTrend}
                            sx={{
                                flexGrow: 1,
                                margin: '0 10px',
                                height: '10px',
                                backgroundColor: 'lightgray',
                                '& .MuiLinearProgress-bar': {
                                    backgroundColor: 'green',
                                },
                            }}
                        />
                        </Typography>
                    </Paper>
                    <Paper elevation={3} sx={{ padding: 2, marginBottom: 2 }}>
                        <Typography variant="h6">Side Trend</Typography>
                        <Typography variant="body1">
                            {NeutralTrend.toFixed(0)}%
                        </Typography>
                        <Typography variant="body1">
                        <LinearProgress
                            variant="determinate"
                            value={NeutralTrend}
                            sx={{
                                flexGrow: 1,
                                margin: '0 10px',
                                height: '10px',
                                backgroundColor: 'lightgray',
                                '& .MuiLinearProgress-bar': {
                                    backgroundColor: 'gray',
                                },
                            }}
                        />
                        </Typography>
                    </Paper>
                    <Paper elevation={3} sx={{ padding: 2, marginBottom: 2 }}>
                        <Typography variant="h6">Down Trend</Typography>
                        <Typography variant="body1" style={{ color: 'red' }}>
                            {DownTrend.toFixed(0)}%
                        </Typography>
                        <Typography variant="body1">
                        <LinearProgress
                            variant="determinate"
                            value={DownTrend}
                            sx={{
                                flexGrow: 1,
                                margin: '0 10px',
                                height: '10px',
                                backgroundColor: 'lightgray',
                                '& .MuiLinearProgress-bar': {
                                    backgroundColor: 'red',
                                },
                            }}
                        />
                        </Typography>
                    </Paper>
                
                </Box>
                <Box>
                
                <strong>Summery:</strong> {Summery}
                </Box>
            </Box>
            <Box sx={{ padding: 2, maxWidth: '100%' }}>
                {chartRef.current && (
                    <div style={{ width: '100%', height: '100%' }}>
                        {<LightweightChart symbol={symbol} rating={Rateing} data={data} />
                        /* <Plot
                            key={symbol} // Force re-render when symbol changes
                            data={chartRef.current.candlestickData}
                            layout={{ ...chartRef.current.layout, autosize: true }}
                            useResizeHandler={true}
                            style={{ width: '100%', height: '100%' }}
                        /> */}
                    </div>
                )}
            </Box>
        </Box>
        <Box>
            {markdownText ? (
                <ReactMarkdown>{markdownText}</ReactMarkdown>
            ) : (
                <div>No markdown text found</div>
            )}
        </Box>
        <Box sx={{ padding: 2, maxWidth: '100%' }}>
        <PlottyStockChart data={data} />
</Box>
    </Box>
);
};

export default StockChart;