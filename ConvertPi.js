import { useState } from "react";
import axios from "axios";

const ConvertPi = () => {
  const [currency, setCurrency] = useState("usd");
  const [amount, setAmount] = useState(1);
  const [converted, setConverted] = useState(null);

  const convertPi = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/convert/${currency}`);
      setConverted(response.data["pi-network"][currency] * amount);
    } catch (error) {
      console.error("Error fetching exchange rate:", error);
    }
  };

  return (
    <div>
      <h2>Konversi Pi Coin</h2>
      <input type="number" value={amount} onChange={(e) => setAmount(e.target.value)} />
      <select value={currency} onChange={(e) => setCurrency(e.target.value)}>
        <option value="usd">USD</option>
        <option value="eur">EUR</option>
        <option value="btc">BTC</option>
        <option value="eth">ETH</option>
      </select>
      <button onClick={convertPi}>Konversi</button>
      {converted !== null && <p>Hasil: {converted} {currency.toUpperCase()}</p>}
    </div>
  );
};

export default ConvertPi;
