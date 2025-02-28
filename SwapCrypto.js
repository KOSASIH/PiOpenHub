import { useState } from "react";
import axios from "axios";

const SwapCrypto = () => {
  const [from, setFrom] = useState("pi-network");
  const [to, setTo] = useState("btc");
  const [amount, setAmount] = useState(1);
  const [swapResult, setSwapResult] = useState(null);

  const swapCrypto = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/swap/${from}/${to}`);
      setSwapResult(amount * response.data.rate);
    } catch (error) {
      console.error("Error fetching swap rate:", error);
    }
  };

  return (
    <div>
      <h2>Swap Kripto</h2>
      <input type="number" value={amount} onChange={(e) => setAmount(e.target.value)} />
      <select value={from} onChange={(e) => setFrom(e.target.value)}>
        <option value="pi-network">Pi Coin</option>
        <option value="bitcoin">Bitcoin</option>
        <option value="ethereum">Ethereum</option>
      </select>
      <span>➡</span>
      <select value={to} onChange={(e) => setTo(e.target.value)}>
        <option value="pi-network">Pi Coin</option>
        <option value="bitcoin">Bitcoin</option>
        <option value="ethereum">Ethereum</option>
      </select>
      <button onClick={swapCrypto}>Tukar</button>
      {swapResult !== null && <p>Hasil: {swapResult} {to.toUpperCase()}</p>}
    </div>
  );
};

export default SwapCrypto; yg
