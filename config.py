import os
# from dotenv import load_dotenv
#
# load_dotenv()

PG_USER = os.getenv('PG_USER', 'admin1')
PG_PASSWORD = os.getenv('PG_PASSWORD', 'admin111')
PG_HOST = os.getenv('PG_HOST', '127.0.0.1')
PG_PORT = os.getenv('PG_PORT', 5433)
PG_DB = os.getenv('PG_DB', 'app_db')

PG_DSN = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}'
