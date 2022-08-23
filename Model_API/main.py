from kafka import KafkaProducer
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from page_categorization import *
import json
import configparser
import os


class Input_Data(BaseModel):
    requestString: str
    searchInput: str
    host: str
    searchUrl: str
    href: str
    timeSpentOnPage: str
    longitude: str
    latitude: str
    locale: str
    timeSpentOnTask: str
    timeUnit: str
    ipAddress: str
    operatingSystem: str
    browserName: str
    city: str
    startDate: str
    startTime: str
    clickedUrl: str
    deviceName: str
    osVersion: str
    token: str
    questionId: int
    questionType: str
    other: str
    title: str
    videoLink: str
    audioLink: str
    cameraLink: str
    imageLink: str
    htmlLink: str
    respId: str
    surveyId: int
    responseTime: str
    topic: str


app = FastAPI()

config_file = "config/"+os.listdir('config')[0]
print(config_file)
def read_config():
  config = configparser.ConfigParser()
  config.read(config_file, encoding='utf-8')
  return config

@app.post("/pdp/")
async def pdp(input_data:Input_Data):
    print(input_data)
    config = read_config()
    input_data['htmlPath'] = input_data.htmlLink[input_data.htmlLink.find("/downloads/")+11:]

    # Call the PDP Model
    input_data['PageCategory'] = get_pdp(input_data['href'], input_data['htmlPath'])
    print(input_data['PageCategory'])
    producer = KafkaProducer(bootstrap_servers=eval(config['KafkaSettings']['bootstrap_servers']),
                        value_serializer=lambda x: 
                        json.dumps(x).encode('utf-8'))
    producer.send(config['KafkaSettings']['Produce_topic'], input_data)
    return input_data['PageCategory']
    