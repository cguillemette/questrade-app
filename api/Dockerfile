FROM python:3.9.18-bullseye

WORKDIR /workspace/api

COPY Pipfile .
COPY Pipfile.lock .

RUN pip install pipenv && pipenv install --system --deploy

COPY . .

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]