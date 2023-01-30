Menu FastAPI project.

Menu has submenu and submenu has dishes.
CRUD available for each layer.
Swagger docs are available 127.0.0.1:8000/docs

.env file is not important anymore. All env. variables are in docker-compose file.

To run "deploy" version use standard docker-compose.yml with next command:

<mark>docker-compose up</mark>
(can be -d if you would like to use command line)

The tests cover all CRUD functions of the app. There are two options to run tests:

The first one run it totally isolated, with separate empty database which will be removed after tests. In order to run this one use docker-compose.isolated_test.yml file or run next command:

<mark>docker-compose -f docker-compose.isolated_test.yml up </mark>

The second one used for testing "deploy" version. Thus, previously you should run main server by command:


and after, just run tests which will influence main database! You can run by using next command:

<mark>docker-compose up</mark> <br>
<mark>docker-compose -f docker-compose.test.yml up</mark>
