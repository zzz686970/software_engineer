## check namespace

```sh
kubectl get namespace
## defaul  创建时不指定资源
## kube-system 自己创建的资源
```

## check pods
```sh
kubectl get pods
```

## check service
```sh
kubectl get services
```

## check replica
```sh
kubectl get deployments
## scale replica
kubectl scale deployments/kubernetes-bootcamp --replica=3
```

## check cluster information
```sh
kubectl cluster-info

```

## create app
```sh
## file way
# kubectl apply -f nginx.yml
kubectl run kubernetes-bootcamp --image=docker.io/jocatalin/kubernetes-bootcamp:v1 --port=8080
kubectl expose deployments/kubernetes-bootcamp --type="NodePort" --port 8080
kubectl get services
## check which port is exposed to
```

## scale up/down
```sh
kubectl get deployments
kubectl scale deployments/kubernetes-bootcamp --replica=3

```

## upgrade image
```sh
kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=jocatalin/kubernetes-bootcamp:v2


```

## rollout
```sh
kubectl rollout undo deployments/kubernetes-bootcamp
```