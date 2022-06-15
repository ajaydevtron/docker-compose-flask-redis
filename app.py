import time
import os
import redis
from flask import Flask

hostname=os.getenv('REDIS_HOSTNAME')
password=os.getenv('REDIS_PASSWORD')
port=os.getenv('REDIS_PORT')
# host='localhost',port=6379,db=0,password='Prabhat'
app = Flask(__name__)
cache = redis.Redis(host=hostname,port=port,password=password)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return '<h2> Hello World! We have been seen {} times.\n <h2>'.format(count)