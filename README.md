# social-network


## Requirements
    python3
    MySQL
    Docker

## Installation
1. Clone the repository: `git clone https://github.com/mathivanansoft/social-network.git`
2. Navigate to the project directory: `cd social-network`
3. Export `MYSQL_VOLUME=/storage-path` and `MYSQL_ROOT_PASSWORD=password`
4. Run `docker-compose up -d mysql` to run mysql container.
5. Copy .env.sample file to .env file and set value of the variables.
6. Run `docker-compose up -d social-network` to run social-network container.


## Usage
docker-compose automatically runs the migration and starts the sever in port 8000

## Steps
1. Signup
2. Login

## Authentication
Token based authentication is used. After login, token is added in each request headers in the form 

    Authorization: Token {{token}}