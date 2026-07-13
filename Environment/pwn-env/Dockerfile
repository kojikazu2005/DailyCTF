FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        python3 python3-pip python3-dev \
        git gdb gcc make \
        wget curl \
        vim \
        binutils \
        libc6-dbg \
        sudo \
    && rm -rf /var/lib/apt/lists/*

# pwndbg
RUN git clone https://github.com/pwndbg/pwndbg /opt/pwndbg && \
    cd /opt/pwndbg && \
    ./setup.sh

# pwntools
RUN pip3 install --upgrade pip && \
    pip3 install pwntools

WORKDIR /root
