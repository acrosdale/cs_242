# python
FROM coady/pylucene

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

RUN pip install --upgrade pip \
    && pip install -r /tmp/requirements.txt

##################### User  ############################

# change working dir to non root user dir
WORKDIR $LOCATION/$USER

RUN mkdir -p $PROJECT_DIR

##################### Project  ############################

# copy current project into docker sites/project_name
COPY . $PROJECT_DIR

# changes working project dir
WORKDIR $PROJECT_DIR

# run start up script in
ENTRYPOINT scripts/$SCRIPT_NAME
