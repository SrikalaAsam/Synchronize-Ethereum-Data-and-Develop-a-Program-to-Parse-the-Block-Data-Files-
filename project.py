from web3 import Web3
from datetime import datetime
import csv

# Infura Ethereum Mainnet URL
INFURA_URL = "https://mainnet.infura.io/v3/11e37d1b095d442c933576b39175cfcb"

# Connect to the Ethereum Mainnet
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Check connection
if web3.is_connected():
    print("Connected to Ethereum Mainnet")

    # Fetch the latest block number
    latest_block = web3.eth.block_number
    print("Latest block number:", latest_block)

    # Open CSV file for saving transactions
    with open("transactions.csv", "w", newline="") as csvfile:
        fieldnames = [
            "block_number",
            "block_timestamp_utc",
            "transaction_hash",
            "from_address",
            "to_address",
            "value",
            "gas",
            "gas_price",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Loop through the last 100 blocks
        for block_number in range(latest_block, latest_block - 100, -1):
            # Retrieve block details for each block
            block_data = web3.eth.get_block(block_number, full_transactions=True)

            # Convert timestamp to a readable format
            block_timestamp = block_data['timestamp']
            readable_timestamp = datetime.utcfromtimestamp(block_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Processing Block {block_number}, Timestamp (UTC): {readable_timestamp}")

            # List of transactions
            transactions = block_data['transactions']
            print(f"\nNumber of transactions in block {block_number}: {len(transactions)}")

            # Write transactions to the CSV file
            for txn in transactions:
                writer.writerow({
                    "block_number": block_number,
                    "block_timestamp_utc": readable_timestamp,
                    "transaction_hash": txn["hash"].hex(),
                    "from_address": txn["from"],
                    "to_address": txn.get("to", None),  # Handle contracts with no recipient
                    "value": web3.from_wei(txn["value"], "ether"),
                    "gas": txn["gas"],
                    "gas_price": web3.from_wei(txn["gasPrice"], "gwei"),
                })

    print("Transactions from the last 100 blocks saved to transactions.csv")

else:
    print("Failed to connect to Ethereum Mainnet")
