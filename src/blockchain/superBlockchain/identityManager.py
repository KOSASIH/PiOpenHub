require('dotenv').config(); // To load environment variables from a .env file
const { ethers } = require('ethers');

// Simulated decentralized storage (in-memory for this example)
const identityStorage = {};

// Event emitter for logging
const EventEmitter = require('events');
const eventEmitter = new EventEmitter();

// Event declarations
eventEmitter.on('identityCreated', (identity) => {
    console.log(`Identity created: ${JSON.stringify(identity)}`);
});

eventEmitter.on('identityVerified', (userAddress) => {
    console.log(`Identity verified for address: ${userAddress}`);
});

/**
 * Create a new identity for a user.
 * @param {string} userAddress - The Ethereum address of the user.
 * @returns {Object} - The created identity object.
 */
async function createIdentity(userAddress) {
    if (!ethers.utils.isAddress(userAddress)) {
        throw new Error('Invalid Ethereum address');
    }

    const identity = {
        address: userAddress,
        createdAt: new Date(),
        verified: false
    };

    // Store identity in decentralized storage (simulated)
    identityStorage[userAddress] = identity;

    // Emit event for identity creation
    eventEmitter.emit('identityCreated', identity);

    return identity;
}

/**
 * Verify the identity of a user.
 * @param {string} userAddress - The Ethereum address of the user.
 * @returns {Object} - The updated identity object.
 */
async function verifyIdentity(userAddress) {
    const identity = identityStorage[userAddress];

    if (!identity) {
        throw new Error('Identity not found');
    }

    identity.verified = true;

    // Emit event for identity verification
    eventEmitter.emit('identityVerified', userAddress);

    return identity;
}

// Example usage
(async () => {
    const userAddress = '0x1234567890abcdef1234567890abcdef12345678'; // Replace with a valid Ethereum address

    try {
        const identity = await createIdentity(userAddress);
        console.log('Created Identity:', identity);

        const verifiedIdentity = await verifyIdentity(userAddress);
        console.log('Verified Identity:', verifiedIdentity);
    } catch (error) {
        console.error('Error:', error.message);
    }
})();
