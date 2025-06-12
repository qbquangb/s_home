try:
	from datetime import date, datetime
	from time import sleep
	import os
	import webbrowser
	from pynput.mouse import Button, Controller
	from func import send_message_text, check_message_text, send_text_photo, restart_number
	import datetime
	import serial

	with open("restart_number.txt", "r") as file:
		restart_count = int(file.read().strip())
		file.close()
	if restart_count == 8:
		with open("restart_number.txt", "w") as file:
			file.write("0")
			file.close()
		print('Máy tính đã restart 8 lần, máy tính sẻ tự tắt.')
		send_message_text('Máy tính đã restart 8 lần, máy tính sẻ tự tắt.')
		sleep(180)
		os.system("shutdown /s")

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

	print('Khởi động thành công')
	send_message_text('Khởi động thành công')
	ser = serial.Serial(port='COM4', baudrate=9600, timeout=0.2)
	ktbatdenlancuoi = None
	ktbatdensau = 10

	while True:

		if kt_response_lancuoi is None or ((datetime.datetime.utcnow() - kt_response_lancuoi).total_seconds() > kt_response_sau):
			kt_response_lancuoi = datetime.datetime.utcnow()
			with open("response_main1.txt", "w") as file:
				file.write(str(val2))
				file.close()
			val2 += 1
			if val2 == 10000:
				val2 = 0

		# Phan code dieu khien den.
		if (ktbatdenlancuoi is None) or ((datetime.datetime.utcnow() - ktbatdenlancuoi).total_seconds() > ktbatdensau):
			ktbatdenlancuoi = datetime.datetime.utcnow()

			check_message_text()
			lines = []
			if os.path.exists("dkmt.txt"):
				with open("dkmt.txt", "r", encoding="utf-8") as dkmt_file:
					lines = dkmt_file.readlines()
					dkmt_file.close()
			if lines:
				res = lines[0].strip()

				if res == 'batden':
					ser.write(b'batloa\r')
					sleep(3)
					send_message_text('Đèn đã được bật.')
				elif res == 'tatden':
					ser.write(b'tatloa\r')
					sleep(3)
					send_message_text('Đèn đã được tắt.')
				else:
					pass

		# Phan code dieu khien den may tinh.
		if (ktdkmaytinhlancuoi is None) or ((datetime.datetime.utcnow() - ktdkmaytinhlancuoi).total_seconds() > ktdkmaytinhsau):
			ktdkmaytinhlancuoi = datetime.datetime.utcnow()

			check_message_text()
			lines = []
			if os.path.exists("dkmt.txt"):
				with open("dkmt.txt", "r", encoding="utf-8") as dkmt_file:
					lines = dkmt_file.readlines()
					dkmt_file.close()
			if lines:
				res = lines[0].strip()

				if res == 'restart':
					os.system("shutdown /r")
					send_message_text('restart thành công')
					sleep(180)

				elif (res == 'shutdown'):
					os.system("shutdown /s")
					send_message_text('shutdown thành công')
					sleep(180)

				elif (res == 'mo nhac'):
					send_message_text('Xin mời bạn chọn tên bài hát:\n1.Nhớ đêm giã bạn.\n2.Hoa cau vườn trầu.\n3.Chỉ là phù du.\n4.Tủi phận.')
					while True:
						check_message_text()
						lines = []

						if os.path.exists("dkmt.txt"):
							with open("dkmt.txt", "r", encoding="utf-8") as dkmt_file:
								lines = dkmt_file.readlines()
								dkmt_file.close()
						if lines:
							result = lines[0].strip()

							if (result == '1') or (result == '2') or (result == '3') or (result == '4') :
								break
					if (result == '1'):
						url2 = 'https://www.youtube.com/watch?v=w-m6zwlmlMo'
						webbrowser.open(url2)
						send_message_text('Đang phát nhớ đêm giã bạn.')
						sleep(240)

						mouse = Controller()
						mouse.position = (600, 400)
						mouse.press(Button.right)
						mouse.release(Button.right)
						mouse.move(40, 20)
						mouse.press(Button.left)
						mouse.release(Button.left)
						send_message_text('Video đang phát lặp lại.')

					if (result == '2'):
						url2 = 'https://www.youtube.com/watch?v=4CB175qsx3k'
						webbrowser.open(url2)
						send_message_text('Đang phát hoa cau vườn trầu.')
						sleep(240)

						mouse = Controller()
						mouse.position = (600, 400)
						mouse.press(Button.right)
						mouse.release(Button.right)
						mouse.move(40, 20)
						mouse.press(Button.left)
						mouse.release(Button.left)
						send_message_text('Video đang phát lặp lại.')

					if (result == '3'):
						url2 = 'https://www.youtube.com/watch?v=IZcaxCZc7Uw'
						webbrowser.open(url2)
						send_message_text('Đang phát chỉ là phù du.')
						sleep(240)

						mouse = Controller()
						mouse.position = (600, 400)
						mouse.press(Button.right)
						mouse.release(Button.right)
						mouse.move(40, 20)
						mouse.press(Button.left)
						mouse.release(Button.left)
						send_message_text('Video đang phát lặp lại.')

					if (result == '4'):
						url2 = 'https://www.youtube.com/watch?v=3arFjgeOyXE'
						webbrowser.open(url2)
						send_message_text('Đang phát tủi phận.')
						sleep(240)

						mouse = Controller()
						mouse.position = (600, 400)
						mouse.press(Button.right)
						mouse.release(Button.right)
						mouse.move(40, 20)
						mouse.press(Button.left)
						mouse.release(Button.left)
						send_message_text('Video đang phát lặp lại.')
				elif (res == 'tatnhac'):
					mouse = Controller()
					mouse.position = (1897, 14)
					mouse.press(Button.left)
					mouse.release(Button.left)
					send_message_text('Đã tắt nhạc.')
					sleep(30)
				else:
					pass

		# Phan code video.

		if (kt_yc_alertimagelancuoi is None) or ((datetime.datetime.utcnow() - kt_yc_alertimagelancuoi).total_seconds() > kt_yc_alertimagesau):
			kt_yc_alertimagelancuoi = datetime.datetime.utcnow()
			if os.path.exists('alert_image'):
				directory = 'alert_image/'
				files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
				latest_file = max(files, key=os.path.getctime)
				cap2 = os.path.basename(latest_file)
				if cap != cap2:
					send_text_photo(text = cap2, photo_path = latest_file)
					cap = cap2

		if (kt_yc_guianhlancuoi is None) or ((datetime.datetime.utcnow() - kt_yc_guianhlancuoi).total_seconds() > kt_yc_guianhsau):
			kt_yc_guianhlancuoi = datetime.datetime.utcnow()
					
			if os.path.exists('update_image'):
				directory = 'update_image/'
				files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
				latest_file = max(files, key=os.path.getctime)
				cap3 = os.path.basename(latest_file)

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
					send_message_text(cap5)
					cap4 = cap5

except Exception as e:
	restart_number()
	print(f'Lỗi: {e}')
	send_message_text(f'Lỗi: {e}, máy tính sẻ tự reset.')

except BaseException as e:
	restart_number()
	print(f'Chương trình bị lỗi, {e}, máy tính sẻ tự reset')
	send_message_text(f'Chương trình bị lỗi, {e}, máy tính sẻ tự reset')

finally:
	send_message_text('Lỗi main1.pyw. Máy tính sẻ tự reset sau 3 phút.')
	sleep(180)
	os.system("shutdown /r")