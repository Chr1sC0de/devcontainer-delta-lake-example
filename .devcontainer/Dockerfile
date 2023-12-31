# ---------------------------------------------------------------------------- #
#                                build pyenv                                   #
# ---------------------------------------------------------------------------- #

FROM ubuntu:23.10 as builder

ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

RUN apt-get update \
    && apt-get install -y \
        git \
        wget \
        curl \
        sudo \
        build-essential \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        llvm \
        libncurses5-dev \
        libncursesw5-dev \
        xz-utils \
        tk-dev \
        libffi-dev \
        liblzma-dev \
        libsasl2-dev

RUN curl https://pyenv.run | bash \
    && pyenv install 3.8  && pyenv global 3.8  && pip install poetry && pyenv rehash \
    && pyenv install 3.9  && pyenv global 3.9  && pip install poetry && pyenv rehash \
    && pyenv install 3.10 && pyenv global 3.10 && pip install poetry && pyenv rehash \
    && pyenv install 3.11 && pyenv global 3.11 && pip install poetry && pyenv rehash

# ---------------------------------------------------------------------------- #
#                                     main                                     #
# ---------------------------------------------------------------------------- #

FROM ubuntu:23.10

ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
ENV SPARK_HOME=/mnt/spark

COPY --from=builder /root/.pyenv /root/.pyenv

RUN apt-get update && apt-get install --no-install-recommends -y \
        git \
        wget \
        curl \
        sudo \
        default-jdk \
        default-jre \
        scala \
        build-essential \
        libsasl2-dev \
        python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN wget https://dlcdn.apache.org/spark/spark-3.4.1/spark-3.4.1-bin-hadoop3.tgz \
    && tar -xvzf spark-3.4.1-bin-hadoop3.tgz \
    && mv spark-3.4.1-bin-hadoop3 /mnt/spark \
    && rm spark-3.4.1-bin-hadoop3.tgz

RUN curl -sS https://starship.rs/install.sh | sh -s -- --yes && \
    echo 'eval "$(starship init bash)"' >> ~/.bashrc

# this is to fix potential compilation issues when installing and compiling
# packages on python 3.11
RUN cp $PYENV_ROOT/versions/3.8.*/include/python3.8/longintrepr.h \
        $PYENV_ROOT/versions/3.11.*/include/python3.11

ENV HOME /root

COPY jars/* /root/.ivy2/jars/

WORKDIR /root/.ivy2/jars/

RUN for file in *; do \
        newname=$(echo "$file" | cut -d'_' -f2-); \
        if [ "$newname" != "" ]; then \
            mv "$file" "$newname"; \
        fi; \
    done
