import React, { useState } from 'react';
import './index.css';

function App() {
  const [symbol, setSymbol] = useState('BTCUSDT');
  const [side, setSide] = useState('BUY');
  const [orderType, setOrderType] = useState('MARKET');
  const [quantity, setQuantity] = useState('0.01');
  const [price, setPrice] = useState('');
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const payload = {
        symbol,
        side,
        order_type: orderType,
        quantity,
        price: orderType === 'LIMIT' ? price : undefined,
      };

      const res = await fetch('http://localhost:8000/api/order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      
      if (!res.ok) {
        throw new Error(data.detail || 'An unexpected error occurred');
      }
      
      setResult(data.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="glass-panel">
        <h1>Binance Futures Bot</h1>
        
        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label>Symbol</label>
              <input type="text" value={symbol} onChange={e => setSymbol(e.target.value.toUpperCase())} required />
            </div>
            <div className="form-group">
              <label>Side</label>
              <select value={side} onChange={e => setSide(e.target.value)}>
                <option value="BUY">BUY</option>
                <option value="SELL">SELL</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Order Type</label>
              <select value={orderType} onChange={e => setOrderType(e.target.value)}>
                <option value="MARKET">MARKET</option>
                <option value="LIMIT">LIMIT</option>
              </select>
            </div>
            <div className="form-group">
              <label>Quantity</label>
              <input type="number" step="0.001" value={quantity} onChange={e => setQuantity(e.target.value)} required />
            </div>
          </div>

          {orderType === 'LIMIT' && (
            <div className="form-group">
              <label>Price</label>
              <input type="number" step="0.01" value={price} onChange={e => setPrice(e.target.value)} required={orderType === 'LIMIT'} />
            </div>
          )}

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? <span className="spinner"></span> : 'Place Order'}
          </button>
        </form>

        {error && (
          <div className="result-container error">
            <div className="result-row">
              <span className="result-label">Error</span>
              <span className="result-value" style={{color: 'var(--error-color)'}}>{error}</span>
            </div>
          </div>
        )}

        {result && (
          <div className="result-container">
            <div className="result-row">
              <span className="result-label">Order ID</span>
              <span className="result-value">{result.order_id}</span>
            </div>
            <div className="result-row">
              <span className="result-label">Status</span>
              <span className="result-value success">{result.status}</span>
            </div>
            <div className="result-row">
              <span className="result-label">Executed Qty</span>
              <span className="result-value">{result.executed_qty}</span>
            </div>
            <div className="result-row">
              <span className="result-label">Avg Price</span>
              <span className="result-value">{result.avg_price || 'N/A'}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
