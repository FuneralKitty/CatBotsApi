
# CatBots API

This repository contains a solution for the [backend-cats-api task](https://github.com/itc-code/test-assignments/tree/main/backend-cats-api). The project is built with Flask and PostgreSQL, running in Docker containers.

## Overview

The CatBots API allows you to manage and query a database of cats. You can add new entries, retrieve lists of cats with specific attributes, and handle common operations through a RESTful interface.

### API Endpoints

- **Add a Cat (POST)**
  - Example:
    ```sh
    curl -X POST http://localhost:8080/cat \
    -H "Content-Type: application/json" \
    -d '{"name": "Tihon", "color": "red & white", "tail_length": 15, "whiskers_length": 12}'
    ```

- **Retrieve Cats (GET)**
  - Example:
    ```sh
    curl -X GET "http://localhost:8080/cats?attribute=color&order=asc&offset=5&limit=2"
    ```

## Installation

### Prerequisites

- Docker
- Docker Compose

### Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/python52course/CatBotsApi.git
   cd CatBotsApi
   ```
   1. Create an .env file:
       ```sh
      echo "POSTGRES_DB=wg_forge_db
            POSTGRES_USER=wg_forge
            POSTGRES_PASSWORD=42a
            FLASK_ENV=development
            FLASK_APP=app.py
            " > .env
   ```

2. **Build and Start the Containers:**
   You can use the provided Makefile for easy setup.

   - Build the Docker images:
     ```sh
     make build
     ```

   - Start the containers:
     ```sh
     make up
     ```

   Alternatively, you can manually build and start the containers:

   ```sh
   docker-compose -f docker-compose.yml build
   docker-compose -f docker-compose.yml up -d
   ```

3. **Check Available Make Commands:**
   For additional commands and help, run:
   ```sh
   make help
   ```

### Ports

- **Flask:** `8080` 
- **PostgreSQL:** `5432`

Ensure these ports are available and not used by other services.

## Testing

The repository includes unit tests using `pytest`. You can run tests inside the Docker container with the following command:

```sh
make test
```

## Dependencies

The following dependencies are managed within the Docker container, so you don’t need to install them manually:

- `psycopg`
- `Flask`
- `pytest`

## Additional Information

This API is designed to be simple and extendable. If you encounter any issues or have questions, please refer to the [GitHub issues](https://github.com/python52course/CatBotsApi/issues) for support.
