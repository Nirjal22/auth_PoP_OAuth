export async function generateKeyPair() {
    return await window.crypto.subtle.generateKey(
        {
            name: "RSA-PSS",
            modulusLength: 2048,
            publicExponent: new Uint8Array([1, 0, 1]),
            hash: "SHA-256",
          },
          true,
          ["sign", "verify"]
        );
    }


// to save the data on the browser(indexedDB)
export async function getOrCreateKeyPair() {
  return new Promise<CryptoKeyPair>((resolve, reject) => {

    const request = indexedDB.open("device-keys-db", 1);

    request.onerror = () => {
      reject(new Error("Failed to open IndexedDB"));
    };

    request.onsuccess = async (event) => {
      const db = (event.target as IDBOpenDBRequest).result;
      console.log(db.name);

      // Check if key already exists
      const transaction = db.transaction("keys", "readonly");
      const store = transaction.objectStore("keys");
      const getRequest = store.get("privateKey");
      
      getRequest.onsuccess = async () => {
        if (getRequest.result) {
          // Key exists, import it
          const privateKey = await crypto.subtle.importKey(
            "pkcs8",
            getRequest.result,
            {
              name: "RSA-PSS",
              hash: "SHA-256",
            },
            true,
            ["sign"]
          );
          
          // Generate public key from private key
          const keyPair: CryptoKeyPair = {
            privateKey,
            publicKey: await crypto.subtle.importKey(
              "jwk",
              await crypto.subtle.exportKey("jwk", privateKey),
              {
                name: "RSA-PSS",
                hash: "SHA-256",
              },
              true,
              ["verify"]
            ),
          };
          resolve(keyPair);
        } else {
          // Key doesn't exist, generate new one
          const keyPair = await generateKeyPair();
          
          // Save the private key
          const writeTransaction = db.transaction("keys", "readwrite");
          const writeStore = writeTransaction.objectStore("keys");
          
          const exported = await crypto.subtle.exportKey(
            "pkcs8",
            keyPair.privateKey
          );
          
          const putRequest = writeStore.put(exported, "privateKey");
          
          putRequest.onsuccess = () => {
            resolve(keyPair);
          };
          
          putRequest.onerror = () => {
            reject(new Error("Failed to save private key"));
          };
          
          writeTransaction.onerror = () => {
            reject(new Error("Transaction failed: " + writeTransaction.error));
          };
        }
      };

      getRequest.onerror = () => {
        reject(new Error("Failed to retrieve private key"));
      };

      transaction.onerror = () => {
        reject(new Error("Transaction failed: " + transaction.error));
      };
    };
    
    request.onupgradeneeded = (event) => {
      const db = (event.target as IDBOpenDBRequest).result;
      if (!db.objectStoreNames.contains("keys")) {
        db.createObjectStore("keys", {keyPath: "privateKey" });
      }
    };

  });
}
