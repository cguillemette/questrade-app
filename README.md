# questrade-ui

Simple UI that interops with the Questrade API.

Why?

Created this app because I felt the process of going on Questrade and authenticating to watch my assets was slow. As each time, I was required to 2FA. Sure, I could turn it off but I also felt there was too much information for what I needed. Therefore I built this app to display my accounts in a minimalist way grouping group all my accounts by stock versus per account.

Features

In addition to adding support for implicit grant oauth, it includes a clean boilerplate that could serve building other apps.

- Both front-end and back-end use docker with hot reloading for both frontend / backend
- It is lightweight to setup and can be deployed if needed to any AWS container based service

## Structure

[![](https://mermaid.ink/img/pako:eNpVUctugzAQ_BVrT6kEBDA2j0OlpGmkHir1dWrpwbHNQwGMjGmbpvx7Deml9sU7s7Oj8Z6BKyEhg6JRn7xi2qCXXd4hezZve60648pOIBc9ScbNO3Ld6x_0g7arLePHP2rfsOF4dRFt5w50s3oc5WA0ExJtHu4sBw60UresFtbrPPfmYCrZyhwy-xRMH3PIu8n2sdGo51PHITN6lA6MvWBG7mpWatb-B29FbZSGrGDNYMFGWUNbnsGc-jlUWQ_GTuSqK-pyxkfdWLgyph-y9XqmvbI21XjwuGrXQy3mH6g-UrqmIU1YiCWNMSMYC34I0qQIo6AQsR-EDKbJgZ5189QvyMIo9dIoSRNMInsTnzhwgiwg1CPYD0lIYoJpQGKr-lbK5vA9mliTyE9jmvokCbEDcslzf9nIspjF43URzMGnX2gihBE?type=png)](https://mermaid.live/edit#pako:eNpVUctugzAQ_BVrT6kEBDA2j0OlpGmkHir1dWrpwbHNQwGMjGmbpvx7Deml9sU7s7Oj8Z6BKyEhg6JRn7xi2qCXXd4hezZve60648pOIBc9ScbNO3Ld6x_0g7arLePHP2rfsOF4dRFt5w50s3oc5WA0ExJtHu4sBw60UresFtbrPPfmYCrZyhwy-xRMH3PIu8n2sdGo51PHITN6lA6MvWBG7mpWatb-B29FbZSGrGDNYMFGWUNbnsGc-jlUWQ_GTuSqK-pyxkfdWLgyph-y9XqmvbI21XjwuGrXQy3mH6g-UrqmIU1YiCWNMSMYC34I0qQIo6AQsR-EDKbJgZ5189QvyMIo9dIoSRNMInsTnzhwgiwg1CPYD0lIYoJpQGKr-lbK5vA9mliTyE9jmvokCbEDcslzf9nIspjF43URzMGnX2gihBE)

Frontend: React using plain javavscript - <http://127.0.0.1:6001>
Backend: Python using Flask

Both are built using a dockerfile that can be ran locally and deployed to cloud of choice.

For the sake of simplicity, top level folder has the typical AWS SAM project files to ease deployment on AWS. That can be changed since it doesn't depend on any AWS services, useful if you intend to deploy on another cloud provider.

## Pre-requisites

If you use VS Code and Dev Containers extension, you have nothing to install.

To run locally, you minimally need:

- [Docker](https://www.docker.com/products/docker-desktop).
- [AWS CLI](https://aws.amazon.com/cli/)
  - From AWS console, create an access key and use `aws configure` to setup authentication
  - Then login to AWS elastic container registry:

  ```sh
  aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
  ```

- [Questrade App Hub](https://www.questrade.com/partner-centre/app-hub)
  - This repo depends on the Questrade API, you will need to setup your own app from their site and ensure you provide an https callback.
  - To do so, you can use ngrok after fetching your authorization token from their site:

    ```sh
    brew install ngrok/ngrok/ngrok
    ngrok config add-authtoken <INSERT-YOUR-AUTH-TOKEN>
    ngrok http 6001
    ```

  - In api/.env, update CORS_ORIGIN_QUESTRADE_CALLBACK with ngrok generated https URL
  - From, your Questrade App, copy/paste your consumer key and redirect uri (prior ngrok generated endpoint) to fill in the following URL:

    ```sh
    https://login.questrade.com/oauth2/authorize?client_id=<client id>&response_type=token&redirect_uri=<url>
    ```

  - Go through Questrade authorization, then it will redirect to locally running app

## Running locally

Ensure you have Docker running then call docker-compose:

```sh
docker-compose up --build -d 
```

Browse to <http://127.0.0.1:6001>.

## Code changes locally

If you use VS Code, no need to install locally node/python or any dependencies.
You can simply install VS Code extension [Dev Containers](https://code.visualstudio.com/remote/advancedcontainers/overview).

Use `Ctrl + Shift + P`, then select `Dev Containers: Attach to running containers..`.
Select either the ui (front end) and/or api ().

It will spawn a new window, any changes will be reflected.

## Deployment

Though setup for AWS SAM deployment, as a docker image is built it could be easily adapted to deploy to other containerization services: ECS, Fargate and EC2 without code changes.

For AWS SAM, you will find up to date deployment instructions [here](https://github.com/awslabs/aws-lambda-web-adapter/tree/main/examples/flask#deploy-to-lambda)

# Auth

We use "Implicit Grant OAuth" flow documented here: <https://www.questrade.com/api/documentation/authorization?TSPD_101_R0=08005b7230ab2000a813ef08eeb33a9bf24b1b1e9cee0fd2bec84c626a9eb9c366751f8d0d47dc9108fbb0473f1430009a473cf802d3836dffe94b52ae48a8f00853d9cacbaaeeac611aba93d7d6a48ff7716a6e4794c6fee5a164944928e260>
