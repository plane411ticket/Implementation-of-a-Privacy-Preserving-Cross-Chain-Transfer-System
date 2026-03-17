from cryptos import *
import hashlib

def hex_to_wif_testnet(priv_hex, compressed=True):
    """Chuyển private key hex sang WIF testnet (compressed)"""
    vbyte = 0xef  # version byte cho testnet
    priv_bytes = bytes.fromhex(priv_hex)
    if compressed:
        priv_bytes += b'\x01'
    extended = bytes([vbyte]) + priv_bytes
    checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
    final = extended + checksum
    wif = base58.b58encode(final).decode('utf-8')
    return wif

def main():
    c = Litecoin(testnet=True)    
    #priv = "AB5BAE62A36AD0DAB0F1B8C1A352F46057C9E4A56BE1C28BC1837FAE97717FA1034060CDBF7112753F6FFA7FA3BC01E6672762B0010CAD41BE489F3DC6AE44B04E"
    #priv = hex_to_wif(priv_hex, compressed=True)
    priv = "cUZ3EsCnFAsR4xBfRMM8TnK6TPXSXumxHPUBKoZZrNFAV8QiVND2"
    #priv = hex_to_wif_testnet(priv_hex, compressed=True)
    inputs = c.unspent('tltc1qw3h3l7qm5w67f09t3239gnvl9l4x8a4z2hvk5z')
    print("Inputs", inputs)
    total_input = sum(i['value'] for i in inputs)
    print("Total Inputs:", total_input)
    send_amount = 10000
    fee = 15*200
    change_amount = total_input - send_amount - fee

    outputs = [{'value': send_amount, 'address': 'mv7r5LwdkZgBDR2UmuCfGhz734dTDUPyQz'}, {'value': change_amount, 'address': 'tltc1qfaycr8edr6ldmyfegj43qetydtq8x8hxnyhy8p'}]
   
    tx = c.mktx(inputs, outputs)
    print("\nUnsigned ransaction:\n", tx)
 
    tx2 = c.signall(tx, priv)
    print("\nSigned ransaction:\n", tx2)
    
    tx3 = serialize(tx2)
    
    # print raw signed transaction ready to be broadcasted
    print("\nRaw signed transaction:\n" + tx3)
    txid = c.pushtx(tx3)
    #print("\nTxid:" + txid)
    #print("\nBroadcast thủ công (không dùng pushtx để tránh lỗi):")
    #print("1. Copy raw tx hex dưới đây")
    #print("2. Vào https://litecoinspace.org/testnet/tx/push")
    #print("3. Paste và nhấn Broadcast transaction")
    #print("4. Kiểm tra TxID trên explorer sau khi confirm")


if __name__ == "__main__":
    main()
