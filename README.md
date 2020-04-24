# Project Details

Overview:
1. Implemented dockerize microservices with version tagging running on Python Flask.
2. Deployed the solution on a local container orchestrator(Minikube). We can deploy the same on Production as well with pod per node define if we want to run a pod on a single node. Either KOPS or Kubeadm, we can create a cluster on cloud provider using KOPS or ON-Premis using Kubeadm. I did not have enough resources so I am using minikube for this project. The same can be deployed on production as well.
3. Used helm manager to install Python Flask App and upgrading the same. 

> This is a project to build Flask app using python flask framework and deploy it on Kubernetes cluster using minikube with version tagging below is the output.


# Used "helm" to deploy app and upgraded the same without down time. We can use multiple ways of deployment i.e. Blue/Green or Rollout strategy. I am using Blue/green strategy here to deploy app which is working 100% wihtout downtime. 

Let's begin install app using helm which is running version 1. As using minikube once application is using Loadbalance to send traffic and exposed on NodePort (32729) but on any cloud platform it will be exposing 80 port.

Charts is only file which describe about the application. So we are not going to change it at all.

Clone the repo and go to deployment/my-app-riskident folder. Edit the tags from value.yaml and then run below command to install your v1 app.
```
$ helm install --name my-app my-app-riskident
NAME:   my-app
LAST DEPLOYED: Fri Jun 28 16:29:15 2019
NAMESPACE: default
STATUS: DEPLOYED

RESOURCES:
==> v1/Deployment
NAME                     READY  UP-TO-DATE  AVAILABLE  AGE
my-app-my-app-riskident  0/1    1           0          0s

==> v1/Pod(related)
NAME                                     READY  STATUS             RESTARTS  AGE
my-app-my-app-riskident-cbd844855-mnmf4  0/1    ContainerCreating  0         0s

==> v1/Service
NAME                     TYPE          CLUSTER-IP     EXTERNAL-IP  PORT(S)       AGE
my-app-my-app-riskident  LoadBalancer  10.107.81.235  <pending>    80:32729/TCP  0s


NOTES:
1. Get the application URL by running these commands:
     NOTE: It may take a few minutes for the LoadBalancer IP to be available.
           You can watch the status of by running 'kubectl get --namespace default svc -w my-app-my-app-riskident'
  export SERVICE_IP=$(kubectl get svc --namespace default my-app-my-app-riskident -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
  echo http://$SERVICE_IP:80

```
![alt text](https://github.com/manukoli1986/riskident/blob/master/images/svc.jpg)
![alt text](https://github.com/manukoli1986/riskident/blob/master/images/deployment.jpg)
![alt text](https://github.com/manukoli1986/riskident/blob/master/images/v1.jpg)

Then check via curl command 

![alt text](https://github.com/manukoli1986/riskident/blob/master/images/curl-v1.jpg)

Now let's upgrade app with version 2. Go to deployment/my-app-riskident folder again and update tag value from v1 to v2 in value.yaml file then run below command.
```
$ helm upgrade my-app my-app-riskident
Release "my-app" has been upgraded.
LAST DEPLOYED: Fri Jun 28 17:39:49 2019
NAMESPACE: default
STATUS: DEPLOYED

RESOURCES:
==> v1/Deployment
NAME                     READY  UP-TO-DATE  AVAILABLE  AGE
my-app-my-app-riskident  1/1    1           1          50m

==> v1/Pod(related)
NAME                                      READY  STATUS             RESTARTS  AGE
my-app-my-app-riskident-6594849b98-79bbq  0/1    ContainerCreating  0         0s
my-app-my-app-riskident-cbd844855-tnktc   1/1    Running            0         29m

==> v1/Service
NAME                     TYPE          CLUSTER-IP      EXTERNAL-IP  PORT(S)       AGE
my-app-my-app-riskident  LoadBalancer  10.105.235.119  <pending>    80:32162/TCP  50m


NOTES:
1. Get the application URL by running these commands:
     NOTE: It may take a few minutes for the LoadBalancer IP to be available.
           You can watch the status of by running 'kubectl get --namespace default svc -w my-app-my-app-riskident'
  export SERVICE_IP=$(kubectl get svc --namespace default my-app-my-app-riskident -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
  echo http://$SERVICE_IP:80

```
![alt text](https://github.com/manukoli1986/riskident/blob/master/images/v2.jpg) 

Curl output

![alt text](https://github.com/manukoli1986/riskident/blob/master/images/upgrade.jpg)

Everything is workng file

```
Administrator@DESKTOP-OPO4JVT MINGW64 ~/Desktop/vagrant/riskident/deployment
$ helm history my-app
REVISION        UPDATED                         STATUS          CHART                   DESCRIPTION
1               Fri Jun 28 16:49:25 2019        SUPERSEDED      my-app-riskident-1.0.0  Install complete
2               Fri Jun 28 17:09:01 2019        DEPLOYED        my-app-riskident-2.0.0  Upgrade complete

Administrator@DESKTOP-OPO4JVT MINGW64 ~/Desktop/vagrant/riskident/deployment
$ helm rollback my-app 1
Rollback was a success.

Administrator@DESKTOP-OPO4JVT MINGW64 ~/Desktop/vagrant/riskident/deployment
$ helm history my-app
REVISION        UPDATED                         STATUS          CHART                   DESCRIPTION
1               Fri Jun 28 16:49:25 2019        SUPERSEDED      my-app-riskident-1.0.0  Install complete
2               Fri Jun 28 17:09:01 2019        SUPERSEDED      my-app-riskident-2.0.0  Upgrade complete
3               Fri Jun 28 17:10:25 2019        DEPLOYED        my-app-riskident-1.0.0  Rollback to 1

```
![alt text](https://github.com/manukoli1986/riskident/blob/master/images/rollback.jpg)



### Prerequisites
You must have setup minikube and helm on your local. Once it is done then start minikube and check below commands to verfiy kubernetes has been setup on local. 

```
$ minikube.exe start
* minikube v1.1.1 on windows (amd64)
* Tip: Use 'minikube start -p <name>' to create a new cluster, or 'minikube delete' to delete this one.
* Restarting existing virtualbox VM for "minikube" ...
* Waiting for SSH access ...
* Configuring environment for Kubernetes v1.14.3 on Docker 18.06.3-ce
* Relaunching Kubernetes v1.14.3 using kubeadm ...
* Verifying: apiserver proxy etcd scheduler controller dns
* Done! kubectl is now configured to use "minikube"
```

# TASK 1

### This project consist of two steps:
1. Created two dockerized microservices with version tagging using alpine python as base image and used flask framework to provide Restapi "/image" endpoints.

a. Flasp-app1 & Dockerfile & Build images with version

```
$ cat flask-app1/app.py
#!/usr/bin/env python3
#Importing module of flask framework to run app on web
from flask import Flask, render_template
import datetime


# Create the application.
app = Flask(__name__)


# Displays the index page accessible at '/'
@app.route("/")
def index():
    return "This is first deployment. Kindly use /image uri to get output"


# Displays the image and text page accessible at '/image' and below is function.
@app.route("/image")
def image():
    print ("Hello World !!! - v1")
    return render_template('index.html')

# This code is finish and ready to server on port 80
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)


$ docker build -t docker.io/manukoli1986/flask-app-image:v1 .
Sending build context to Docker daemon 16.38 kB
Step 1/7 : FROM frolvlad/alpine-python3
 ---> 04e335690445
Step 2/7 : MAINTAINER "Mayank Koli"
 ---> Using cache
 ---> cfc2fc217984
Step 3/7 : EXPOSE 80
 ---> Running in 7a38fe62f871
 ---> b3c2a9bb9dad
Removing intermediate container 7a38fe62f871
Step 4/7 : WORKDIR /usr/src/app
 ---> 6cc09ec5145f
Removing intermediate container e5594486956b
Step 5/7 : COPY . ./
 ---> e44956ccdae3
Removing intermediate container 4dd57dea8ea6
Step 6/7 : RUN pip3 install --no-cache-dir -r requirements.txt
 ---> Running in 2a8fd779ba0a


$ docker push docker.io/manukoli1986/flask-app-image:v1
The push refers to a repository [docker.io/manukoli1986/flask-app-image]
6d9da613a206: Pushed
548b586db206: Pushed
8ae296b0e008: Pushed
508b76350c79: Mounted from manukoli1986/flask-app2
a464c54f93a9: Mounted from manukoli1986/flask-app2
v1: digest: sha256:401865967b953c9b4a63d4cf7a8c50b3cbc3d98a3470940189f75f7422dd6c51 size: 1366
```
b. Flasp-app2 & Dockerfile & Build images with version

```
#!/usr/bin/env python3
#Importing module of flask framework to run app on web
from flask import Flask, render_template
import datetime


# Create the application.
app = Flask(__name__)


# Displays the index page accessible at '/'
@app.route("/")
def index():
    return "This is first deployment. Kindly use /image uri to get output"


# Displays the image and text page accessible at '/image' and below is function.
@app.route("/image")
def image():
    print ("Hello World !!! - v2")
    return render_template('index.html')

# This code is finish and ready to server on port 80
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)


$ docker build -t docker.io/manukoli1986/flask-app-image:v2 .
Sending build context to Docker daemon 16.38 kB
Step 1/7 : FROM frolvlad/alpine-python3
 ---> 04e335690445
Step 2/7 : MAINTAINER "Mayank Koli"
 ---> Using cache
 ---> cfc2fc217984
Step 3/7 : EXPOSE 80
 ---> Running in 7a38fe62f871
 ---> b3c2a9bb9dad
Removing intermediate container 7a38fe62f871
Step 4/7 : WORKDIR /usr/src/app
 ---> 6cc09ec5145f
Removing intermediate container e5594486956b
Step 5/7 : COPY . ./
 ---> e44956ccdae3
Removing intermediate container 4dd57dea8ea6
Step 6/7 : RUN pip3 install --no-cache-dir -r requirements.txt
 ---> Running in 2a8fd779ba0a


$ docker push docker.io/manukoli1986/flask-app-image:v2
The push refers to a repository [docker.io/manukoli1986/flask-app-image]
6d9da613a206: Pushed
548b586db206: Pushed
8ae296b0e008: Pushed
508b76350c79: Mounted from manukoli1986/flask-app2
a464c54f93a9: Mounted from manukoli1986/flask-app2
v1: digest: sha256:401865967b953c9b4a63d4cf7a8c50b3cbc3d98a3470940189f75f7422dd6c51 size: 1367
```

# Helm Activity

How I create this chart and can be upload to remote repo path. 

```
$ helm create my-app-riskident

$ helm ls
NAME    REVISION        UPDATED                         STATUS          CHART                   APP VERSION     NAMESPACE
my-app  4               Fri Jun 28 17:39:49 2019        DEPLOYED        my-app-riskident-2.0.0  1.0             default

$ helm package my-app-riskident
Successfully packaged chart and saved it to: C:\Users\Administrator\Desktop\vagrant\riskident\deployment\my-app-riskident-2.0.0.tgz


$ helm search my-app-riskident
NAME                    CHART VERSION   APP VERSION     DESCRIPTION
local/my-app-riskident  2.0.0           1.0             Chart for deploying version 2 flask application
```

I have updated below files to run application using helm.
```
$ cat Chart.yaml
apiVersion: v1
appVersion: "1.0"
description: Chart for deploying version 2 flask application
name: my-app-riskident
version: 1.0.0

$ cat values.yaml
replicaCount: 1
image:
  repository: docker.io/manukoli1986/flask-app-image
  tag: v1
  pullPolicy: IfNotPresent
service:
  type: LoadBalancer
  port: 80
  targetPort: 80
resources:
   limits:
     cpu: 100m
     memory: 128Mi
```

Once application is UP and new updated dockerized image is pushed to repository, then we will update chart.yaml and values.yml to version 2 and we are ready to upgrade app from version 1 to version 2 without downtime

# Kubernetes Deployment files 
```
$ cat deployment1.yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: flask-app-image-v1
spec:
  replicas: 1
  template:
    metadata:
      labels:
        name: flask-app-image
        version: "v1"
        slot: blue

    spec:
      containers:
        - name: flask-app-image
          image: docker.io/manukoli1986/flask-app-image:v1
          ports:
            - name: http
              containerPort: 80
          readinessProbe:
            tcpSocket:
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            tcpSocket:
              port: 80
            initialDelaySeconds: 10
            periodSeconds: 10
```

```
$ cat deployment2.yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: flask-app-image-v2
spec:
  replicas: 1
  template:
    metadata:
      labels:
        name: flask-app-image
        version: "v2"
    spec:
      containers:
        - name: flask-app-image
          image: docker.io/manukoli1986/flask-app-image:v2
          ports:
            - name: http
              containerPort: 80
          readinessProbe:
            tcpSocket:
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            tcpSocket:
              port: 80
            initialDelaySeconds: 10
            periodSeconds: 10
```


# Issue 

1. Used Livness and Readiness probes to solve my problem as when I was using kubectl blue/green deployment it was working fine as I just had to update service object to route the traffic. But using helm it will not wait for new version release and release traffic to it even though it is not active yet. So by using Livness and Readiness new version will only accept traffic once app is completely deployed and up.
2. Duing build flask app, I found rendering template was easy option to show image with text.


Prepared By: Mayank Koli
Kindly update me if there is any issue during deployment.  
