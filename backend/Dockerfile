FROM alpine:3.22

RUN apk add --no-cache curl

RUN apk add --no-cache tesseract-ocr
RUN apk add --no-cache tesseract-ocr-data-rus


RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /code

COPY ./.python-version /code/.python-version

RUN uv python install $(cat .python-version)

COPY ./pyproject.toml .
COPY ./requirements.txt .
COPY ./uv.lock .

RUN uv sync 

COPY ./src ./src
COPY ./alembic ./alembic
COPY ./alembic.ini .
COPY ./.env.prod ./.env 

# CMD ["uv", "run", "python", "src/main.py"]
