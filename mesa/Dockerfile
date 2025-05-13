FROM --platform=linux/amd64 ubuntu:24.04

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y sudo repo git python-is-python3 ssh make gcc libssl-dev liblz4-tool \
    llvm clang meson glslang-tools

ENV LANG=zh_CN.UTF-8 \
    LANGUAGE=zh_CN:zh \
    LC_ALL=zh_CN.UTF-8

RUN apt-get install -y language-pack-zh-hans && \
    locale-gen zh_CN.UTF-8 && \
    update-locale LANG=zh_CN.UTF-8

RUN apt install -y bindgen

RUN apt install -y python3-pip libclc-19-dev pkg-config python3-mako libdrm-dev \
    libllvmspirvlib-18-dev cmake libclang-dev libelf-dev byacc flex libxcb1-dev \
    libxcb-randr0-dev libx11-dev libxext-dev libxcb-glx0-dev libxfixes-dev libxcb-shm0-dev \
    libx11-xcb-dev libxcb-dri3-dev  libxcb-sync0-dev libxcb-xfixes0-dev libxcb-xinerama0-dev \
    libxcb-xinput-dev libxcb-xkb-dev libxkbcommon-dev libxkbcommon-x11-dev libxcb-icccm4-dev \
    libxcb-image0-dev libxcb-keysyms1-dev libxcb-render-util0-dev libxcb-render0-dev \
    libxcb-present-dev libxshmfence-dev libxxf86vm-dev libxrandr-dev cbindgen


RUN apt-get install -y zsh openssh-server vim curl && \
    apt-get clean all

RUN git clone https://github.com/KhronosGroup/SPIRV-Tools.git && \
    cd SPIRV-Tools && \
    python3 ./utils/git-sync-deps && \
    mkdir build && \
    cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr -DSPIRV_SKIP_TESTS=ON -DSPIRV_LOG_LEVEL=0&& \
    make -j8 && \
    make install

ARG USER_NAME=ubuntu
RUN echo "${USER_NAME}:ubuntu" | chpasswd

WORKDIR /home/${USER_NAME}/mesa
RUN chown -R ${USER_NAME}:${USER_NAME} /home/${USER_NAME}
USER ${USER_NAME}

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs  | sh -s -- -y

ENV PATH="/home/ubuntu/.cargo/bin:${PATH}"

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended && \
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
    git clone https://github.com/zsh-users/zsh-syntax-highlighting ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

RUN sed -i 's/^plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting z extract)/' ~/.zshrc && \
    sed -i 's/^ZSH_THEME=.*/ZSH_THEME="agnoster"/' ~/.zshrc && \
    echo "export TERM=xterm-256color" >> ~/.zshrc

WORKDIR /home/${USER_NAME}    
VOLUME ["/home/${USER_NAME}/mesa"]

# 拷贝当前目录到容器中
COPY ./toolchains /home/${USER_NAME}/toolchains
ENV ARCH=arm64
ENV CROSS_COMPILE=aarch64-linux-gnu-
ENV PATH=/home/${USER_NAME}/toolchains/sysroots/x86_64-openeulersdk-linux/usr/bin:$PATH

# 设置工作目录
WORKDIR /home/${USER_NAME}/mesa

