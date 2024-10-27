Eghbali - Play Store Crawler and Analysis

this Project is a complete system for crawling the Play Store, collecting and managing application data, and analyzing data using Metabase. This project allows you to easily store and analyze information about various applications.

Contents

- Features
- Prerequisites
- Setup
- Running Tests
- Using API
- Using Swagger
- Crawling the Play Store
- Data Analysis with Metabase
- Useful Docker Commands
- Support

Features

- Play Store Crawling: Automatically collects information about applications.
- Application Management: Add, delete, and update applications in the database using Django rest_framework.
- API Documented with Swagger: Documents all API routes and methods.
- Data Analysis with Metabase: Display and analyze data using interactive dashboards.
- Easy Setup with Docker: Use Docker and Docker Compose for quick project setup.

Prerequisites

Before setting up the project, make sure you have the following prerequisites installed on your system
other Prerequisites will be installed Automatically.

- Docker
- Docker Compose

Setup

1. Clone the Repository

First, clone the repository:

git clone https://gitlab.com/sahabino403/eghbali.git
cd eghbali

2. Build and Start Services

Use Docker Compose to build and start the services:

docker-compose up --build

3. View Logs

To view the service logs:

docker-compose logs -f

4. Access the Django Application

After setup, the application is accessible in the browser at the following address:

http://0.0.0.0:8000/


$$$Working with database using urls:

to get Applications list use:

http://0.0.0.0:8000/api/app-names/

you can post json to create new Application

to update an Application use:

http://0.0.0.0:8000/api/app-names/{id}

you can put json to update an Application

if you want to delete that Application you should press the delete button


$$$Crawling the Play Store

Running the Crawler

The Play Store crawler is located in the file `crawler.py`. To run the crawler:

docker-compose exec web python crawler.py

This crawler collects application data and stores it in the PostgreSQL database.
I used redis for storing informations in a queue and I also used postgresql to storing data in data base
if you want to add other applications to crawl you should use http://0.0.0.0:8000/api/app-names/
link to create your own application

this application crawls th playstore every 1 hour and store the data in database for Data Analysis with Metabase


$$$Running Tests

To run the unit tests, use the following command:

docker-compose exec web python manage.py test

Additionally, to run the tests concurrently with the server, add the following line to the Dockerfile:

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000 & python manage.py test"]


$$$Using Swagger

To view and use the Swagger UI, visit the following address:

http://0.0.0.0:8000/swagger/

Here you can view all the methods and routes of the API and test them. If specific parameters are needed for API methods, you can enter them here and test the methods.


$$$Data Analysis with Metabase

Accessing Metabase

To access Metabase and view dashboards and data analysis, go to the following address:

http://localhost:3000/

Creating Charts and Dashboards

In Metabase, you can ask questions about the data available in the database and use various types of charts to display the data. Some useful analyses may include:

- Displaying charts of changes in app ratings in each app category based on overall rating and review scores.
- Analyzing the rise or fall of install numbers and reviewing trends.

Viewing Trends

To view trends in Metabase, simply use the filtering and time grouping features in the "Ask a Question" section.


$$$Useful Docker Commands

Stopping and Removing Services

To stop and remove all services:

docker-compose down

Viewing Active Containers

To view all running containers:

docker ps

Viewing Logs of a Specific Container

To view logs of a specific container:

docker logs <container_name_or_id>

Accessing Container Shell

To access the Django container shell:

docker-compose exec web bash


Support

If you encounter any issues using the project, please contact us:

- Email: amirmahdi82.ae@gmail.com
- Gitlab: Amirmahdi_Eghbali
