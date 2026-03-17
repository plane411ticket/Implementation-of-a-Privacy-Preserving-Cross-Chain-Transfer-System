from cryptos import *

def main():
    c = Litecoin(testnet=True)
    
    # 1. THÔNG TIN VÍ CHỨA TIỀN DƯ (Địa chỉ tltc1qfaycr...)
    addr_phu = 'tltc1qfaycr8edr6ldmyfegj43qetydtq8x8hxnyhy8p'
    priv_phu = 'cPAWuoaUxSBDZdsfHX8xTid8oh8vGeAFhk6CgiLH2MnWLL4qwH7t' # Key bắt đầu bằng chữ 'c'
    
    # 2. ĐỊA CHỈ VÍ GỐC (Nơi bạn muốn nhận lại tiền)
    addr_goc = 'tltc1qw3h3l7qm5w67f09t3239gnvl9l4x8a4z2hvk5z'
    
    # 3. Tìm các cục tiền đang kẹt
    inputs = c.unspent(addr_phu)
    
    if not inputs:
        print("Không tìm thấy tiền dư ở địa chỉ này!")
        return
        
    total_input = sum(i['value'] for i in inputs)
    print(f"Tổng tiền phát hiện: {total_input} satoshis")

    # 4. Thiết lập phí và tính số tiền thực nhận
    fee = 2000 # Phí giao dịch (khoảng 0.00002 LTC)
    send_amount = total_input - fee
    
    if send_amount <= 0:
        print("Số dư quá nhỏ không đủ trả phí!")
        return

    # Chỉ có 1 output duy nhất về ví gốc
    outputs = [{'value': send_amount, 'address': addr_goc}]
    
    # 5. Tạo và ký
    tx = c.mktx(inputs, outputs)
    tx2 = c.signall(tx, priv_phu)
    tx3 = serialize(tx2)
    
    print("\nRaw Hex để gom tiền về ví gốc:\n", tx3)
    
    # 6. Phát tán
    try:
        txid = c.pushtx(tx3)
        print(f"\nThành công! Tiền đang trên đường về ví gốc. Txid: {txid}")
    except:
        print("\nLỗi pushtx (do node chưa sync). Hãy copy Hex dán vào LitecoinSpace nhé!")

if __name__ == "__main__":
    main()
