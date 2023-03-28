# base

FROM public.ecr.aws/docker/library/python:3.8.12-slim-buster

COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.6.4 /lambda-adapter /opt/extensions/lambda-adapter

WORKDIR /workspace/api

COPY Pipfile .
COPY Pipfile.lock .

RUN pip install pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

COPY . .

CMD pipenv run python -m flask run --host=0.0.0.0 --port=8080