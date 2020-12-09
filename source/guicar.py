import os
import sys

# import some PyQt5 modules
from typing import List, Any

from PyQt5 import QtGui
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QFileDialog, QSlider, QLabel, QHBoxLayout
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer

# import Opencv module
import cv2
import math
import numpy as np
import maincar

from intgui import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.init()
        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)

        self.getpathButton.clicked.connect(self.getImage)
        self.runButton.clicked.connect(self.controlTimer)
        self.horizontalSlider.valueChanged.connect(self.update_first_frame)
        self.horizontalSlider_2.valueChanged.connect(self.update_first_frame)

    def startline(self):
        size = self.horizontalSlider.value()
        self.label_3.setText(str(size))

    def endline(self):
        size_1 = self.horizontalSlider_2.value()
        self.label_4.setText(str(size_1))

    def init(self):
        self.START_POINT = 0
        self.END_POINT = 0
        self.CLASSES = ["car", "motorcycle", "bus", "truck"]
        # Define vehicle class
        self.VEHICLE_CLASSES = [0, 1, 2, 3]

        self.YOLOV3_CFG = 'yolov3.cfg'
        self.YOLOV3_WEIGHT = 'yolov3_5000.weights'

        self.CONFIDENCE_SETTING = 0.4
        self.YOLOV3_WIDTH = 416
        self.YOLOV3_HEIGHT = 416

        self.MAX_DISTANCE = 80
        self.colors = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))

        # Load yolo model
        self.net = cv2.dnn.readNetFromDarknet(self.YOLOV3_CFG, self.YOLOV3_WEIGHT)
        self.number_frame = 0
        self.number_vehicle = 0
        self.list_object = []
        self.skip_frame =1

    def getImage(self):
        test_path = os.path.join(os.getcwd(), "vehicles_counting")
        fname = QFileDialog.getOpenFileName(self, 'Open file', test_path, "Image files (*.jpg *.mp4 *.gif)")
        self.imagePath = fname[0]
        self.number_vehicle = 0
        # print(self.imagePath)

    def update_first_frame(self):
        self.cap = cv2.VideoCapture(self.imagePath)
        _, frame = self.cap.read()
        height, width, channel = frame.shape
        step = channel * width
        self.START_POINT = self.horizontalSlider.value()
        self.END_POINT = self.horizontalSlider_2.value()
        # Draw start line
        cv2.line(frame, (0, self.START_POINT), (width, self.START_POINT), (0, 255, 0), 1)
        # Draw end line
        cv2.line(frame, (0, height - self.END_POINT), (width, height - self.END_POINT), (255, 0, 0), 2)
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.output_img.setPixmap(QPixmap.fromImage(qImg))
        self.cap.release()
        self.startline()
        self.endline()


    # view camera
    def viewCam(self):

        # read image in BGR format
        ret_val, image = self.cap.read()
        # convert image to RGB format
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # get image info
        height, width, channel = frame.shape
        # print(height, width)
        step = channel * width
        # process
        while True:
            self.number_frame += 1
            # Tracking old object
            tmp_list_object = self.list_object
            self.list_object = []
            for obj in tmp_list_object:
                tracker = obj['tracker']
                class_id = obj['id']
                confidence = obj['confidence']
                check, box = tracker.update(frame)
                if check:
                    box_x, box_y, box_width, box_height = box
                    maincar.draw_prediction(self.CLASSES, self.colors, frame, class_id, confidence,
                                    box_x, box_y, box_width, box_height)
                    obj['tracker'] = tracker
                    obj['box'] = box
                    if maincar.check_location(box_y, box_height, height):
                        # This object passed the end line
                        self.number_vehicle += 1
                    else:
                        self.list_object.append(obj)
            if self.number_frame % self.skip_frame == 0:
                # Detect object and check new object
                boxes, class_ids, confidences = maincar.detections_yolo3(self.net, frame, self.CONFIDENCE_SETTING, self.YOLOV3_WIDTH,
                                                             self.YOLOV3_HEIGHT, width, height, classes=self.CLASSES)
                for idx, box in enumerate(boxes):
                    box_x, box_y, box_width, box_height = box
                    if not maincar.check_location(box_y, box_height, height):
                        # This object doesnt pass the end line
                        box_center_x = int(box_x + box_width / 2.0)
                        box_center_y = int(box_y + box_height / 2.0)
                        check_new_object = True
                        for tracker in self.list_object:
                            # Check exist object
                            current_box_x, current_box_y, current_box_width, current_box_height = tracker['box']
                            current_box_center_x = int(current_box_x + current_box_width / 2.0)
                            current_box_center_y = int(current_box_y + current_box_height / 2.0)
                            # Calculate distance between 2 object
                            distance = math.sqrt((box_center_x - current_box_center_x) ** 2 +
                                                 (box_center_y - current_box_center_y) ** 2)
                            if distance < self.MAX_DISTANCE:
                                # Object is existed
                                check_new_object = False
                                break
                        if check_new_object and maincar.check_start_line(box_y, box_height):
                            # Append new object to list
                            new_tracker = cv2.TrackerKCF_create()
                            new_tracker.init(frame, tuple(box))
                            new_object = {
                                'id': class_ids[idx],
                                'tracker': new_tracker,
                                'confidence': confidences[idx],
                                'box': box
                            }
                            self.list_object.append(new_object)
                            # Draw new object
                            maincar.draw_prediction(self.CLASSES, self.colors, frame, new_object['id'], new_object['confidence'],
                                            box_x, box_y, box_width, box_height)
            # Put summary text
            cv2.putText(frame, "Number : {:03d}".format(self.number_vehicle), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 0, 255), 2)
            # Draw start line
            cv2.line(frame, (0, self.START_POINT), (width, self.START_POINT), (0, 255, 0), 1)
            # Draw end line
            cv2.line(frame, (0, height - self.END_POINT), (width, height - self.END_POINT), (255, 0, 0), 2)
            break

        # create QImage from image
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.output_img.setPixmap(QPixmap.fromImage(qImg))

    # start/stop timer
    def controlTimer(self):
        self.START_POINT = self.horizontalSlider.value()
        self.END_POINT = self.horizontalSlider_2.value()
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(self.imagePath)
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.runButton.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.runButton.setText("Start")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()