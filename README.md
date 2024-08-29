## Table of Contents
- [Project Structure](#project-structure)
- [Project Description](#project-description)
- [Installation and Setup](#installation-and-setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Configure Environment Variables](#2-configure-environment-variables)
  - [3. Docker build](#3-docker-builddocker-is-required)
  - [4. Manual setup](#4-manual-setuppostgresql-is-required)
  - [5. Run Tests](#5-tests)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
  - [1. Generate Secret](#1-generate-secret)
  - [2. Retrieve Secret](#2-retrieve-secret)
- [Notes](#notes)
---


## Project Structure
```plaintext
├── Dockerfile                    # Some additional commands for docker-compose file
├── .env                          # Keep here your data as it was demonstradted in the .env.example
├── .env.example                  # example
├── Makefile                      # Simple commands to manage with docker and postgresql
├── README.md                     
├── app.py                        # Main application with Flask
├── data.sql                      # Data for postgres
├── docker-compose.yml            # Docker-compose file helps to build and run the app in Docker
├── requirements.txt              # Requirements for the project
├── src
│   ├── __init__.py               # Package initialization
│   ├── arithmetic_for_cats.py    # Additional file with math logic 
│   ├── config.py                 # Configuration and environment variables loading
│   └── data_fullfilling.py       # Main logical database file
├── tests
│   ├── __init__.py               # Package initialization
│   └── test_app.py               # Tests for the app
└──start.sh                       # Simple script to run that app localy
```

## Project Description

This repository contains a solution for the [backend-cats-api task](https://github.com/itc-code/test-assignments/tree/main/backend-cats-api). 
The project is built with Flask and PostgreSQL, running in Docker containers.

The CatBots API allows you to manage and query a database of cats. You can add new entries, retrieve lists of cats with specific attributes, 
and handle common operations through a RESTful interface.

API Endpoints include **Add a Cat (POST)**, where you can add a cat by sending a JSON payload with attributes like name, color, tail length, 
and whiskers length. Another endpoint is **Retrieve Cats (GET)**, which allows you to retrieve a list of cats based on specific query parameters such as attribute and order.

---

## Installation and Setup

To install, you need to have Docker and Docker Compose otherwise you can do it manually. 

### 1. Clone the Repository
Begin by cloning the repository using the command:
```sh
git clone https://github.com/python52course/CatBotsApi.git
cd CatBotsApi
```
### 2. Configure Environment Variables
After cloning the app, you should create and fulfill **.env** file by the example in **.env.example** or you can use common data from that file.
### 3. Docker build(docker is required)
Build the project using Docker. Check that the Docker engine running.
The provided Makefile simplifies this process. First, build the Docker images with the command:
```sh
make build
```
Then, start the containers:
```sh
make up
```
Alternatively, you can build and start the containers manually using Docker Compose:
```sh
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d
```
Run `make help` to check available Make commands.

### 4. Manual setup(postgresql is required)
For manual setup, it's recommended to install PostgreSQL using your package manager (e.g., `sudo apt-get install postgresql-all` for Ubuntu) or use a UI client like `postgresapp.com` for macOS, or an installer from [EnterpriseDB](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads#windows) for Windows. After that, create a database and user for your project:

You need to enter to psql, then create user like **wg_forge** and give a password. Then to create Database and give all privileges to user. Also check that user, database and password are the same as those in your .env file.
```sh
su postgres -c psql
CREATE USER wg_forge WITH PASSWORD 'a42';
CREATE DATABASE wg_forge_db;
GRANT ALL PRIVILEGES ON DATABASE wg_forge_db TO wg_forge;
```
Then, run the SQL script `data.sql` on your database:
```sh
psql --host=localhost --port=5432 --dbname=wg_forge_db --username=wg_forge --password --file=wg_forge_init.sql
```

#### Running App
Make sure that ports 8080 (Flask):

```bash
python3 -m venv venv
source venv/bin/activate

python3 -m pip install --upgrade pip
pip3 install -r requirements.txt

flask --app app run --port 8080
```
---

## Tests

The repository includes unit tests using `pytest`. You can run the tests inside the Docker container with the command:
```sh
make test
```
---

## Dependencies

The project dependencies are managed within the Docker container, so you don’t need to install them manually. Key dependencies include `psycopg2`, `Flask`, `pydantic` and `pytest`.

---

## Additional Information

This API is designed to be simple and extendable. If you encounter any issues or have questions, please refer to the [GitHub issues](https://github.com/python52course/CatBotsApi/issues) for support.

---
