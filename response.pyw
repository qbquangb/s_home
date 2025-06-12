import os
import psutil
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket
import time
from time import sleep
from func import restart_number

def is_connected():
	try:
		# Kiểm tra kết nối tới máy chủ DNS của Google
		socket.create_connection(("8.8.8.8", 53), timeout=5)
		return True
	except:
		return False
	
def get_val2():
	global val2
	try:
		with open("response_main2.txt", "r") as file:
			val2 = file.read()
			file.close()
			print(f"val2: {val2}")
		return val2
	except:
		return False
	
def get_val2_lan2():
	global val22
	try:
		with open("response_main2.txt", "r") as file:
			val22 = file.read()
			file.close()
			print(f"val22: {val22}")
		return val22
	except:
		return False

def get_val1():
	global val1
	try:
		with open("response_main1.txt", "r") as file:
			val1 = file.read()
			file.close()
			print(f"val1: {val1}")
		return val1
	except:
		return False
	
def get_val1_lan2():
	global val12
	try:
		with open("response_main1.txt", "r") as file:
			val12 = file.read()
			file.close()
			print(f"val12: {val12}")
		return val12
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
	
def main():

	while not is_connected():
		print("Không có kết nối mạng. Đang chờ...")
		sleep(5)
	print("Đã kết nối mạng.")

	thoigiantatmay = 6 * 60 * 60
	boot_time = psutil.boot_time()
	uptime_seconds = time.time() - boot_time
	if uptime_seconds > thoigiantatmay:
		os.system("shutdown /s")
		send_message_text('hoạt động 6h, shutdown thành công')
		sleep(180)

	while not get_val2():
		sleep(3)

	while not get_val1():
		sleep(3)

	sleep(600)

	while not get_val2_lan2():
		sleep(3)

	while not get_val1_lan2():
		sleep(3)

	if int(val2) == int(val22):
		send_message_text('not response main2, restart thành công')
		sleep(180)
		os.system("shutdown /r")

	if int(val1) == int(val12):
		send_message_text('not response main1, restart thành công')
		sleep(180)
		os.system("shutdown /r")

if __name__ == "__main__":
	# try:
	# 	main()
	# except Exception as e:
	# 	restart_number()
	# 	print(f"Đã xảy ra lỗi trong quá trình thực thi: {e}")
	# 	send_message_text('lỗi response.pyw, restart thành công')
	# finally:
	# 	send_message_text('lỗi response.pyw, máy tính sẻ tự reset sau 3 phút.')
	# 	sleep(180)
	# 	os.system("shutdown /r")
	thoigiantatmay = 2 * 60 * 60
	boot_time = psutil.boot_time()
	uptime_seconds = time.time() - boot_time
	if uptime_seconds > thoigiantatmay:
		os.system("shutdown /s")
		send_message_text('hoạt động 2h, shutdown thành công')
		sleep(180)