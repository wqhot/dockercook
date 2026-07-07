FROM ubuntu:18.04

# Install required dependencies
RUN /bin/sh -c export DEBIAN_FRONTEND=noninteractive && \
    apt update -y && \
    apt install -y wget && \
    apt install -y libssl-dev && \
    apt install -y pkg-config && \
    apt install -y libssl-dev && \
    apt install -y libcrypto++-dev && \
    apt install -y build-essential && \
    apt install -y zlib1g-dev && \
    apt install -y ca-certificates

RUN apt install -y cmake && \
    apt install -y git
RUN apt install -y libx11-dev && \
    apt install -y libxrandr-dev && \
    apt install -y libxinerama-dev && \
    apt install -y libxcursor-dev && \
    apt install -y nasm && \
    apt install -y libxi-dev && \
    apt install -y libvdpau-dev && \
    apt install -y libva-dev

RUN apt install -y gcc g++

RUN apt install -y python3 python3-pip

# RUN /bin/sh -c pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# RUN /bin/sh -c pip3 install empy

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt update -y && \
    apt install -y libdrm-dev && \
    apt install -y libvulkan-dev vulkan-utils

RUN apt install -y libgbm-dev libasound2-dev libfreetype6-dev liblzma-dev libglfw3-dev libx11-dev && \
    apt install -y libxrandr-dev && \
    apt install -y libxinerama-dev && \
    apt install -y libxcursor-dev && \
    apt install -y libxv-dev && \
    apt install -y libxext-dev && \
    apt install -y nasm && \
    apt install -y libxi-dev && \
    apt install -y libvdpau-dev && \
    apt install -y libva-dev

# Install CMake 3.22.1
RUN wget https://cmake.org/files/v3.22/cmake-3.22.1.tar.gz && \
    tar -zxvf cmake-3.22.1.tar.gz && \
    cd cmake-3.22.1 && \
    ./bootstrap --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf cmake-3.22.1 cmake-3.22.1.tar.gz
