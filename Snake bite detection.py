import tensorflow as tf
import sys
import time
import cv2
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
import telepot
import telepot
import time
import cv2
import requests
buz=26
GPIO.setup(buz,GPIO.OUT)
GPIO.output(buz,0)
vs = cv2.VideoCapture(0)
time.sleep(3)
def handle(msg):
 global cap
 global telegramText
 global chat_id
 global receiveTelegramMessage
 global inp
 content_type, chat_type, chat_id = telepot.glance(msg)
 print(content_type)
 if content_type == 'photo':
 
 inp=1
 bot.download_file(msg['photo'][-1]['file_id'], './img.jpg')
 cap = cv2.VideoCapture('img.jpg')
 image_path = 'test.jpg'
 graph_file = "Venomous_nonVenomous_inception.pb"
 labels_txt = "snake_labels.txt"
 with tf.gfile.FastGFile(graph_file, 'rb') as f:
 graph_def = tf.GraphDef()
 graph_def.ParseFromString(f.read())
 _ = tf.import_graph_def(graph_def, name='')
 image_data = tf.gfile.FastGFile(image_path, 'rb').read()
 label_lines = [line.rstrip() for line in tf.gfile.GFile(labels_txt)]
 with tf.Session() as sess:
 softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
 predictions = sess.run(softmax_tensor,{'DecodeJpeg/contents:0': 
image_data})
 top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
 temp = ['','']
 i=0
 for node_id in top_k:
 
 human_string = label_lines[node_id]
 score = predictions[0][node_id]
 print('%s (score = %.5f)' % (human_string, score))
 bot.sendMessage(chat_id, '%s (score = %.5f)' % (human_string, 
score))
 print(score)
 i=i+1
 if(i==1 and score>0.5):
 GPIO.output(buz,1)
print('buzzer on')
 time.sleep(5)
 print('buzzer off')
 GPIO.output(buz,0)
 
 
 
 if content_type == 'video':
 inp=2
 file_id = msg['video']['file_id']
 # Use the file ID to download the video
 file_info = bot.getFile(file_id)
 video_url = 
'https://api.telegram.org/file/bot{}/{}'.format('6035550747:AAHlf0nEosKZ0HApKLjWXtDn1
OSTZu6Fa6k', file_info['file_path'])
 video_file = requests.get(video_url)
 # Save the video to a file
 with open('video.mp4', 'wb') as f:
 f.write(video_file.content)
 bot.sendMessage(chat_id, 'Video downloaded.')
 cap = cv2.VideoCapture('video.mp4')
 
 
 if content_type == 'text':
 
 chat_id = msg['chat']['id']
 telegramText = msg['text']
 print("Message received from " + str(chat_id))
 print("Message " + str(telegramText))
 
def capture():
 
 print("Sending photo to " + str(chat_id))
 bot.sendPhoto(chat_id, photo = open('./image.jpg', 'rb'))
time.sleep(2)
bot = telepot.Bot('6035550747:AAHlf0nEosKZ0HApKLjWXtDn1OSTZu6Fa6k')
chat_id='6287775346'
bot.message_loop(handle)
print("Telegram bot is ready")
bot.sendMessage(chat_id, 'BOT STARTED')
while(True):
 (grabbed, frame) = vs.read()
 cv2.imshow('input',frame)
 if cv2.waitKey(1) & 0xFF == ord('s'):
 break
cv2.imwrite('test.jpg',frame)
cv2.waitKey(10)
image_path = 'test.jpg'
graph_file = "Venomous_nonVenomous_inception.pb"
labels_txt = "snake_labels.txt"
with tf.gfile.FastGFile(graph_file, 'rb') as f:
 graph_def = tf.GraphDef()
 graph_def.ParseFromString(f.read())
 _ = tf.import_graph_def(graph_def, name='')
image_data = tf.gfile.FastGFile(image_path, 'rb').read()
label_lines = [line.rstrip() for line in tf.gfile.GFile(labels_txt)]
with tf.Session() as sess:
 softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
 predictions = sess.run(softmax_tensor,{'DecodeJpeg/contents:0': image_data})
 top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
 temp = ['','']
 i=0
 for node_id in top_k:
 
 human_string = label_lines[node_id]
 score = predictions[0][node_id]
 print('%s (score = %.5f)' % (human_string, score))
 print(score)
 i=i+1
 if(i==1 and score>0.5):
 GPIO.output(buz,1)
 print('buzzer on')
 time.sleep(5)
 print('buzzer off')
 GPIO.output(buz,0)
