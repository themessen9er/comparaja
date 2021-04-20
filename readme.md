# Requirements
In order to execute the services contained in the current solution, it is advised that the following technologies be used:

1. Docker - Build and launch containers for each individual service.

2. Docker-compose - Orchestrate the launch of, and access across all services.


# General system design
The components being delivered as a response to the technical challenge have all been designed to execute in docker linux containers.

There are 3 services that comprise the system:
1. backend - Provides a single HTTP API endpoint to a filtered list of products. It is written using the Python programming language.
2. db - A postgresql database that is seeded at first launch with the data contained inside the provided CSV files. The initial seeding also creates the necessary tables and views.
3. frontend - A Browser-based single-page web application that fetches a list of products from [backend] and presents these in the user's browser. It is written in javascript, using Vue.js 


# Build and launch
In order to build the solution in a local machine and launch the all services simultaneously:

1. Open a terminal window
2. Navigate to the root of the repository, which contains the docker-compose.yaml file.
3. run the following command:
    $ docker-compose up

Note: The services will be built on the first time this command is executed. This may take a few minutes. After the services have been built, they will be launched automatically.

After the services have finished being launched, they will become available at the following addresses:

1. backend - http://localhost:5000
2. frontend - http://localhost:5050
3. db - postgres://postgres:super-safe-pwd@localhost:5435/comparaja


# Using the services online
An instance of the 'frontend' and 'backend' services is publicly available at the following address:

- frontend : http://ec2-52-49-96-189.eu-west-1.compute.amazonaws.com
- backend: http://ec2-52-49-96-189.eu-west-1.compute.amazonaws.com:5000/products

Note: These services are made available on the AWS cloud platform.


# Challenge

## API Design & Implementation

1. For the database, PostgreSQL is used as the engine of choice. It is launched from the default official docker container. The configuration for this service may be found in the file 'docker-compose.yaml' located in the root of this repository. It is the service under the name 'db'.

In order to launch the 'db' service by itself, run the command frim the repository root directory:

    $ docker-compose up db

During the first execution of this service, the container's bootstrap procedure will run any SQL scripts contained in a specified directory. This is used in order to seed the database.
The contents of this directory are located in:

    {repo_root}/db/seed

The file db_seed.sql contains all statements that create the tables and views.
The loading of the CSVs is also stated in this file. It is achieved through the direct import of the CSV contents into the created tables.

In order to fetch all active products from the database, one may execute the following SQL statement:

    SELECT pd.*
    FROM products pd
    JOIN providers pv ON pv.id=pd.provider_id
    WHERE pv.is_active;

A portion of the results is presented below:
![image](docs/sqlresults1.png)


2. The backend service can is built in Python as a Flask web application.
SQLalchemy is used to interact with the database and ensure query parameter validation.

The backend code is found in:
    
    {repo_root}/backend

The file 'app.py' contains all the relevant system logic, including the handling of the specified API route (/products), as well as filtering, sorting and pagination features.

As it is such a simple application, all relevant logic is kept in a single file for ease of handling.

The route that returns responds with the list of products may be accessed via HTTP GET at:

    http://{base_uri}/products


3. The filtering is achieved throught the inclusion of query parameters in the request URI.
The route supports query parameters for filtering, sorting and paginating results. 
The query parameters should abide by the following formats:

    - filtering : {target field}={operator}:{value}
        ( e.g. /products?price=le:60 )

    the supported operators are: 
    'is_null'
    'is_not_null'
    'eq'
    'ne'
    'gt'
    'lt'
    'ge'
    'le'
    'like'
    'ilike'
    'not_ilike'
    'in'
    'not_in'
    'any'
    'not_any'


    - sorting : sort={direction}:{target field}
        ( e.g. /products?sort=asc:id )

    The supported directions are are: 
    'asc'
    'desc'


    - pagination : The supported parameters are page_size, page_number.
        ( e.g. /products?page_size=5&page_number=2 )


    ### Request results

    The response provided contains a json payload which follows the schema below:

    ```json
    [
        {
            "provider_logo_url":"https://www.comparaja.pt/s3/portugal/comparaja.pt/production/pt/images/providerLogos/meo.png",
            "mobile_phone_count":1,
            "p":4,
            "provider_name":"MEO",
            "price":29.99,
            "vertical_code":"BB",
            "internet_download_speed_in_mbs":100,
            "mobile_phone_data_in_gbps":5,
            "is_sponsored":true,
            "id":1,
            "tv_channels":120
        }
    ]
    ```


    A few request examples may be found below, using the cURL command.
    These requests are sent to the AWS hosted instance of this solution, and thus, responses should be available when executing:

    1. All products. The default pagination parameters will apply (10 elements per page):
    ```
    curl 'http://ec2-52-49-96-189.eu-west-1.compute.amazonaws.com:5000/products'
    ```

    2. Products with a price lower or equal to 60€:
    ```
    curl 'http://ec2-52-49-96-189.eu-west-1.compute.amazonaws.com:5000/products?price=le:60'
    ```

    3. Products from MEO. With pagination:
    ```
    curl 'http://ec2-52-49-96-189.eu-west-1.compute.amazonaws.com:5000/products?provider_name=eq:MEO&page_size=3&page_number=2'
    ```

    4. Sort products by ascending price, from NOWO:
    ```
    curl 'http://ec2-52-49-96-189.eu-west-1.compute.amazonaws.com:5000/products?provider_name=eq:NOWO&sort=asc:price'
    ```


# Build Front-end for Results Page
The Frontend application code may be found in:
    {repo_root}/frontend/app

It is written in Javascript and is a Vue.js application.
Build and launch details may be found in the [Build and launch] section of this document.
