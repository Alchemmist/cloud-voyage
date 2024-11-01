import os
import redis
from flask import Flask
from flask_cors import CORS
from flask_caching import Cache


app = Flask(__name__)
CORS(app)

cache = redis.Redis(host='redis', port=6379, password=os.getenv("REDIS_PASSWORD"))
CACHE_EXPIRATION = 3600


