import socket
import time
from datetime import date, datetime
from time import sleep
import os
import webbrowser
from pynput.mouse import Button, Controller
from func import restart_number
import datetime
import sys

sleep(20)

TIMEOUT_SECONDS = 40 # Thời gian chờ tối đa cho kết nối mạng
isConnected = True

def is_connected():
	try:
		# Kiểm tra kết nối tới máy chủ DNS của Google
		socket.create_connection(("8.8.8.8", 53), timeout=5)
		return True
	except:
		return False
	
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

if isConnected:
	from func import send_message_text, check_message_text, send_text_photo

try:

	RESET_MAX = 12
	print("Khoi dong thanh cong.")
	with open("restart_number.txt", "r") as file:
		restart_count = int(file.read().strip())
		file.close()
	if restart_count > RESET_MAX:
		with open("restart_number.txt", "w") as file:
			file.write("0")
			file.close()
		if isConnected:
			send_message_text(f'Máy tính đã khởi động lại {RESET_MAX} lần liên tiếp, hệ thống sẽ tắt máy để tránh lỗi lặp lại.')
		sleep(180)
		os.system("shutdown /s")
		sleep(180)

	del file
	del restart_count

	ktdkmaytinhlancuoi = None
	ktdkmaytinhsau = 5

	kt_yc_alertimagelancuoi = None
	kt_yc_alertimagesau = 1

	kt_yc_guianhlancuoi = None
	kt_yc_guianhsau = 600

	kt_thongbaolancuoi = None
	kt_thongbaosau = 2

	kt_response_lancuoi = None
	kt_response_sau = 60
	val2 = 0
	cap = None
	cap4 = None

	if isConnected:
		send_message_text('Khởi động thành công')

	while True:

		if kt_response_lancuoi is None or ((datetime.datetime.utcnow() - kt_response_lancuoi).total_seconds() > kt_response_sau):
			kt_response_lancuoi = datetime.datetime.utcnow()
			with open("response_main1.txt", "w") as file:
				file.write(str(val2))
				file.close()
			val2 += 1
			if val2 == 10000:
				val2 = 0

		# Phan code dieu khien den may tinh.
		if (ktdkmaytinhlancuoi is None) or ((datetime.datetime.utcnow() - ktdkmaytinhlancuoi).total_seconds() > ktdkmaytinhsau):
			ktdkmaytinhlancuoi = datetime.datetime.utcnow()

			check_message_text("dkmt")
			lines = []
			if os.path.exists("dkmt.txt"):
				with open("dkmt.txt", "r", encoding="utf-8") as dkmt_file:
					lines = dkmt_file.readlines()
					dkmt_file.close()
			if lines:
				res = lines[0].strip()

				if res == 'restart':
					if isConnected:
						send_message_text('restart thành công')
					sleep(180)
					os.system("shutdown /r")
					sleep(180)

				elif (res == 'shutdown'):
					if isConnected:
						send_message_text('shutdown thành công')
					sleep(180)
					os.system("shutdown /s")
					sleep(180)

		# Phan code video.

		if (kt_yc_alertimagelancuoi is None) or ((datetime.datetime.utcnow() - kt_yc_alertimagelancuoi).total_seconds() > kt_yc_alertimagesau):
			kt_yc_alertimagelancuoi = datetime.datetime.utcnow()
			if os.path.exists('alert_image'):
				directory = 'alert_image/'
				files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
				latest_file = max(files, key=os.path.getctime)
				cap2 = os.path.basename(latest_file)
				if cap != cap2:
					if isConnected:
						send_text_photo(text = cap2, photo_path = latest_file)
					cap = cap2

		if (kt_yc_guianhlancuoi is None) or ((datetime.datetime.utcnow() - kt_yc_guianhlancuoi).total_seconds() > kt_yc_guianhsau):
			kt_yc_guianhlancuoi = datetime.datetime.utcnow()
					
			if os.path.exists('update_image'):
				directory = 'update_image/'
				files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
				latest_file = max(files, key=os.path.getctime)
				cap3 = os.path.basename(latest_file)

				if isConnected:
					send_text_photo(text = cap3, photo_path = latest_file)

			else:
				pass

		if (kt_thongbaolancuoi is None) or ((datetime.datetime.utcnow() - kt_thongbaolancuoi).total_seconds() > kt_thongbaosau):
			kt_thongbaolancuoi = datetime.datetime.utcnow()
			if os.path.exists('alert_notification'):
				directory = 'alert_notification/'
				files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
				latest_file = max(files, key=os.path.getctime)
				cap5 = os.path.basename(latest_file)
				if cap4 != cap5:
					if isConnected:
						send_message_text(cap5)
					cap4 = cap5

except Exception as e:
	restart_number()
	print(f'err {e}', file=sys.stderr, flush=True)
	if isConnected:
		send_message_text(f'Lỗi: {e}, máy tính sẻ tự reset.')

except BaseException as e:
	restart_number()
	print(f'err {e}', file=sys.stderr, flush=True)
	if isConnected:
		send_message_text(f'Chương trình bị lỗi, {e}, máy tính sẻ tự reset')

finally:
	if isConnected:
		send_message_text('Lỗi main1.pyw. Máy tính sẻ tự reset sau 3 phút.')
	sleep(180)
	os.system("shutdown /r")
	sleep(180)