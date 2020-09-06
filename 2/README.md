# Instalation instructions

### Prepare environment
create new namespace:
1. kubectl create namespace ___YOUR NAMESPACE___
2. Change namespace: kubectl config set-context --current --namespace=___YOUR NAMESPACE___

### Run HELM
helm install ___YOUR RELEASENAME___ ./second-ls-chart


### Run postman collection
install newman: sudo npm install -g newman
```
newman run Second_lesson.postman_collection.json
```
