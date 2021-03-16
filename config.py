import os

PRODUCTION = os.getenv('PRODUCTION')

PORT = int(os.environ.get("PORT", 5000))
PRODUCTION_HOST = '0.0.0.0'
LOCAL_HOST = '127.0.0.1'
