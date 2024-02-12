# questrade-app

Simple way to monitor your investments through Questrade.

**Why?**

I understand the importance of having a tool that provides a minimalist view of your assets while ensuring quick updates. That's why I created this app – keeping an eye on your stocks without any unnecessary clutter.

**Features**

- Adds support for implicit grant oauth against the Questrade API [link](https://www.questrade.com/api/documentation/authorization)
- Includes a clean boilerplate that could serve building other apps
- Both front-end and back-end use docker with hot reloading
- It is lightweight to setup and can be deployed if needed to any container based provider

**Demo**

<img alt="demo" src="doc/screenshot.webp" width="550" />

## Stack

[![](https://mermaid.ink/img/pako:eNptUU1TgzAQ_SuZPdUZCkmgCXBwbK2d8eCMXyfFQ0pCYQqECUGtbf-7odWDM24uydt9-_J295BrqSCFotYfeSmMRc_LrEUu5q8ro1s7Va1EU_SoRG7RFUKltV0aBIRyH7tDUoYxeUPT6eUBHdBishD59oezqkW_dZz_KPTirLL4ZV5PHgbVWyOkQvP7W5cGDxplGlFJ97_9WJ6BLVWjMkjdVQqzzSBrj65ODFY_7docUmsG5cHQSWHVshIbI5q_4I2srDaQFqLuHVhrJ-iee7C7bhzEpuqt65jrtqg2Iz6Y2sGjh96ZGNP-prLlsPZz3QR9Jceple8JCxhlsaChYjwUszCU-ZokcUEjUkiOCRVwPHrQiXbs-gkpJZHPo4TjJIkJiRn1YAcpwdynmPNoFrKIJ4w5zpfWzgX2Z_gccZTEYRhyD9TJzd15h6dVnhReToTR9vEbT6GP3w?type=png)](https://mermaid.live/edit#pako:eNptUU1TgzAQ_SuZPdUZCkmgCXBwbK2d8eCMXyfFQ0pCYQqECUGtbf-7odWDM24uydt9-_J295BrqSCFotYfeSmMRc_LrEUu5q8ro1s7Va1EU_SoRG7RFUKltV0aBIRyH7tDUoYxeUPT6eUBHdBishD59oezqkW_dZz_KPTirLL4ZV5PHgbVWyOkQvP7W5cGDxplGlFJ97_9WJ6BLVWjMkjdVQqzzSBrj65ODFY_7docUmsG5cHQSWHVshIbI5q_4I2srDaQFqLuHVhrJ-iee7C7bhzEpuqt65jrtqg2Iz6Y2sGjh96ZGNP-prLlsPZz3QR9Jceple8JCxhlsaChYjwUszCU-ZokcUEjUkiOCRVwPHrQiXbs-gkpJZHPo4TjJIkJiRn1YAcpwdynmPNoFrKIJ4w5zpfWzgX2Z_gccZTEYRhyD9TJzd15h6dVnhReToTR9vEbT6GP3w)

## Pre-requisites

To run locally, you minimally need:

- [Docker](https://www.docker.com/products/docker-desktop).
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
    https://login.questrade.com/oauth2/authorize?client_id=<QUESTRADE-CLIENT-ID>&response_type=token&redirect_uri=<NGROK-URL>
    ```

  - Go through Questrade authorization, then it will redirect to locally running app

## Running locally

Ensure you have Docker running then call docker-compose:

```sh
docker-compose up --build -d 
```

Browse to <http://127.0.0.1:6001>.
