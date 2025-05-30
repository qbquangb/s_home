import imaplib
import email
import os
from time import sleep
import socket

# Cấu hình thông tin đăng nhập Gmail
USERNAME = 'qbquangbinh@gmail.com'
PASSWORD = os.getenv("PASS_EMAIL") # Nếu dùng xác thực 2 bước, hãy sử dụng App Password

IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993

def check_and_download():
    try:
        # Kết nối tới server IMAP của Gmail
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(USERNAME, PASSWORD)
        mail.select("inbox")

        # Tìm kiếm email chưa đọc từ người gửi qbquangbinh@gmail.com với Subject chứa "capnhatchuongtrinh"
        while True:
            search_criteria = '(UNSEEN FROM "qbquangbinh@gmail.com" SUBJECT "capnhatchuongtrinh")'
            status, messages = mail.search(None, search_criteria)
            if status == 'OK':
                break
        email_ids = messages[0].split()
        if not email_ids:
            print("Không có email mới.")
            mail.logout()
            return

        for email_id in email_ids:
            status, data = mail.fetch(email_id, '(RFC822)')
            if status != 'OK':
                print("Lỗi khi lấy email id:", email_id)
                continue

            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Duyệt qua các phần của email để tìm file đính kèm
            for part in msg.walk():
                content_disposition = part.get("Content-Disposition")
                if content_disposition and "attachment" in content_disposition:
                    filename = part.get_filename()
                    # Chỉ xử lý file có đuôi .pyw hoặc .py
                    if filename and (filename.endswith('.pyw') or filename.endswith('.py')):
                        # Đường dẫn lưu file.
                        save_path = os.path.join("D:\\Duan\\2s_home", filename)
                        if filename == 'response.pyw' or filename == 'main1.pyw' or filename == 'main2.pyw' or filename == 'prog_add.pyw':
                            if os.path.exists(save_path):
                                os.remove(save_path)
                            with open(save_path, "wb") as f:
                                f.write(part.get_payload(decode=True))
                       
            # Đánh dấu email đã đọc
            mail.store(email_id, '+FLAGS', '\\Seen')

        mail.logout()
    except Exception as e:
        print(f"Đã xảy ra lỗi khi kiểm tra email: {e}")

def is_connected():
    try:
        # Kiểm tra kết nối tới máy chủ DNS của Google
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except:
        return False

if __name__ == "__main__":
    while not is_connected():
        print("Không có kết nối mạng. Đang chờ...")
        sleep(5)
    print("Đã kết nối mạng.")
    check_and_download()