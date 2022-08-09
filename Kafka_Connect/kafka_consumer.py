from kafka import KafkaConsumer
import mysql.connector
import json
import requests
import configparser
import threading


def read_config():
  config = configparser.ConfigParser()
  config.read('config/configurations.ini', encoding='utf-8')
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
    topic = msg.topic
    subdict = {'topic':str(topic), 'respId':str(msg_json['respId']), 'surveyId':str(msg_json['surveyId']), 'questionId':str(msg_json['questionId']), 'token':str(msg_json['token']), 'href':str(msg_json['href']), 'htmlLink':str(msg_json['htmlLink']), 'videoLink':str(msg_json['videoLink'])}
    print(config['APIServer']['pdp_endpoint'])
    response_api = requests.post(config['APIServer']['pdp_endpoint'], data=json.dumps(subdict)).json()
    print(response_api)
  except Exception as e:
    print(e)
    continue