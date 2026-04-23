import hashlib

# 1. Điền các giá trị HEX lấy từ log debug của bạn vào đây
r_hex = "77E6B728352D1F0C5556D84460D008B815E8426E667BBDED231CB6F0A508D321"
pk_hex = "036cee2ab45f0d2198a6578c6c89e7fdd4898d099fe45b50cb7154466a7b450f82"
msg_hex = "7478" # "tx"

# 2. Ghép nối các thành phần (phải khớp với thứ tự trong code C của bạn)
# Lưu ý: Có thể code C của bạn chỉ hash mỗi msg, hoặc hash (r + msg)
data_to_hash = bytes.fromhex(r_hex) + bytes.fromhex(pk_hex) + bytes.fromhex(msg_hex)

# 3. Tính toán SHA256
hash_result = hashlib.sha256(data_to_hash).hexdigest()

# 4. Chuyển từ Hex sang Decimal (thập phân) để khớp với chuỗi bạn đang dùng
e_decimal = int(hash_result, 16)
print(f"Giá trị e (Decimal) để hardcode: {e_decimal}")