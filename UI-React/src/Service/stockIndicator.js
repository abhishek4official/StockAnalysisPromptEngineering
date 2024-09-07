// src/services/stockIndicators.js

// Helper function to calculate Moving Average
export const calculateMovingAverage = (data, windowSize = 5) => {
  let movingAverages = [];
  for (let i = windowSize - 1; i < data.length; i++) {
    const window = data.slice(i - windowSize + 1, i + 1);
    const average = window.reduce((acc, val) => acc + val.close, 0) / windowSize;
    movingAverages.push({ time: data[i].time, value: average });
  }
  return movingAverages;
};
  
  // Helper function to calculate MACD
  export const calculateMACD = (data, shortPeriod = 12, longPeriod = 26, signalPeriod = 9) => {
    const ema = (prices, period) => {
      const k = 2 / (period + 1);
      let emaArray = [prices[0]];
  
      for (let i = 1; i < prices.length; i++) {
        const emaValue = (prices[i] - emaArray[i - 1]) * k + emaArray[i - 1];
        emaArray.push(emaValue);
      }
  
      return emaArray;
    };
  
    const prices = data.map(item => item.close);
    const shortEma = ema(prices, shortPeriod);
    const longEma = ema(prices, longPeriod);
    const macdLine = shortEma.map((val, index) => val - longEma[index]);
    const signalLine = ema(macdLine.slice(longPeriod - 1), signalPeriod);
    const macdHistogram = macdLine.slice(longPeriod - 1).map((val, index) => val - signalLine[index]);
  
    return macdLine.slice(longPeriod - 1).map((val, index) => ({
      time: data[index + longPeriod - 1].time,
      value: val,
      signal: signalLine[index],
      histogram: macdHistogram[index],
    }));
  };
  
  // Helper function to calculate ADX
  export const calculateADX = (data, period = 14) => {
    const tr = (data) => {
      const trArray = [];
      for (let i = 1; i < data.length; i++) {
        const prev = data[i - 1];
        const current = data[i];
        const trValue = Math.max(
          current.high - current.low,
          Math.abs(current.high - prev.close),
          Math.abs(current.low - prev.close)
        );
        trArray.push(trValue);
      }
      return trArray;
    };
  
    const atr = (trArray, period) => {
      const atrArray = [];
      let sum = trArray.slice(0, period).reduce((a, b) => a + b, 0);
  
      atrArray.push(sum / period);
  
      for (let i = period; i < trArray.length; i++) {
        sum = sum - atrArray[i - period] + trArray[i];
        atrArray.push(sum / period);
      }
  
      return atrArray;
    };
  
    const plusDM = (data) => {
      const plusDMArray = [];
      for (let i = 1; i < data.length; i++) {
        const current = data[i];
        const prev = data[i - 1];
        const plusDMValue = (current.high - prev.high > prev.low - current.low && current.high > prev.high) ?
          (current.high - prev.high) : 0;
        plusDMArray.push(plusDMValue);
      }
      return plusDMArray;
    };
  
    const minusDM = (data) => {
      const minusDMArray = [];
      for (let i = 1; i < data.length; i++) {
        const current = data[i];
        const prev = data[i - 1];
        const minusDMValue = (prev.low - current.low > current.high - prev.high && prev.low < current.low) ?
          (prev.low - current.low) : 0;
        minusDMArray.push(minusDMValue);
      }
      return minusDMArray;
    };
  
    const atrArray = atr(tr(data), period);
    const plusDMArray = atr(plusDM(data), period);
    const minusDMArray = atr(minusDM(data), period);
  
    const plusDI = plusDMArray.map((value, index) => (value / atrArray[index]) * 100);
    const minusDI = minusDMArray.map((value, index) => (value / atrArray[index]) * 100);
  
    const adxArray = [];
    let prevADX = (Math.abs(plusDI[0] - minusDI[0]) / (plusDI[0] + minusDI[0])) * 100;
  
    adxArray.push({ time: data[period].time, value: prevADX });
  
    for (let i = 1; i < plusDI.length; i++) {
      const dx = (Math.abs(plusDI[i] - minusDI[i]) / (plusDI[i] + minusDI[i])) * 100;
      const adx = ((prevADX * (period - 1)) + dx) / period;
      adxArray.push({ time: data[i + period].time, value: adx });
      prevADX = adx;
    }
  
    return adxArray;
  };
  
  // Helper function to calculate Bollinger Bands
  export const calculateBollingerBands = (data, windowSize = 20, numStdDev = 2) => {
    let bollingerBands = [];
    for (let i = windowSize - 1; i < data.length; i++) {
      const window = data.slice(i - windowSize + 1, i + 1);
      const average = window.reduce((acc, val) => acc + val.close, 0) / windowSize;
      const stdDev = Math.sqrt(window.reduce((acc, val) => acc + Math.pow(val.close - average, 2), 0) / windowSize);
      const upper = average + numStdDev * stdDev;
      const lower = average - numStdDev * stdDev;
      bollingerBands.push({ time: data[i].time, upper, lower });
    }
    return bollingerBands;
  };
  