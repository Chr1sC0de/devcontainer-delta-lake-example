# Use the official Ubuntu image as a parent image
FROM ubuntu:23.10

# Update the system and install required packages
RUN apt-get update && apt-get install -y \
    sudo curl build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev git libsasl2-dev

RUN sudo apt install default-jdk -y
RUN sudo apt install default-jre -y

# install scala
RUN apt-get install scala -y

# install spark

RUN wget https://dlcdn.apache.org/spark/spark-3.4.1/spark-3.4.1-bin-hadoop3.tgz
RUN tar -xvzf spark-3.4.1-bin-hadoop3.tgz
RUN mv spark-3.4.1-bin-hadoop3 /mnt/spark

# Install pyenv
RUN curl https://pyenv.run | bash

# Set environment variables for pyenv
ENV SPARK_HOME=/mnt/spark
ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

# Install Python versions and poetry on each version
RUN pyenv install 3.8 && \
    pyenv global 3.8 && \
    python -m pip install poetry && \
    pyenv rehash
RUN pyenv install 3.9 && \
    pyenv global 3.9 && \
    python -m pip install poetry && \
    pyenv rehash
RUN pyenv install 3.10 && \
    pyenv global 3.10 && \
    python -m pip install poetry && \
    pyenv rehash
RUN pyenv install 3.11 && \
    pyenv global 3.11 && \
    python -m pip install poetry && \
    pyenv rehash

# Set the global python version
RUN pyenv global 3.8

# # install pyspark
# RUN pip install pyspark -v

# # set the appropriate spark variables
# ENV PYSPARK_HADOOP_VERSION=3

RUN curl -sS https://starship.rs/install.sh | sh -s -- --yes
RUN echo 'eval "$(starship init bash)"' >> ~/.bashrc

# now copy the required jars
COPY jars/* $SPARK_HOME/jars
