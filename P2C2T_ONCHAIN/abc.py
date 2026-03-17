from cryptos import *
from cryptos import serialize

def main():
    c = Bitcoin(testnet=True)

    # Private key dạng hex raw (64 ký tự) – THAY BẰNG KEY THẬT CỦA BẠN
    priv_hex = "AC60019C77CF2FB7FC752B281563CD6D0E4BB6D910EF5C4F3B7FEB23255A5C83"  # ví dụ từ alice.key (lấy bằng xxd)

    inputs = c.unspent('mgnRdzyRYH9eyaYbV89u5QP4f8WgQgWM6S')
    print("Inputs (UTXOs):", inputs)

    if not inputs:
        print("ERROR: No unspent outputs found for address mgnRdzyRYH9eyaYbV89u5QP4f8WgQgWM6S")
        return

    outputs = [
        {'value': 15000, 'address': 'n2XSUne7GUnj6Fy4wNQMJiNLaLE4pGRQs4'},  # shared address
        {'value': 0, 'address': '2MzKf17jzLf9HntXWE5LJw5neWAJysTi8xU'}      # change
    ]

    tx = c.mktx(inputs, outputs)
    print("\nUnsigned transaction:", tx)

    # Sign bằng hex raw (không cần WIF)
    tx2 = c.signall(tx, priv_hex)
    print("\nSigned transaction:", tx2)

    tx3 = serialize(tx2)
    print("\nRaw signed transaction (hex):\n", tx3)

    txid = c.pushtx(tx3)
    print("\nTxID:", txid)

if __name__ == "__main__":
    main()
