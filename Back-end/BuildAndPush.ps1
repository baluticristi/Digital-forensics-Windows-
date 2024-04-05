# Build and push the licenses component
docker build -t mwkido/licenta_cristian:latest -f .\docker_licenta .
docker push mwkido/licenta_cristian:latest

# Build and push the report generator component
docker build -t mwkido/report_generator:latest -f .\docker_report .
docker push mwkido/report_generator:latest

# Build and push the analyzer component
docker build -t mwkido/analyzer:latest -f .\docker_analyzer .
docker push mwkido/analyzer:latest

#delete all images
kubectl delete deployment --all
kubectl delete service --all
kubectl delete pod --all

#deploy all images
kubectl apply -f .\main_server.yaml
kubectl apply -f .\report_deployment.yaml
kubectl apply -f .\analyzer.yaml