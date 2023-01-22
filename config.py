import os
# from dotenv import load_dotenv
#
# load_dotenv()

PG_USER = os.getenv('PG_USER', 'admin')
PG_PASSWORD = os.getenv('PG_PASSWORD', 'admin1')
PG_HOST = os.getenv('PG_HOST', 'test_db')
PG_PORT = os.getenv('PG_PORT', 5432)
PG_DB = os.getenv('PG_DB', 'test_db')

PG_DSN = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}'
