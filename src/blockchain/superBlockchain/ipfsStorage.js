const IPFS = require('ipfs-core');

async function storeData(data) {
    const ipfs = await IPFS.create();
    const { cid } = await ipfs.add(data);
    return cid.toString();
}

async function retrieveData(cid) {
    const ipfs = await IPFS.create();
    const data = await ipfs.cat(cid);
    return data.toString();
}

// Example usage
(async () => {
    const dataToStore = 'Hello, IPFS!';
    const cid = await storeData(dataToStore);
    console.log(`Stored data with CID: ${cid}`);

    const retrievedData = await retrieveData(cid);
    console.log(`Retrieved data: ${retrievedData}`);
})();
