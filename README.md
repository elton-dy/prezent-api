# Prezent

Application that lets you find the perfect gift with the help of an AI.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation

To get the project up and running locally, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/elton-dy/prezent-api.git 
cd prezent-api
```

2. Copy the .env.example file to a new file called .env and update it with your local settings:

```bash
cp .env.example .env
```

3. Build and run the containers with Docker Compose:

```bash
docker-compose up --build
```
## Database Setup

After setting up your environment variables but before starting the application, you need to make and apply the database migrations. Follow these steps to set up the database schema:

```bash
# Start up the Docker services in detached mode
docker-compose up -d

# Run the migrations to create the database schema
docker-compose exec api python manage.py migrate
```

## Database Initialization

To populate your database with initial data or to create your vector database, run the custom management command provided with the project:

```bash

# Execute the custom Django management command to process the CSV file
docker-compose exec api python manage.py process_csv data/cadeaux.csv
```
This command will process the specified CSV file and populate your database as required. Make sure that your CSV file is located in the correct directory that the process_csv command expects.
