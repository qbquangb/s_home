try:
	import cv2
	import numpy as np
	from datetime import date, datetime
	import serial
	from time import sleep
	import datetime
	from image_save import luuanh
	import os
	from func import restart_number, send_message_text

	kt_update_anhlancuoi = None
	kt_update_anhsau = 300

	kt_baodonglancuoi = None
	kt_baodonghsau = 60

	python_uno = None
	data = None

	ser = serial.Serial(port='COM3', baudrate=9600, timeout=0.2)
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

	while True:

		sleep(1.5)

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
				if (ser.in_waiting == 0):
					python_uno = python_uno + '\r'
					python_uno = python_uno.encode()
					ser.write(python_uno)
					sleep(1.5)

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

		cv2.waitKey(1)
		cv2.imshow("Bao dong xam nhap.", frame)

	cv2.destroyAllWindows()

except Exception as e:
	restart_number()
	print(f'Lỗi: {e}')
	send_message_text(f'Lỗi: {e}, máy tính sẻ tự reset.')

except BaseException as e:
	restart_number()
	print(f'Chương trình bị lỗi, {e}, máy tính sẻ tự reset')
	send_message_text(f'Chương trình bị lỗi, {e}, máy tính sẻ tự reset')

finally:
	sleep(180)
	os.system("shutdown /r")