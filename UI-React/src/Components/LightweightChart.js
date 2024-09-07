import React, { useEffect, useRef } from 'react';
import { createChart } from 'lightweight-charts';
import { Box, Chip } from '@mui/material';

const LightweightChart = ({ symbol, rating, data }) => {
    const chartContainerRef = useRef(null);
    const chartRef = useRef(null);

    useEffect(() => {
        if (chartRef.current) {
            chartRef.current.remove();
        }

        const chart = createChart(chartContainerRef.current, {
            width: chartContainerRef.current.clientWidth,
            height: 500,
        });
        chartRef.current = chart;

        const candlestickSeries = chart.addCandlestickSeries();
        const formattedData = data.map(item => {
            const date = new Date(item.date);
            if (isNaN(date.getTime())) {
                console.error(`Invalid date: ${item.Date}`);
                return null;
            }
            return {
                time: date.toISOString().split('T')[0], // Convert to 'YYYY-MM-DD' format
                open: item.open,
                high: item.high,
                low: item.low,
                close: item.close
            };
        }).filter(item => item !== null); // Filter out invalid dates
        // Sort the data by time in ascending order
        formattedData.sort((a, b) => new Date(a.time) - new Date(b.time));

        candlestickSeries.setData(formattedData);

        return () => {
            if (chartRef.current) {
                chartRef.current.remove();
                chartRef.current = null;
            }
        };
    }, [data]);

    return (
        <Box>
            {/* <h2>
                <a href={`https://www.tradingview.com/chart/?symbol=${symbol}`} target='_blank' rel="noopener noreferrer">
                    {symbol}
                </a>
                <Chip
                    label={`Rating: ${rating}`}
                    color={rating > 7 ? 'success' : 'error'}
                    size="small"
                    style={{ marginLeft: '10px' }}
                />
            </h2> */}
            <Box ref={chartContainerRef} style={{ position: 'relative' }} ></Box>
        </Box>
    );
};

export default LightweightChart;