FROM ubuntu:20.04

RUN sed -i "s@http://.*archive.ubuntu.com@http://mirrors.huaweicloud.com@g" /etc/apt/sources.list && \
    sed -i "s@http://.*security.ubuntu.com@http://mirrors.huaweicloud.com@g" /etc/apt/sources.list
# Install required dependencies
RUN export DEBIAN_FRONTEND=noninteractive && \
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
    apt install -y git gcc g++ gdb

RUN apt install -y libx11-dev && \
    apt install -y libxrandr-dev && \
    apt install -y libxinerama-dev && \
    apt install -y libxcursor-dev && \
    apt install -y libxv-dev && \
    apt install -y libxext-dev && \
    apt install -y nasm && \
    apt install -y libxi-dev && \
    apt install -y libvdpau-dev && \
    apt install -y libva-dev && \
    apt install -y libegl-dev libgl-dev libgles-dev

RUN apt install -y libglfw3-dev

RUN apt install -y liblzma-dev

RUN apt install -y libfreetype6-dev

RUN apt install -y libavcodec-dev libavformat-dev libavutil-dev libswscale-dev libswresample-dev libavdevice-dev libavfilter-dev
