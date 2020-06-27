# Casting Agency API
This project is an API that helps manage actors and 
movies. Actors and movies can be created,
retrieved, updated, and deleted at the corresponding
resources. The relationship between actors and movies
can also be updated from either resources.

The project follows [Pep8 style guidelines](https://www.python.org/dev/peps/pep-0008/) for formatting code.

## Getting Started
### PosgtreSQL Database
A PostgreSQL database is needed to run the application.
A url can be provided to the application via the 
`DATABASE_URL` environment variable. Alternatively,
the application accepts the database name, username,
host, and password can be provided with the `DB_NAME`,
`DB_USER`, `DB_HOST`, `DB_PASSWORD` environment variables.

PostgreSQL should be installed locally for local development.
Installation instructions can be found on the [Postgres site](https://www.postgresqltutorial.com/install-postgresql/).
Alternatively, Digitalocean offers a great [tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04) 
for installing PostgreSQL on Ubuntu, CentOS, and Debian
system.

By default, the application connects to a database at 
`localhost` using port `5432`. The default username is 
`casting_api`. The database user must have a database
password when the application is run from a Linux 
distro such as Ubuntu.

#### Local Database Setup (Linux System)
Follow these steps to set up the database:
  - Activate the **postgres** user with the command:
    ```
    sudo -i -u postgres
    ```
  - Create a database named `casting` with the command:
    ```
    createdb casting
    ```
  - Create a test database named `casting_test` with the command:
    ```
    createdb casting_test
    ```
  - Create a user named `casting_api` with the command:
    ```
    createuser --interactive
    ```
    - The command will ask a series of questions that can all be answered with a no
    - **NOTE**: Answering no to all the questions is fine since the user is only needed
      to give the app access to the database and does not need to manage the database or tables
  - Run the psql interpretor with the command:
    ```
    psql
    ```
  - To change the database user password, run the psql command:
    ```
    \password casting_api
    ```
    - This password is needed to connect the application to the local database
    - **NOTE**: This step is necessary to connect to the database using password based 
      authentication on Linux machines instead of peer based authentication.
      By default, password based authentication is required by the psycopg2 
      library when connecting to postgres on some Linux distros
  - Exit the psql interpretor using the psql command `\q` 
  - From the root project directory, run the command:
    ```
    flask db upgrade
    ```
    - The command will create the tables defined in the `migrations` directory
  - Run the `exit` command to exit out of the postgres user shell login

#### Verify Local Database Setup Works
Connect to the database with the command:
```
psql casting --username casting_api --host localhost
```
  - Providing the `--host` or `-h` flag will ask for the database user password instead of
    attempting peer authentication using the system user

Display the `casting` database tables with the commannd:
```
\dt
```

Display the `actor` schema with the command:
```
\d questions
```

Display the `actor` table rows using the command:
```
SELECT * FROM questions;
```

### Flask Web API
The web API uses Python and Flask. For this project, Anaconda is used to manage 
Python packages and the virtual environments. Installation instructions can be found on the [Conda documentation](https://docs.conda.io/projects/continuumio-conda/en/latest/user-guide/install/index.html#) 
page. For a lean installation of just the conda command, there are instructions for installing
Miniconda as well.

#### Virtual Environment
Creating a virtual environment is recommended to keep the project packages separate from any 
Python packages that may be installed on the host computer. The conda command provided by
Anaconda or Miniconda, will be used to manage the virtual environment.

To create the python environment run the command:
```
conda env create --file environment.yml
```

To use a different environment name, use the `--name` flag when running the command:
```
conda env create --file environment.yml --name alternate_name
```

To export the current environment, run the command:
```
conda env export --file environment.yml
```

The last line in the `environment.yml` file can be removed, since it contains the
path where the environment is installed on the host computer and does not affect the
creation of the environment on other computers.

#### Additional Dependencies
On a Linux system, it may be neccessary to install additional dependencies
to allow the psycopg2 Python library to communicate with PostgreSQL. The dependencies are
`python-psycopg2` and `libpq-dev` and can be installed on Ubuntu using the command:
```
apt install python-psycopg2 libpq-dev
```

#### Running the Web API
Activate the virtual environment with the command:
```bash
conda activate casting_agency 
```

Traverse to the root project directory and create these Flask app environment variables:
```
export FLASK_APP=app
export FLASK_ENV=development
```
  - FLASK_APP tells Flask the name of the file or module the app is located in
  - When FLASK_ENV is set to developmet, Flask restarts the app whenever a file is updated

From the root project directory, run the command
```
flask run
```

The application will also run using the command:
```
python app.py
```

There will be a message similar to:
```
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 867-874-182
```

The web API will be available at the url in the output. In this case at
`http://127.0.0.1:5000/`.

#### Running Integration Tests
The integration tests are located in `tests` directory and
are split into separate files for each resource endpoint.
The tests expect the database name to be `casting_test`.
The tests also expect authentication bearer tokens to be
provided for Assistant, Director, and Executive roles using
the `ASSISTANT_TOKEN`, `DIRECTOR_TOKEN`, and `EXECUTIVE_TOKEN`
environment variables, respectively.

Run the tests with the command:
```
python -m unittest
```

Run specific tests by appending the relative test filename:
```
python -m unittest tests/test_health.py
```

**NOTE**: The tests only run from the root project directory.