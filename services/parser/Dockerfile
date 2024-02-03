FROM python:3.10

WORKDIR /code

RUN apt-get update 

RUN python3 -m pip install pipx
RUN python3 -m userpath append ~/.local/bin

RUN pipx install poetry


COPY ./pyproject.toml /code/pyproject.toml
COPY ./poetry.lock /code/poetry.lock

COPY ./parser/ /code/

RUN poetry init
RUN poetry shell
RUN poetry install


CMD [ "poetry", "run", "dev" ]



