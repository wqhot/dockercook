# 使用 openEuler 22.03 LTS SP4 的 ARM64 镜像（支持在 x86_64 上通过 --platform=arm64 运行）
FROM --platform=arm64 hub.oepkgs.net/openeuler/openeuler:22.03-lts-sp4

# 维护者信息
LABEL maintainer="wqhot@outlook.com"

# 设置非交互模式
ENV DEBIAN_FRONTEND=noninteractive

# 使用华为云镜像加速（提升国内构建速度）
RUN yum makecache

# 安装所有构建依赖（包括系统工具、编译器、Mesa 所需的开发库）
RUN yum install -y \
    # 构建工具
    git make gcc gcc-c++ bison byacc flex \
    python3 python3-pip openssh-server sudo lz4 \
    meson cmake \
    # LLVM/Clang 支持（即使禁用，部分头文件可能仍需）
    llvm-devel clang-devel libclc-devel \
    # X11 和 DRM 相关开发库
    libX11-devel libXext-devel libXfixes-devel libXdamage-devel \
    libXrandr-devel libxshmfence-devel libXxf86vm-devel \
    libdrm-devel \
    # XCB 及其模块
    xcb-util-wm-devel xcb-util-image-devel \
    xcb-util-keysyms-devel xcb-util-renderutil-devel \
    xorg-x11-proto-devel libxcb-devel libxkbcommon-devel \
    # 其他
    elfutils-libelf-devel \
    # 调试与工具
    vim tar gzip which

# 创建构建用户（避免使用 root 构建）
ARG USER_NAME=builduser
ARG UID=1000
ARG GID=1000

RUN if getent group ${GID} > /dev/null 2>&1; then \
        GROUP_NAME=$(getent group ${GID} | cut -d: -f1); \
    else \
        GROUP_NAME="${USER_NAME}-group"; \
        groupadd -g ${GID} "${GROUP_NAME}"; \
    fi && \
    if getent passwd ${UID} > /dev/null 2>&1; then \
        USER_NAME=$(getent passwd ${UID} | cut -d: -f1); \
    else \
        useradd -u ${UID} -g ${GROUP_NAME} -m -s /bin/bash ${USER_NAME}; \
    fi && \
    echo "${USER_NAME}:${USER_NAME}" | chpasswd && \
    echo "${USER_NAME} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    mkdir -p /home/${USER_NAME} && \
    chown -R ${USER_NAME}:${GROUP_NAME} /home/${USER_NAME}


RUN dnf install -y libgudev-devel

RUN dnf install -y expat expat-devel libunwind libunwind-devel
# 切换到构建用户
USER ${USER_NAME}
WORKDIR /home/${USER_NAME}

# 安装 Rust 工具链（Mesa 子模块如 bindgen 需要）
# ENV CARGO_HOME=/home/${USER_NAME}/.cargo \
#     PATH=/home/${USER_NAME}/.cargo/bin:$PATH

# RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
#     source "$CARGO_HOME/env" && \
#     cargo install cbindgen bindgen-cli

# 安装 Python 工具（Miniconda + meson/ninja/mako）
# 注意：这里下载 aarch64 版本的 Miniconda
# RUN wget -O Miniconda3-latest-Linux-aarch64.sh https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-aarch64.sh && \
#     bash Miniconda3-latest-Linux-aarch64.sh -b -p /home/${USER_NAME}/miniconda3 && \
#     rm Miniconda3-latest-Linux-aarch64.sh

# ENV PATH=/home/${USER_NAME}/miniconda3/bin:$PATH

# # 初始化 conda（可选）
# RUN conda init && \
#     pip install --no-cache-dir meson ninja mako pyyaml

RUN pip install ninja mako pyyaml

# 设置 Mesa 源码目录
WORKDIR /home/${USER_NAME}/mesa
VOLUME ["/home/${USER_NAME}/mesa"]

# 提供默认命令，便于进入容器
CMD ["/bin/bash"]