from cryptos import *
import bech32

def fixed_from_string_to_bytes(a):
    if isinstance(a, bytes):
        return a
    if isinstance(a, str):
        try:
            # Thử chuyển từ Hex string sang bytes trước
            return bytes.fromhex(a)
        except ValueError:
            # Nếu không phải Hex, mới dùng utf-8
            return a.encode('utf-8')
    return bytes(a)
import cryptos.py3specials
cryptos.py3specials.from_string_to_bytes = fixed_from_string_to_bytes
def bech32_script_pubkey(bech32_addr):
    """Tính scriptPubKey từ địa chỉ Bech32 (tb1q...) cho P2WPKH"""
    hrp, data = bech32.bech32_decode(bech32_addr)
    if hrp is None:
        raise ValueError("Địa chỉ Bech32 không hợp lệ")
    
    # witver là data[0], witprog chuyển từ 5-bit sang 8-bit
    witver = data[0]
    witprog = bech32.convertbits(data[1:], 5, 8, False)
    
    # ScriptPubKey SegWit P2WPKH: OP_0 (0x00) + PUSH_20 (0x14) + 20 bytes pubkey hash
    return bytes([witver, len(witprog)]) + bytes(witprog)


def main():
    c = Bitcoin(testnet=True)

    # 1. HARDCODE INPUTS TỪ BƯỚC 2.2 (QUAN TRỌNG NHẤT)
    # Thay TxID dưới đây bằng kết quả nhận được từ file test_pay_new_address_1.py
    my_txid = "daa91cd88eba465c4162c0c097f8c2dbd9bd7c72281919b948ed19aee0575330" 
    my_address = "tb1qlqxtrvc7peq4avaq2aedzk68ldc4jkerh38425" # Địa chỉ Alice
    
    inputs = [{
        'tx_hash': my_txid,
        'tx_pos': 0,           # Thường là 0
        'value': 10000,      # Số satoshi đã khóa
        'address': my_address
    }]
    print("\nInputs (Hardcoded):", inputs)

    # 2. THIẾT LẬP ĐẦU RA (HUB)
    outs = [{'value': 9700, 'address': 'tb1qy2ldd07rzkwaqzg7t057zvtg6xmqssz59mp40s'}]
    
    tx = c.mktx(inputs, outs)
    
    
    tx_split = tx

    # 3. TÍNH TOÁN SCRIPT CHO SEGWIT
    script = bech32_script_pubkey(my_address)
    print("\nScriptPubKey Hex:", script.hex())

    # Tạo form ký để lấy Hash (e)
    print("\ntx_split - SIGHASH_ALL", tx_split, SIGHASH_ALL)
    tx4 = signature_form(tx_split, 0, script.hex(), SIGHASH_ALL)
    print("\nSigning transaction:\n", tx4)
    if isinstance(tx4, bytes):
    	tx4 = tx4.hex()
    bin_txh = bin_txhash(tx4, SIGHASH_ALL)
    e = hash_to_int(bin_txh)
    
    print("\n--- DỮ LIỆU CHO CODE C ---")
    print(f"e (int): {e}")
    print(f"e (hex) -> Dán vào alice.c & tumbler.c: {hex(e)[2:].zfill(64)}")

    # 4. SỬA PRIVATE KEYS 
    priv_s = "cPHSGLYv5hJ53V3Weo8T1Wfu7aHbTa8vu19qZfdN9VXsY7Fxdh5M" 
    priv_h1 = "cUZ3EsCnFAsR4xBfRMM8TnK6TPXSXumxHPUBKoZZrNFAV8QiVND2"

    try:
        k_s = deterministic_generate_k(tx4, priv_s)
        print(f"k_s (hex) -> Dán vào alice.c: {k_s}")

        k_h1 = deterministic_generate_k(tx4, priv_h1)
        print(f"k_h1 (hex) -> Dán vào tumbler.c: {k_h1}")
    except Exception as err:
        print("\nLỗi tính k: Kiểm tra lại Private Key định dạng Hex chưa?")

    
    #print("\n[!] Lưu ý: Chữ ký 'rawsig' phía dưới cần được cập nhật từ kết quả của alice.c")

if __name__ == "__main__":
    main()
