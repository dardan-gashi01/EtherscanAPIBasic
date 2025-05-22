import os
import sys
import requests
import csv

ETHERSCAN_API_KEY = ""

def get_eth_balance(address):
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}"
    res = requests.get(url).json()
    if res["status"] != "1":
        raise ValueError(f"Error fetching balance: {res['message']}")
    balance_wei = int(res["result"])
    balance_eth = balance_wei / 10**18
    return balance_eth

def get_tx_count(address):
    url = f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionCount&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}"
    res = requests.get(url).json()
    tx_count = int(res["result"], 16)
    return tx_count

def is_contract(address):
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
    res = requests.get(url).json()
    if res["status"] != "1":
        return "Unknown"
    for tx in res["result"]:
        if tx.get("contractAddress"):
            return "Contract"
    return "Externally Owned"

def main():
    print("Ethereum Address Information Tool")
    print("--------------------------------")
    address = input("Please enter an Ethereum address: ").strip()

    try:
        balance = get_eth_balance(address)
        tx_count = get_tx_count(address)
        addr_type = is_contract(address)

        with open("output.csv", mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Address", "Balance (ETH)", "Transaction Count", "Address Type"])
            writer.writeheader()
            writer.writerow({
                "Address": address,
                "Balance (ETH)": balance,
                "Transaction Count": tx_count,
                "Address Type": addr_type
            })

        print("\nResults:")
        print(f"Address: {address}")
        print(f"Balance: {balance} ETH")
        print(f"Transaction Count: {tx_count}")
        print(f"Address Type: {addr_type}")
        print("\nCSV written successfully as 'output.csv'.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
