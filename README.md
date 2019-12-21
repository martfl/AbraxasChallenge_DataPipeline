# Data Pipeline Abraxas - Histórico de unidades de metrobús

## Requirements

- Kubernetes (or minikube)
- kubectl
- Docker (docker-compose optional.)

## Architecture

The solution is made up of 3 containers.

- A GraphQL API on a Node.js server
- A persistent Redis server
- A Python script that fetches data from the https://datos.cdmx.gob.mx/explore/ API's and stores them on Redis.

Using Kubernetes for orchestration, it deploys both a Service resource and a Deployment resource for the GraphQL API and the Redis server.
And finally a CronJob resource for scheduling the Python script to run every hour.

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

The GraphQL playground is enabled at the ```/graphql```endpoint.

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

