FROM python:3.10

WORKDIR /parser

RUN apt-get update 

# RUN python3 -m pip install pipx
# RUN python3 -m userpath append ~/.local/bin


# RUN pipx install poetry

# RUN pipx ensurepath
# RUN export PATH=$PATH:/root/.local/bin

# RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python


RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="$HOME/.local/bin"
COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock

COPY . .

RUN poetry init
RUN poetry shell
RUN poetry install


CMD [ "poetry", "run", "pytest" ]



