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
import sys

TIMEOUT_SECONDS = 40 # Thời gian chờ tối đa cho kết nối mạng
TIME_SHUTDOWN = 6 # Thời gian hoạt động trước khi tắt máy tính bằng giờ
isConnected = True

def is_connected():
	try:
		# Kiểm tra kết nối tới máy chủ DNS của Google
		socket.create_connection(("8.8.8.8", 53), timeout=5)
		return True
	except:
		return False

# Lay giá trị từ file response_main2.txt, trả về False nếu lỗi. Neu chuong trinh main2.pyw hoat dong binh thuong, 
# gia tri val2 va val22 se khac nhau
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

# Lay giá trị từ file response_main1.txt, trả về False nếu lỗi. Neu chuong trinh main1.pyw hoat dong binh thuong,
# gia tri val1 va val12 se khac nhau
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
		return False

if __name__ == "__main__":

	start = time.time()
	while not is_connected():
		elapsed = time.time() - start
		if elapsed >= TIMEOUT_SECONDS:
			isConnected = False
			break
		print("Không có kết nối mạng. Đang chờ...")
		sleep(5)
	if not isConnected:
		print(f"Không có kết nối mạng sau {TIMEOUT_SECONDS}s")
	else:
		print("Đã kết nối mạng.")

	thoigiantatmay = TIME_SHUTDOWN * 60 * 60

	while True:
		
		boot_time = psutil.boot_time()
		uptime_seconds = time.time() - boot_time
		if uptime_seconds > thoigiantatmay:
			if isConnected:
				send_message_text(f'hoạt động quá {TIME_SHUTDOWN}h, shutdown thành công')
			sleep(180)
			os.system("shutdown /s")
			sleep(180)

		while not get_val2():
			sleep(3)

		while not get_val1():
			sleep(3)

		sleep(180) # Kiểm tra mỗi 3 phút

		while not get_val2_lan2():
			sleep(3)

		while not get_val1_lan2():
			sleep(3)

		if int(val2) == int(val22):
			restart_number()
			if isConnected:
				send_message_text('not response main2, restart thành công')
			sleep(180)
			os.system("shutdown /r")
			sleep(180)

		if int(val1) == int(val12):
			restart_number()
			if isConnected:
				send_message_text('not response main1, restart thành công')
			sleep(180)
			os.system("shutdown /r")
			sleep(180)