import logging
from chainlink import Oracle

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PiCommodityOracle:
    def __init__(self):
        self.commodities = {
            "gold": 0.4,  # Default weight for gold
            "oil": 0.6    # Default weight for oil
        }

    def set_commodity_weights(self, weights):
        """Set custom weights for commodities."""
        if sum(weights.values()) != 1:
            logging.error("Weights must sum to 1.")
            raise ValueError("Weights must sum to 1.")
        self.commodities = weights

    def get_commodity_value(self):
        """Fetch the commodity values and calculate the weighted average."""
        try:
            total_value = 0
            for commodity, weight in self.commodities.items():
                price = Oracle.get_price(commodity)
                total_value += price * weight
                logging.info(f"Fetched price for {commodity}: {price}, Weight: {weight}")

            logging.info(f"Calculated commodity value: {total_value}")
            return total_value
        except Exception as e:
            logging.error(f"Error fetching commodity values: {e}")
            return None

# Example usage
if __name__ == "__main__":
    oracle = PiCommodityOracle()

    # Fetch the default commodity value
    commodity_value = oracle.get_commodity_value()
    print(f"Default Commodity Value: {commodity_value}")

    # Set custom weights and fetch the commodity value again
    custom_weights = {
        "gold": 0.5,
        "oil": 0.5
    }
    oracle.set_commodity_weights(custom_weights)
    commodity_value = oracle.get_commodity_value()
    print(f"Custom Weighted Commodity Value: {commodity_value}")
