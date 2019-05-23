FROM python:3.7-slim

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100
ENV POETRY_VERSION=0.12.16
ENV PATH=$PATH:/usr/src/app

ENV BUILD_DEPS git gcc g++ cmake make

ARG ENVIRONMENT=prod

COPY pyproject.toml poetry.lock ./

COPY . .

RUN set -ex ; \
    if [ $ENVIRONMENT = "local" ] || [ $ENVIRONMENT = "test" ]  ; then \
      POETRY_EXTRA="-E carto -E postgres -E redis" ; \
    else \
      POETRY_EXTRA="-E carto -E postgres -E redis --no-dev" ; \
    fi ; \
    apt-get update ; \
    apt-get install -y --no-install-recommends \
      $BUILD_DEPS ; \
    pip install "poetry==$POETRY_VERSION" ; \
    # poetry config settings.virtualenvs.create false ; \
    poetry completions bash > /etc/bash_completion.d/poetry.bash-completion ; \
    poetry install --no-interaction --no-ansi $POETRY_EXTRA ; \
    apt-get remove -y --purge $BUILD_DEPS ; \
    apt-get autoremove -y ; \
    apt-get clean -y ; \
    rm -rf /var/lib/apt/lists/*


CMD ["python", "-m", "glutemulo.gluto"]
