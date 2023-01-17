Menu FastAPI project. 

Menu has submenu and submenu has dishes.
CRUD available for each layer.
Swagger docs are available 127.0.0.1:8000/docs
.env file with database parameters should be created in the root (example with tests info):
    PG_USER = 'admin'
    PG_PASSWORD = 'admin1'
    PG_HOST = '127.0.0.1'
    PG_PORT = 5431
    PG_DB = 'test_db'

for the simplicity, all files stored in the same folder including Postman tests.

After creation of .env file, virtualenv should be created and activated. Python 3.10 was used.
Requirements should be installed by next command "pip install -r requirements.txt"
Test database can be started simply by "docker-compose up" command
Afterwards "uvicorn main:menu_app" or "uvicorn main:menu_app --reload" should be run