# python
FROM python:3.7-alpine

LABEL "MAINTAINER" = "Alexander Crosdale"

##################### Environment Vars ############################

# this is the project name
ARG SCRIPT

# this is the non root user
ARG USER

# this is the files location
ARG LOCATION

# this is the path of the project
ARG PROJECT_DIR

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

# the script to run in the entrypoint
ENV SCRIPT_NAME=$SCRIPT

##################### System  ############################

COPY requirements.txt /tmp/

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev libc-dev linux-headers musl-dev \
    && apk add postgresql-dev \
    && apk add pcre-dev \
    && pip install --upgrade pip \
    && pip install -r /tmp/requirements.txt \
    && apk del build-deps

##################### User  ############################

# add non root user. NEVER RUN CODE AS ROOT
RUN adduser -h $LOCATION/$USER -D -s /bin/sh $USER

# change working dir to non root user dir
WORKDIR $LOCATION/$USER

# make the /location/user/sites folder to store project
# change owner of /location/user to user1
RUN mkdir -p $PROJECT_DIR \
    && chown -R $USER:$USER .

# set USER to be use for any RUN, CMD and ENTRYPOINT instructions that follow
USER $USER

##################### Project  ############################

# copy current project into docker sites/project_name
COPY --chown=$USER:$USER . $PROJECT_DIR

# changes working project dir
WORKDIR $PROJECT_DIR

# run start up script in
ENTRYPOINT scripts/$SCRIPT_NAME

