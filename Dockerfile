FROM openup/docker-python-nodejs:python3.7-nodejs12

ENV PYTHONUNBUFFERED 1
ENV NODE_ENV production

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential python3.7-dev \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # git for codecov file listing
  && apt-get install -y git \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN pip install -U poetry

# Copy, then install requirements before copying rest for a requirements cache layer.
COPY pyproject.toml poetry.lock /tmp/
RUN cd /tmp \
    && poetry env use system \
    && poetry install

COPY . /app

ARG USER_ID=1001
ARG GROUP_ID=1001

RUN addgroup --gid $GROUP_ID --system django \
    && adduser --system --uid $USER_ID --gid $GROUP_ID django
RUN chown -R django:django /app
USER django

WORKDIR /app

RUN yarn && yarn build

EXPOSE 5000
CMD /app/bin/start.sh
