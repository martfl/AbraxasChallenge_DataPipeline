# Data Pipeline Abraxas - Histórico de unidades de metrobús

## Requirements

- Kubernetes (or minikube)
- kubectl
- Docker (docker-compose optional.)

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


### GraphQL API

Several queries are available:
- listUnits
-

