# AWS Selenium Scraper  

## Overview
  Python web scraper that uses Selenium library to scrape data from a website and store it in a Postgres database. \
  The scraper is deployed to AWS ECS and runs on a schedule using AWS Events. 

## Prerequisites
### AWS
Follow the installation instructions to install AWS CDK V2: 
https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html

### Docker
Follow the installation instructions to install Docker:
https://docs.docker.com/desktop/

### dbmate
Follow the installation instructions to install dbmate:
https://github.com/amacneil/dbmate

To manage database migrations and ensure the smooth operation of your project, you need to set up a configuration file named `.env` in the project root folder. \
This `.env` file is essential for configuring the database connection for `dbmate`.

#### Create .env file
```bash
ENV_PATH=".env"

if [ ! -f $ENV_PATH ]; then
    echo "DATABASE_URL=postgres://postgres:S3cret@127.0.0.1:5432/postgres?sslmode=disable" >> $ENV_PATH
    echo "DEV=postgres://username:password@host:port/database" >> $ENV_PATH
    echo "PROD=postgres://username:password@host:port/database" >> $ENV_PATH
fi
```
Make sure to replace the placeholders with your actual database connection details.
DATABASE_URL varibale is used as a default value for dbmate commands. You can override it with --e flag.
```bash
dbmate -e DEV status
```

**Example dbmate Commands:**

- To create a new migration:
  ```
  dbmate new migration_name
  ```

- To apply pending migrations:
  ```
  dbmate up
  ```

- To check the status of migrations:
  ```
  dbmate status
  ```


The `.env` file is necessary to provide your application with the required configuration information, \
especially the `DATABASE_URL`. This URL specifies how your application can connect to your PostgreSQL database.

`DATABASE_URL` example:
```
postgres://postgres:S3cret@127.0.0.1:5432/postgres?sslmode=disable
```
- `postgres://`: Indicates that you are using the PostgreSQL protocol.
- `postgres`: Specifies the username for the database.
- `S3cret`: Specifies the password for the database (ensure it's secure).
- `127.0.0.1`: Indicates the database server's IP address.
- `5432`: Specifies the database server's port.
- `postgres`: Specifies the database name.
- `?sslmode=disable`: Disables SSL for local development. Ensure proper security settings for production environments.


### Poetry
Follow the installation instructions to install Poetry:
https://python-poetry.org/docs/#installation

### Python
The project was developed using Python **3.9.16**
Check you python version: 
```bash 
python --version
```

### Make
Follow the installation instructions to install Make:
https://www.gnu.org/software/make/

## Running locally

### Python

To run the project locally using python, you need to install the project dependencies using Poetry:

```bash
poetry install
```

You also need to start the database using docker:
```bash
make up-db
```

Then you can run the project using:
```bash
poetry run python src/index.py
```
You can also run the tests using:
```bash
poetry run python -m unittest tests/test_scrape.py
```

### Docker

To run the project inside a docker container with a database run the following command:
```bash
make start
```
This command will rebuild the images if changes are detected. \
To start the app container and connect to it's terminal run:
```bash
make terminal
```

## Deploy to AWS
By default the project is deployed using your aws credentials stored in `~/.aws/credentials` and the configuration stored in `~/.aws/config`.
Run the following command to deploy the project to AWS:
```bash
make deploy
```
Run the following command to cdk changes the project to AWS:
```bash
make diff
```