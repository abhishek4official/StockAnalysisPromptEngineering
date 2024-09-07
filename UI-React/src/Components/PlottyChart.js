import React, { useMemo } from 'react';
import Plot from 'react-plotly.js';
import {
  calculateMACD,
  calculateADX,
  calculateBollingerBands,
  calculateMovingAverage,
} from '../Service/stockIndicator';

const PlottyStockChart = ({ data = [] }) => {
  // Memoize calculations to prevent unnecessary re-computations
  const { formattedData, movingAverageData,  bollingerBands } = useMemo(() => {
    if (!data || data.length === 0) {
        return { formattedData: [], movingAverageData: [], bollingerBands: [] };
      }
      
      const formattedData = data.map(item => {
        const date = new Date(item.date);
        if (isNaN(date.getTime())) {
          console.error(`Invalid date: ${item.date}`);
          return null;
        }
        return {
          time: date.toISOString().split('T')[0], // Convert to 'YYYY-MM-DD' format
          open: item.open,
          high: item.high,
          low: item.low,
          close: item.close,
        };
      }).filter(item => item !== null); // Filter out invalid data points
      formattedData.sort((a, b) => new Date(a.time) - new Date(b.time));
      // Calculate indicators
      const movingAverageData = calculateMovingAverage(formattedData);
      const bollingerBands = calculateBollingerBands(formattedData);

    return { formattedData, movingAverageData,  bollingerBands };
  }, [data]);

  const candlestickData = [
    {
      x: formattedData.map(item => item.time),
      close: formattedData.map(item => item.close),
      decreasing: { line: { color: 'red' } },
      high: formattedData.map(item => item.high),
      increasing: { line: { color: 'green' } },
      low: formattedData.map(item => item.low),
      open: formattedData.map(item => item.open),
      type: 'candlestick',
      xaxis: 'x',
      yaxis: 'y',
    },
  ];

  const movingAverageTrace = {
    x: movingAverageData.map(item => item.time),
    y: movingAverageData.map(item => item.value),
    type: 'scatter',
    mode: 'lines',
    name: 'Moving Average',
    line: { color: 'blue' },
  };

  

  const bollingerBandsUpperTrace = {
    x: bollingerBands.map(item => item.time),
    y: bollingerBands.map(item => item.upper),
    type: 'scatter',
    mode: 'lines',
    name: 'Bollinger Bands Upper',
    line: { color: 'grey', dash: 'dash' },
  };

  const bollingerBandsLowerTrace = {
    x: bollingerBands.map(item => item.time),
    y: bollingerBands.map(item => item.lower),
    type: 'scatter',
    mode: 'lines',
    name: 'Bollinger Bands Lower',
    line: { color: 'grey', dash: 'dash' },
  };

  const layout = {
    xaxis: {
      title: {
        text: 'Date',
        font: {
          family: 'Roboto, Arial, sans-serif',
          size: 12,
          color: '#212121',
        },
      },
      showgrid: true,
      gridcolor: '#e0e0e0',
      tickcolor: '#757575',
      tickfont: {
        family: 'Roboto, Arial, sans-serif',
        size: 10,
        color: '#757575',
      },
    },
    yaxis: {
      title: {
        text: 'Price',
        font: {
          family: 'Roboto, Arial, sans-serif',
          size: 12,
          color: '#212121',
        },
      },
      showgrid: true,
      rangeslider: { visible: false },
      gridcolor: '#e0e0e0',
      tickcolor: '#757575',
      tickfont: {
        family: 'Roboto, Arial, sans-serif',
        size: 10,
        color: '#757575',
      },
    },
    yaxis2: {
      title: 'MACD',
      overlaying: 'y',
      side: 'right',
      showgrid: false,
      zeroline: false,
    },
    yaxis3: {
      title: 'ADX',
      overlaying: 'y',
      side: 'right',
      position: 0.95,
      showgrid: false,
      zeroline: false,
    },
    plot_bgcolor: '#f4f6f8',
    paper_bgcolor: '#ffffff',
    margin: {
      l: 60,
      r: 60,
      t: 50,
      b: 40,
    },
    font: {
      family: 'Roboto, Arial, sans-serif',
      size: 12,
      color: '#212121',
    },
    title: {
      text: 'Stock Price Chart',
      font: {
        family: 'Montserrat, sans-serif',
        size: 16,
        color: '#212121',
      },
      x: 0.5,
      xanchor: 'center',
    },
    rangeslider: { visible: false },
  };

  return (
    <Plot
      data={[
        ...candlestickData,
        movingAverageTrace,
       
        bollingerBandsUpperTrace,
        bollingerBandsLowerTrace,
      ]}
      layout={{ ...layout, autosize: true }}
      useResizeHandler={true}
      style={{ width: '100%', height: '100%' }}
    />
  );
};

export default PlottyStockChart;