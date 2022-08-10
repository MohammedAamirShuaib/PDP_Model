from bs4 import BeautifulSoup
import boto3
import configparser

def read_config():
    config = configparser.ConfigParser()
    config.read('config/configurations.ini', encoding='utf-8')
    return config

def search_engine(URL):
    config = read_config()
    for key in eval(config['PageCategory']['search_engine_page']):
        if URL.count(key,0,35) > 0:
            return True


def social_media(URL):
    config = read_config()
    for key in eval(config['PageCategory']['social_media_page']):
        if URL.count(key,0,45) > 0:
            return True

def pdp_page(URL):
    config = read_config()
    for key in eval(config['PageCategory']['pdp']):
        matching = all(x in URL for x in key)
        if matching:
            return True

def search_page(URL):
    config = read_config()
    for key in eval(config['PageCategory']['search']):
        matching = all(x in URL for x in key)
        if matching:
            return True

def deal_page(URL):
    config = read_config()
    for key in eval(config['PageCategory']['deal']):
        matching = all(x in URL for x in key)
        if matching:
            return True

def reviews_page(URL):
    config = read_config()
    for key in eval(config['PageCategory']['reviews']):
        matching = all(x in URL for x in key)
        if matching:
            return True

def cart_page(URL):
    config = read_config()
    for key in eval(config['PageCategory']['cart']):
        matching = all(x in URL for x in key)
        if matching:
            return True

def category_page(URL):
    config = read_config()
    for key in eval(config['PageCategory']['category']):
        matching = all(x in URL for x in key)
        if matching:
            return True
        elif all(x in URL for x in ['amazon','i=']) and \
             all(x not in URL for x in ['k='] ):
              return True



def get_pdp(URL,html_path):
    config = read_config()
    if search_engine(URL):
        return "search_engine_page"
    elif social_media(URL):
        return "social_media_page"
    elif pdp_page(URL):
        return "pdp_page"
    elif search_page(URL):
        return "search_page"
    elif deal_page(URL):
        return "deal_page"
    elif reviews_page(URL):
        return "reviews_page"
    elif cart_page(URL):
        return "cart_page"
    elif category_page(URL):
        return "category_page"
    else:
        client = boto3.client(
            service_name='s3',
            region_name='us-east-1',
            aws_access_key_id=config['S3Settings']['aws_access_key_id'],
            aws_secret_access_key=config['S3Settings']['aws_secret_access_key'])
        html_obj = client.get_object(Bucket=config['S3Settings']['bucket'], Key=html_path)
        body = html_obj['Body']
        html_content = body.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.find_all(text=True)
        if text == None:
            return "No Data"
        else:
            new = []
            for i in text:
                new.append(i.lower())
            keys = eval(config['HTML_Keywords']['pdp'])
            pdp = [i for i in new if i in keys]
            if len(pdp) > 0 and len(pdp)< 10:
                return "pdp_page"
            else:
                return "other_page"
