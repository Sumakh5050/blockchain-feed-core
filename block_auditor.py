"""
Block Auditor — аудит содержимого блока в Bitcoin: скрипты, OP_RETURN, комиссии.
"""

import requests
import argparse

def fetch_block(block_height):
    url = f"https://api.blockchair.com/bitcoin/blocks?q=id({block_height})"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("❌ Ошибка получения блока.")
    data = r.json()["data"][0]
    return data["id"], data["hash"]

def fetch_block_transactions(block_hash):
    url = f"https://api.blockchair.com/bitcoin/raw/block/{block_hash}"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("❌ Ошибка получения транзакций блока.")
    txs = r.json()["data"][block_hash]["decoded_raw_block"]["tx"]
    return txs

def analyze_block(block_height):
    print(f"🔍 Block Auditor: анализ блока #{block_height}")
    _, block_hash = fetch_block(block_height)
    txs = fetch_block_transactions(block_hash)
    print(f"💼 Транзакций в блоке: {len(txs)}")

    op_return_count = 0
    high_fee_txs = []

    for tx in txs:
        inputs = tx.get("vin", [])
        outputs = tx.get("vout", [])
        total_in = sum(i.get("value", 0) for i in inputs if "coinbase" not in i)
        total_out = sum(o.get("value", 0) for o in outputs)
        fee = total_in - total_out if total_in > 0 else 0

        for out in outputs:
            script = out.get("script_pub_key", {})
            asm = script.get("asm", "")
            if "OP_RETURN" in asm:
                op_return_count += 1

        if fee > 0.01:
            high_fee_txs.append((tx["txid"], round(fee, 8)))

    print(f"📜 OP_RETURN транзакций: {op_return_count}")
    print(f"💸 Транзакции с высокой комиссией (>0.01 BTC):")
    for txid, fee in high_fee_txs:
        print(f"  - {txid}: {fee} BTC")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Block Auditor — аудит содержимого блока.")
    parser.add_argument("height", type=int, help="Высота блока")
    args = parser.parse_args()
    analyze_block(args.height)
