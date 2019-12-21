# Data Pipeline Abraxas - Histórico de unidades de metrobús

## Requirements

- Kubernetes (or minikube)
- kubectl
- Docker (docker-compose optional.)

## Helpers

- Re-using local Docker daemon with minikube: `eval $(minikube docker-env)` (run it once before Docker build)
- On OSX: To base64: `pbpaste | base64 | pbcopy` and From base64: `pbcopy | base64 --decode`
- `minikube start` and `minikube stop`

## Tasks

### 1. Build Docker image

Re-using local Docker daemon with minikube:

```sh
eval $(minikube docker-env)
```

Building Docker image:

```sh
cd src/gateway
docker build -t my-co/gateway:v1 .
