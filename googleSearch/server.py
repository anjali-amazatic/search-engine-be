import os
import sys
import waitress
from googleSearch.wsgi import application

BASE_DIR = os.path.join(os.path.dirname(__file__), 'src')
sys.path.append(BASE_DIR)

waitress.serve(
    application,
    host='0.0.0.0',
    port=os.getenv('PORT', '8000'))