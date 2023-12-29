# base

FROM public.ecr.aws/docker/library/python:3.8.12-slim-buster

COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.7.1 /lambda-adapter /opt/extensions/lambda-adapter

WORKDIR /workspace/api

COPY Pipfile .
COPY Pipfile.lock .

RUN pip install pipenv && pipenv install --system --deploy

COPY . .

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]