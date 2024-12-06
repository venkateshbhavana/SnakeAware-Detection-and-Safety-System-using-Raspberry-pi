import tensorflow as tf
import sys
import time
import cv2
import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
buz=26
GPIO.setup(buz,GPIO.OUT)
GPIO.output(buz,0)
vs = cv2.VideoCapture(0)
time.sleep(3)
while(True):        
(grabbed, frame) = vs.read()      
  cv2.imshow('input',frame)      
  if cv2.waitKey(1) & 0xFF == ord('s'):            
Break
cv2.imwrite('test.jpg',frame)
cv2.waitKey(10)
image_path = 'test.jpg’
graph_file = "Venomous_nonVenomous_inception.pb"labels_txt = "snake_labels.txt“
with tf.gfile.FastGFile(graph_file, 'rb') as f:        graph_def = tf.GraphDef()        graph_def.ParseFromString(f.read())        _ = tf.import_graph_def(graph_def, name=‘’)
image_data = tf.gfile.FastGFile(image_path, 'rb').read()label_lines = [line.rstrip() for line in tf.gfile.GFile(labels_txt)]
