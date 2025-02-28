require("dotenv").config();
const express = require("express");
const axios = require("axios");
const cors = require("cors");

const app = express();
app.use(express.json());
app.use(cors());

const COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price";

// Mendapatkan nilai tukar Pi Coin ke mata uang lain
app.get("/convert/:currency", async (req, res) => {
  try {
    const currency = req.params.currency.toLowerCase();
    const response = await axios.get(`${COINGECKO_API}?ids=pi-network&vs_currencies=${currency}`);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: "Gagal mendapatkan nilai tukar" });
  }
});

// Swap antara dua mata uang kripto
app.get("/swap/:from/:to", async (req, res) => {
  try {
    const { from, to } = req.params;
    const response = await axios.get(`${COINGECKO_API}?ids=${from},${to}&vs_currencies=usd`);
    
    const fromPrice = response.data[from].usd;
    const toPrice = response.data[to].usd;
    
    const swapRate = fromPrice / toPrice;
    res.json({ rate: swapRate });
  } catch (error) {
    res.status(500).json({ error: "Gagal mendapatkan nilai tukar" });
  }
});

app.listen(5000, () => console.log("Server berjalan di port 5000"));
