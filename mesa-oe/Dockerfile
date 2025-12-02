FROM hub.oepkgs.net/openeuler/openeuler:22.03-lts-sp4

# 安装依赖项
RUN yum makecache

RUN yum install -y sudo git python3 python3-pip openssh-server make gcc openssl-devel lz4 llvm clang meson g++ \
      libclc-devel pkgconfig python3-mako libdrm-devel llvm-devel cmake clang-devel elfutils-libelf-devel byacc flex xcb-util-wm-devel \
      xcb-util-image-devel xcb-util-keysyms-devel xcb-util-renderutil-devel xorg-x11-proto-devel libxcb-devel libxkbcommon-devel && \
    yum clean all

# 编译 glslang（作为子模块之一）
RUN git clone -b 14.3.0 --depth=1 https://github.com/KhronosGroup/glslang.git  && \
    cd glslang && \
    ./update_glslang_sources.py && \
    mkdir build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr -DSPIRV_SKIP_TESTS=ON -DSPIRV_LOG_LEVEL=0 && \
    make -j8 && \
    make install

# 创建用户
ARG USER_NAME=builduser
ARG UID=1000
ARG GID=1000

# 创建用户组和用户
RUN if getent group $GID > /dev/null 2>&1; then \
        echo "Group with GID $GID already exists"; \
    else \
        groupadd -g $GID "${USER_NAME}-group" || groupadd "${USER_NAME}-group"; \
    fi && \
    if getent passwd $UID > /dev/null 2>&1; then \
        echo "User with UID $UID already exists"; \
    else \
        useradd -u $UID -g ${USER_NAME}-group -m -s /bin/bash $USER_NAME || useradd -u $UID -m -s /bin/bash $USER_NAME; \
    fi && \
    # 设置用户密码
    echo "${USER_NAME}:builduser" | chpasswd && \
    # 添加用户到 sudoers
    echo "${USER_NAME} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    # 确保用户目录存在且权限正确
    mkdir -p /home/${USER_NAME} && \
    chown -R ${USER_NAME}:${USER_NAME}-group /home/${USER_NAME}

# 切换用户
USER ${USER_NAME}
WORKDIR /home/${USER_NAME}

# 安装 Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs  | sh -s -- -y && \
    source "$HOME/.cargo/env" &&\
    cargo install cbindgen


RUN curl -o Miniconda3-py312_25.3.1-1-Linux-x86_64.sh https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-py312_25.3.1-1-Linux-aarch64.sh && \
    bash Miniconda3-py312_25.3.1-1-Linux-x86_64.sh -b -p /home/${USER_NAME}/miniconda3 && \
    rm Miniconda3-py312_25.3.1-1-Linux-x86_64.sh

ENV PATH=/home/${USER_NAME}/miniconda3/bin:$PATH

RUN conda init &&\
    pip install meson ninja mako

RUN source "$HOME/.cargo/env" &&\
    cargo install bindgen-cli &&\
    pip install pyyaml

USER root

RUN dnf install -y libX11-devel

RUN dnf install -y libXext-devel libXfixes-devel libXdamage-devel libXrandr-devel 

RUN dnf makecache

RUN dnf install -y libxshmfence-devel libXxf86vm-devel bison

USER ${USER_NAME}

WORKDIR /home/${USER_NAME}/mesa
VOLUME ["/home/${USER_NAME}/mesa"]