import os
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket
import imaplib

def is_connected():
	try:
		# Kiểm tra kết nối tới máy chủ DNS của Google
		socket.create_connection(("8.8.8.8", 53), timeout=5)
		return True
	except:
		return False

def send_message_text(message_text):
	try:
		smtp_server = "smtp.gmail.com"
		port = 587
		sender_email = "qbquangbinh@gmail.com"
		receiver_email = 'qbquangbinh@gmail.com'
		password = os.getenv("PASS_EMAIL")
		subject = message_text
		body = message_text
		message = MIMEMultipart()
		message["From"] = sender_email
		message["To"] = receiver_email
		message["Subject"] = subject
		message.attach(MIMEText(body, "plain"))
		text = message.as_string()
		context = ssl.create_default_context()
		server = smtplib.SMTP(smtp_server, port)
		server.starttls(context=context)
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, text)
		server.quit()
		return True
	except Exception as e:
		print(f"Đã xảy ra lỗi khi gửi email: {e}")
		return False

def check_message_text():
	# Cấu hình thông tin đăng nhập Gmail
	USERNAME = 'qbquangbinh@gmail.com'
	PASSWORD = os.getenv("PASS_EMAIL") # Nếu dùng xác thực 2 bước, hãy sử dụng App Password

	IMAP_SERVER = 'imap.gmail.com'
	IMAP_PORT = 993
	if os.path.exists("dkmt.txt"):
		os.remove("dkmt.txt")
	try:
		# Kết nối tới server IMAP của Gmail
		mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
		mail.login(USERNAME, PASSWORD)
		mail.select("inbox")

		# Tìm kiếm email chưa đọc từ người gửi qbquangbinh@gmail.com với Subject chứa "dkmt"
		while True:
			search_criteria = '(UNSEEN FROM "qbquangbinh@gmail.com" SUBJECT "dkmt")'
			status, messages = mail.search(None, search_criteria)
			if status == 'OK':
				break
		email_ids = messages[0].split()
		if not email_ids:
			print("Không có email mới.")
			mail.logout()
			return False

		for email_id in email_ids:
			status, data = mail.fetch(email_id, '(RFC822)')
			if status != 'OK':
				print("Lỗi khi lấy email id:", email_id)
				continue
			# Lấy nội dung email
			raw_email = data[0][1]
			msg = email.message_from_bytes(raw_email)

			# Lưu nội dung email vào file dkmt.txt
			with open("dkmt.txt", "w", encoding="utf-8") as dkmt_file:
				if msg.is_multipart():
					for part in msg.walk():
						if part.get_content_type() == "text/plain":
							dkmt_file.write(part.get_payload(decode=True).decode("utf-8"))
				else:
					dkmt_file.write(msg.get_payload(decode=True).decode("utf-8"))
					   
			# Đánh dấu email đã đọc
			mail.store(email_id, '+FLAGS', '\\Seen')

		mail.logout()
		return True
	except Exception as e:
		print(f"Đã xảy ra lỗi khi kiểm tra email: {e}")
		return False
	
def send_text_photo(text, photo_path):
	try:
		smtp_server = "smtp.gmail.com"
		port = 587
		sender_email = "qbquangbinh@gmail.com"
		receiver_email = 'qbquangbinh@gmail.com'
		password = os.getenv("PASS_EMAIL")
		subject = text
		body = text
		message = MIMEMultipart()
		message["From"] = sender_email
		message["To"] = receiver_email
		message["Subject"] = subject
		message.attach(MIMEText(body, "plain"))
		with open(photo_path, "rb") as attachment:
			part = MIMEBase("application", "octet-stream")
			part.set_payload(attachment.read())
		encoders.encode_base64(part)
		part.add_header(
			"Content-Disposition",
			f"attachment; filename={photo_path}",
		)
		message.attach(part)
		text = message.as_string()
		context = ssl.create_default_context()
		server = smtplib.SMTP(smtp_server, port)
		server.starttls(context=context)
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, text)
		server.quit()
		return True
	except Exception as e:
		print(f"Đã xảy ra lỗi khi gửi email: {e}")
		return False
	
def restart_number(file_path = "restart_number.txt"):
	if not os.path.exists(file_path):
		with open(file_path, "w") as file:
			file.write("1")
			file.close()
		restart_count = 1
	else:
		with open(file_path, "r") as file:
			restart_count = int(file.read().strip())
		restart_count += 1
		with open(file_path, "w") as file:
			file.write(str(restart_count))
			file.close()
	print(f"Đã ghi số lần khởi động lại: {restart_count} lần.")
	return