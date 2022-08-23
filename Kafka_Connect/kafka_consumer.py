from kafka import KafkaConsumer
import mysql.connector
import json
import requests
import configparser
import threading
import os

config_file = "config/"+os.listdir('config')[0]

print(config_file)
def read_config():
  config = configparser.ConfigParser()
  config.read(config_file, encoding='utf-8')
  return config

config = read_config()

consumer = KafkaConsumer(bootstrap_servers=eval(config['KafkaSettings']['bootstrap_servers']))
topic_list = list(consumer.topics())
listening_topics = []
for topic in topic_list:
  if topic.startswith(config['KafkaSettings']['Listen_topic_pattern']):
    listening_topics.append(topic)
consumer.subscribe(listening_topics)

class BackgroundTasks(threading.Thread):
    def run(self):
        while True:
          topic_list = list(consumer.topics())
          listening_topics = []
          for topic in topic_list:
            if topic.startswith(config['KafkaSettings']['Listen_topic_pattern']):
              listening_topics.append(topic)
          consumer.subscribe(listening_topics)

t = BackgroundTasks()
t.start()

for msg in consumer:
  try:
    config = read_config()
    msg_json = json.loads(msg.value.decode('utf-8'))
    msg_json['topic'] = msg.topic
    for key, value in msg_json.items():
      if value is None:
          msg_json[key] = ''
    response_api = requests.post(config['APIServer']['pdp_endpoint'], data=json.dumps(msg_json)).json()
    print(response_api)
  except Exception as e:
    print(e)
    continue