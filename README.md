# Flask example

A basic Flask application example. You can build and test it locally as a typical Flask application.

Using AWS Lambda Adapter, You can package this web application into Docker image, push to ECR, and deploy to Lambda, ECS/EKS, or EC2.

The application can be deployed in an AWS account using the [Serverless Application Model](https://github.com/awslabs/serverless-application-model). The `template.yaml` file in the root folder contains the application definition.

The top level folder is a typical AWS SAM project. The `app` directory is a flask application with a [Dockerfile](app/Dockerfile).

```dockerfile
FROM public.ecr.aws/docker/library/python:3.8.12-slim-buster
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.6.4 /lambda-adapter /opt/extensions/lambda-adapter
WORKDIR /var/task
COPY app.py requirements.txt ./
RUN python3.8 -m pip install -r requirements.txt
CMD ["gunicorn", "-b=:8080", "-w=1", "app:app"]
```

Line 2 copies lambda adapter binary into /opt/extensions. This is the only change to run the Flask application on Lambda.

```dockerfile
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.6.4 /lambda-adapter /opt/extensions/lambda-adapter
```

## Pre-requisites

The following tools should be installed and configured.
* [AWS CLI](https://aws.amazon.com/cli/)
* [SAM CLI](https://github.com/awslabs/aws-sam-cli)
* [Python](https://www.python.org/)
    ** [Pyenv/Pipenv](https://medium.com/geekculture/setting-up-python-environment-in-macos-using-pyenv-and-pipenv-116293da8e72#:~:text=Pyenv%20is%20to%20manage%20Python,to%20install%20Pyenv%20and%20Pipenv.)
* [Docker](https://www.docker.com/products/docker-desktop)


## Deploy to Lambda
Navigate to the sample's folder and use the SAM CLI to build a container image
```shell
$ aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
$ sam build
```

This command compiles the application and prepares a deployment package in the `.aws-sam` sub-directory.

To deploy the application in your AWS account, you can use the SAM CLI's guided deployment process and follow the instructions on the screen

```shell
$ sam deploy --guided
```
Please take note of the container image name.
Once the deployment is completed, the SAM CLI will print out the stack's outputs, including the new application URL. You can use `curl` or a web browser to make a call to the URL

```shell
...
---------------------------------------------------------------------------------------------------------
OutputKey-Description                        OutputValue
---------------------------------------------------------------------------------------------------------
FlaskApi - URL for application            https://xxxxxxxxxx.execute-api.us-west-2.amazonaws.com/
---------------------------------------------------------------------------------------------------------
...

$ curl https://xxxxxxxxxx.execute-api.us-west-2.amazonaws.com/
```

## Run the docker locally

We can run the same docker image locally, so that we know it can be deployed to ECS Fargate and EKS EC2 without code changes.

```shell
$ docker run -d -p 8080:8080 {ECR Image}

```

Use curl to verify the docker container works.

```shell
$ curl localhost:8080/ 
```

## Running locally

SAM
```sh
Supports hot reloading (this runs all lambdas)
$ sam local start-api
```

Previously if you use the --debug flag, you will see the Event payload.
You could grab it pass it along to directly call Lambda. (runs only one lambda)
```sh
sam local invoke FlaskFunction -e apig-home.json
```

docker run (see above) (no hot reloading)

docker-compose up --build -d (hot reloading)

aws
[-] Requires to build and deploy on each change

## Useful CLI commands

```sh
Passthrough credentials to docker
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws

```
Build, deploy and beep
$ sam build && sam deploy && print \\a
```

```
Tail logs
$ sam logs --stack-name mktbot-serverless --tail
```

```
Build and Run Docker Image (no debugger)
$ docker-compose up --build -d
```

```
Debugging flask app
$ docker-compose run -p 8000:8000 svc1 python3 -m pdb app.py
```

````
Docker-compose build and up
$ cd app
$ docker-compose up --build -d
```

# Auth

We use "Implicit Grant OAuth" flow documented here: https://www.questrade.com/api/documentation/authorization?TSPD_101_R0=08005b7230ab2000a813ef08eeb33a9bf24b1b1e9cee0fd2bec84c626a9eb9c366751f8d0d47dc9108fbb0473f1430009a473cf802d3836dffe94b52ae48a8f00853d9cacbaaeeac611aba93d7d6a48ff7716a6e4794c6fee5a164944928e260

# Notes

[VS Code - Advanced Containers](https://code.visualstudio.com/remote/advancedcontainers/overview)