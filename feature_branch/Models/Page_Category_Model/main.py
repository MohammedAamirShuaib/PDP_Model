from kafka import KafkaProducer
from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel
from pdp_model import *
import json
import configparser


class Input_Data(BaseModel):
    topic: str
    respId: str
    surveyId: str
    questionId: str
    token: str
    href: str
    htmlLink: str
    videoLink: str


app = FastAPI()

def read_config():
    config = configparser.ConfigParser()
    config.read('config/configurations.ini', encoding='utf-8')
    return config


@app.post("/pdp/")
async def pdp(input_data:Input_Data):
    config = read_config()
    topic= input_data.topic
    respId= input_data.respId
    surveyId= input_data.surveyId
    questionId= input_data.questionId
    token= input_data.token
    href= input_data.href
    htmlLink= input_data.htmlLink
    videoLink= input_data.videoLink
    htmlPath = htmlLink[htmlLink.find("/downloads/")+11:]

    # Call the PDP Model
    page_tag = get_pdp(href, htmlPath)

    # Sending data to Seisens though Kafka
    output_dict = {'topic':topic, 'respId':respId, 'surveyId':surveyId, 'questionId':questionId, 'token':token, 'href':href, 'htmlLink':htmlLink, 'videoLink':videoLink,'PageCategory':page_tag}
    producer = KafkaProducer(bootstrap_servers=eval(config['KafkaSettings']['bootstrap_servers']),
                        value_serializer=lambda x: 
                        json.dumps(x).encode('utf-8'))
    producer.send(config['KafkaSettings']['Produce_topic'], output_dict)
    return output_dict
    