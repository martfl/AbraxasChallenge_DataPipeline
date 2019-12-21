# Data Pipeline Abraxas - Histórico de unidades de metrobús

## Requirements

- Kubernetes (or minikube)
- kubectl
- Docker (docker-compose optional.)

## Architecture

The solution is made up of 3 containers.

- A GraphQL API on a Node.js server
- A persistent Redis server
- A Python script that fetches data from the https://datos.cdmx.gob.mx/explore/ API's, handles data transformations, and stores them on Redis.

Alcaldías are calculated using the following API: https://datos.cdmx.gob.mx/explore/dataset/ubicacion-acceso-gratuito-internet-wifi-c5. 
Results are cached in Redis to lower number of requests.  

Using Kubernetes for orchestration, it deploys both a Service resource and a Deployment resource for the GraphQL API and the Redis server.
And finally a CronJob resource for scheduling the Python script to run every hour.

## Data Model

Main data model was accomplished using Redis as a time-series db.

A sorted set is used for storing a vehicle's location history. Its rank is calculated using the timestamp in miliseconds.
Keys are stored in Redis in the following format: ```vehicle:<VEHICLE_ID>```

The GraphQL API is written in such way that any request is treated as atomic for Redis. i.e. A single command is issued to the server.

For Alcaldías and Units available a simple set is used.


## Deploying

### 0. Run a Kubernetes cluster

```sh
minikube start
```

### 1. Build Docker images locally (optional, but recommended)

Re-using local Docker daemon with minikube:

```sh
eval $(minikube docker-env)
```

Building Docker images:

```sh
docker build -t mmartfl/api:v1 api
docker build -t mmartfl/redis-server:v1 redis-server
docker build -t mmarfl/backend:v1 backend
```

### 2. Deploy Services using ```kubectl```

```sh
kubectl apply -f deployments
```

It should output the Deployments and Services created
```sh
▶ kubectl apply -f deployments
deployment.apps/metrobus-api created
service/metrobus-api-service created
cronjob.batch/backend created
deployment.apps/redis-master created
service/redis-master created
```

Kubernetes dynamically asigns an IP to each service, to get the url for our API service:

```sh
minikube service metrobus-api-service --url
```

The GraphQL playground is enabled at the ```/graphql```endpoint. Test data is provided.

### GraphQL API

#### Schema

The following schema is used for representing the position at a certain time for a single vehicle.

```
type Unit {
coords: [String]
alcaldia: String!
date_updated: String
}
```

Several queries are available:
- listUnits:[Int]
- unitHistory(id:<VEHICLE_ID>):[Unit]
- listAlcaldias:[String]
- unitsByAlcaldia(alcaldias:<ALCALDIA_NAME>)[String]

