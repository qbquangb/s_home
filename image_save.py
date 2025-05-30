from datetime import date, datetime

def luuanh(text):
	text = text
	now = datetime.now()
	now_str = str(now)

	now_str_replace1 = now_str.replace('-','')
	now_str_replace2 = now_str_replace1.replace(':', '')
	now_str_replace3 = now_str_replace2.replace('.', '')
	now_str_replace4 = now_str_replace3.replace(' ', '_')

	res1 = now_str_replace4[0:15]

	milisec_float_str = now_str_replace4[15:18] + '.' + now_str_replace4[18:21]
	milisec_float = float(milisec_float_str)
	milisec_round = round(milisec_float)
	if now_str_replace4[15] == '0':
		milisec_round_str = '0' + str(milisec_round)
	else:
		milisec_round_str = str(milisec_round)

	filename = text + res1 + '.' + milisec_round_str
	return filename


# import cv2
# import numpy as np

# # Đường dẫn đến tệp cấu hình và trọng số của YOLO
# config_path = 'model/yolov3.cfg'
# weights_path = 'model/yolov3.weights'
# class_names_path = 'model/classnames.txt'

# with open(class_names_path, 'r') as f:
# 	class_names = f.read().strip().split('\n')

# # Tải mô hình YOLO
# net = cv2.dnn.readNetFromDarknet(config_path, weights_path)

# # Đọc ảnh đầu vào
# image = cv2.imread('road.jfif')
# # image = cv2.resize(image, dsize=None, fx=0.2, fy=0.2)
# (H, W) = image.shape[:2]

# # Tạo blob từ ảnh đầu vào
# blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
# net.setInput(blob)

# layer_names = net.getLayerNames()
# output_layer_names = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# # Thực hiện dự đoán
# outputs = net.forward(output_layer_names)

# # Xử lý kết quả đầu ra
# boxes = []
# confidences = []
# class_ids = []

# for output in outputs:
# 	for detection in output:
# 		scores = detection[5:]
# 		class_id = np.argmax(scores)
# 		confidence = scores[class_id]
# 		if confidence > 0.5:
# 			box = detection[0:4] * np.array([W, H, W, H])
# 			(centerX, centerY, width, height) = box.astype("int")
# 			x = int(centerX - (width / 2))
# 			y = int(centerY - (height / 2))
# 			boxes.append([x, y, int(width), int(height)])
# 			confidences.append(float(confidence))
# 			class_ids.append(class_id)

# # Áp dụng NMS (Non-maxima suppression) để loại bỏ các bounding box chồng lấn
# indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
# print(len(indices))

# # Vẽ bounding box và tên lớp lên ảnh
# if len(indices) > 0:
# 	for i in indices.flatten():
# 		(x, y) = (boxes[i][0], boxes[i][1])
# 		(w, h) = (boxes[i][2], boxes[i][3])
# 		color = [int(c) for c in np.random.randint(0, 255, size=(3,))]
# 		cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
# 		text = "{}: {:.4f}".format(class_names[class_ids[i]], confidences[i])
# 		cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# # Hiển thị ảnh kết quả
# cv2.imshow('Image', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()