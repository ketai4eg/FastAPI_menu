Menu FastAPI project.

Menu has submenu and submenu has dishes.
CRUD available for each layer.
Swagger docs are available 127.0.0.1:8000/docs

.env file contains all parameters for the run deploy version.

To run "deploy" version use standard docker-compose.yml with next command:

<mark>docker-compose up</mark>
(can be -d if you would like to use command line)

The tests cover all CRUD functions of the app. There are two options to run tests:


The tests used for testing "deploy" version. Thus, previously you should run main server and
after, just run tests which will influence main database! You can run by using next command:

<mark>docker-compose up</mark> <br>
<mark>docker-compose -f docker-compose.test.yml up</mark>

in case you want to start from empty database you should clean volume data.

And second option is running isolated service just for tests. Here you need to run docker-compose.isolated_test.yml file by similar command: <br>
<mark>docker-compose -f docker-compose.isolated_test.yml up</mark>
