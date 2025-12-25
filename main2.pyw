import socket
import time
import cv2
import numpy as np
from datetime import date, datetime
import serial
from time import sleep
import datetime
from image_save import luuanh
import os
from func import restart_number
import sys

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
	from func import send_message_text

try:

	kt_update_anhlancuoi = None
	kt_update_anhsau = 600

	kt_baodonglancuoi = None
	kt_baodonghsau = 35

	python_uno = None
	data = None

	ser = serial.Serial(port='COM4', baudrate=9600, timeout=0.2)
	classnames_file = "model/classnames.txt"
	weights_file = "model/yolov3.weights"
	config_file = "model/yolov3.cfg"
	conf_threshold = 0.5
	nms_threshold = 0.4
	detect_class = "nguoi"
	scale = 1 / 255
	net = cv2.dnn.readNet(weights_file, config_file)
	with open(classnames_file, 'r') as f:
		classes = [line.strip() for line in f.readlines()]
	layer_names = net.getLayerNames()
	output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
	scale = 1 / 255

	video = cv2.VideoCapture(0)

	kt_response_lancuoi = None
	kt_response_sau = 60
	val2 = 0
	backSub = cv2.createBackgroundSubtractorMOG2(history=500)
	trigger = False

	while True:

		sleep(0.3)

		if kt_response_lancuoi is None or ((datetime.datetime.utcnow() - kt_response_lancuoi).total_seconds() > kt_response_sau):
			kt_response_lancuoi = datetime.datetime.utcnow()
			with open("response_main2.txt", "w") as file:
				file.write(str(val2))
				file.close()
			val2 += 1
			if val2 == 10000:
				val2 = 0

		while True:
			ret, frame = video.read()
			
			if ret:
				break
			else:
				continue
			
		frame = cv2.flip(frame, 1)
		
		fgMask = backSub.apply(frame, learningRate=-1)

		fgMask = cv2.cvtColor(fgMask, 0)

		kernel = np.ones((5,5), np.uint8)
		fgMask = cv2.erode(fgMask, kernel, iterations=1) 
		fgMask = cv2.dilate(fgMask, kernel, iterations=1)
		fgMask = cv2.GaussianBlur(fgMask, (3,3), 0)

		fgMask = cv2.Canny(fgMask,20,200)
		contours ,_ = cv2.findContours(fgMask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		for i in range(len(contours)):
			area = cv2.contourArea(contours[i])
			if area > 800:
				cv2.drawContours(fgMask, contours[i], 0, (0, 0, 255), 6)

		trigger = np.sum(fgMask > 0) > 2500  # Set threshold value as 1000 (adjust as needed)
		# if trigger:
		# 	print("Trigger activated.", file=sys.stdout, flush=True)
		# else:
		# 	print("No trigger detected.", file=sys.stdout, flush=True)
		
		if kt_update_anhlancuoi is None:
			kt_update_anhlancuoi = datetime.datetime.utcnow()
		elif ((datetime.datetime.utcnow() - kt_update_anhlancuoi).total_seconds() > kt_update_anhsau):
			kt_update_anhlancuoi = datetime.datetime.utcnow()
			if not os.path.exists('update_image'):
				os.mkdir('update_image')
			filename = luuanh('update')

			cv2.imwrite('update_image/' + filename + ".png", cv2.resize(frame, dsize=None, fx=0.20, fy=0.20))
			
		else:
			pass

		if trigger:

			frame_width = frame.shape[1]
			frame_height = frame.shape[0]
			blob = cv2.dnn.blobFromImage(frame, scale, (416, 416), (0, 0, 0), True, crop=False)
			net.setInput(blob)
			outs = net.forward(output_layers)

			class_ids = []
			confidences = []
			boxes = []

			for out in outs:
				for detection in out:
					scores = detection[5:]
					class_id = np.argmax(scores)
					confidence = scores[class_id]
					if (confidence >= conf_threshold) and (classes[class_id] == detect_class):
						center_x = int(detection[0] * frame_width)
						center_y = int(detection[1] * frame_height)
						w = int(detection[2] * frame_width)
						h = int(detection[3] * frame_height)
						x = center_x - w / 2
						y = center_y - h / 2
						class_ids.append(class_id)
						confidences.append(float(confidence))
						boxes.append([x, y, w, h])

			indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

			for i in indices:
				box = boxes[i]
				x = box[0]
				y = box[1]
				w = box[2]
				h = box[3]
				label = str(classes[class_ids[i]])
				color = (0, 255, 0)
				cv2.rectangle(frame, (round(x), round(y)), (round(x + w), round(y + h)), color, 2)
				cv2.putText(frame, label, (round(x) - 10, round(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

			if (len(indices) > 0):
				cv2.putText(frame, "BAO DONG CO NGUOI.", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

				if kt_baodonglancuoi is None or ((datetime.datetime.utcnow() - kt_baodonglancuoi).total_seconds() > kt_baodonghsau):
					kt_baodonglancuoi = datetime.datetime.utcnow()
						
					if not os.path.exists('alert_image'):
						os.mkdir('alert_image')
					filename = luuanh('alert_image')
					cv2.imwrite('alert_image/' + filename + ".png", cv2.resize(frame, dsize=None, fx=0.40, fy=0.40))

					python_uno = 'bat'
					# if (ser.in_waiting == 0):
					python_uno = python_uno + '\r'
					python_uno = python_uno.encode()
					ser.write(python_uno)
					sleep(0.75)

					# if (ser.in_waiting > 0):
					data = ser.readline()
					data = data.decode()
					data = data.rstrip()
					if not os.path.exists('alert_notification'):
						os.mkdir('alert_notification')
					filename = luuanh(data)
					with open('alert_notification/' + filename + '.txt', "w") as file:
						file.write(filename)
						file.close()

				else:
					pass

			if (ser.in_waiting > 0):
				data = ser.readline()
				data = data.decode()
				data = data.rstrip()
				if not os.path.exists('alert_notification'):
					os.mkdir('alert_notification')
				filename = luuanh(data)
				with open('alert_notification/' + filename + '.txt', "w") as file:
					file.write(filename)
					file.close()
			trigger = False

		cv2.waitKey(1)
		cv2.imshow("Bao dong xam nhap.", frame)

except Exception as e:
	restart_number()
	print(f'err: {e}', file=sys.stderr, flush=True)
	if isConnected:
		send_message_text(f'Chương trình bị lỗi, {e}, máy tính sẻ tự reset')
except BaseException as e:
	restart_number()
	print(f'err {e}', file=sys.stderr, flush=True)
	if isConnected:
		send_message_text(f'Chương trình bị lỗi, {e}, máy tính sẻ tự reset')
finally:
	cv2.destroyAllWindows()
	if isConnected:
		send_message_text('Lỗi main2.pyw. Máy tính sẻ tự reset sau 3 phút.')
	sleep(180)
	os.system("shutdown /r")
	sleep(180)