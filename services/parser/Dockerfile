FROM python:3.10

WORKDIR /code

RUN apt-get update 

RUN apt install pipx -y

RUN pipx install poetry -y

COPY ./pyproject.toml /code/pyproject.toml
COPY ./poetry.lock /code/poetry.lock

RUN poetry init
RUN poetry shell
RUN poetry install

COPY ./parser/ /code/

CMD [ "poetry", "run", "dev" ]



