require('dotenv').config(); // To load environment variables from a .env file
const Web3 = require('web3');

/**
 * Connect to the blockchain using the provided URL.
 * @param {string} url - The URL of the blockchain node.
 * @returns {Web3} - An instance of the Web3 object.
 */
async function connectToBlockchain(url) {
    try {
        const web3 = new Web3(new Web3.providers.HttpProvider(url));
        console.log("Connected to blockchain at:", url);
        return web3;
    } catch (error) {
        console.error("Error connecting to blockchain:", error);
        throw error;
    }
}

/**
 * Transfer tokens from one account to another.
 * @param {Web3} web3 - The Web3 instance.
 * @param {string} from - The sender's address.
 * @param {string} to - The recipient's address.
 * @param {number} amount - The amount of tokens to transfer (in Ether).
 * @param {string} privateKey - The private key of the sender.
 * @returns {Object} - The transaction receipt.
 */
async function transferTokens(web3, from, to, amount, privateKey) {
    try {
        const nonce = await web3.eth.getTransactionCount(from, 'latest'); // Get the latest nonce

        const transaction = {
            from: from,
            to: to,
            value: web3.utils.toWei(amount.toString(), 'ether'),
            gas: 2000000,
            nonce: nonce,
        };

        // Sign the transaction
        const signedTransaction = await web3.eth.accounts.signTransaction(transaction, privateKey);

        // Send the transaction
        const receipt = await web3.eth.sendSignedTransaction(signedTransaction.rawTransaction);
        console.log("Transaction successful with hash:", receipt.transactionHash);
        return receipt;
    } catch (error) {
        console.error("Error transferring tokens:", error);
        throw error;
    }
}

// Example usage
(async () => {
    const url = process.env.BLOCKCHAIN_URL; // Set your blockchain node URL in .env file
    const web3 = await connectToBlockchain(url);

    const fromAddress = process.env.FROM_ADDRESS; // Sender's address
    const toAddress = process.env.TO_ADDRESS; // Recipient's address
    const amount = 0.1; // Amount to transfer in Ether
    const privateKey = process.env.PRIVATE_KEY; // Sender's private key

    try {
        const receipt = await transferTokens(web3, fromAddress, toAddress, amount, privateKey);
        console.log("Transaction receipt:", receipt);
    } catch (error) {
        console.error("Transaction failed:", error);
    }
})();
