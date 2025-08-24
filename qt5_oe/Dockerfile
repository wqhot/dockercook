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
    git make gcc gcc-c++ bison byacc flex ninja-build \
    openssh-server sudo lz4 pkgconf \
    meson cmake \
    # X11 和 DRM 相关开发库
    libX11-devel libXext-devel libXfixes-devel libXdamage-devel \
    libXrandr-devel libxshmfence-devel libXxf86vm-devel \
    libdrm-devel \
    abrt-dbus alsa-lib-devel  bzip2-devel dbus-devel \
    ffmpeg-devel fontconfig-devel freetype-devel \
    genwqe-zlib glibc-nss-devel gperf gperftools-devel graphite2 \
    harfbuzz harfbuzz-devel \
    # XCB 及其模块
    xcb-util-wm-devel xcb-util-image-devel \
    xcb-util-keysyms-devel xcb-util-renderutil-devel \
    xorg-x11-proto-devel libxcb-devel libxkbcommon-devel \
    libX11-devel libXau-devel libXext-devel libXrender-devel libdrm-devel \
    libevdev-devel libinput-devel libudev-devel libxcb-devel libxkbcommon-devel \
    libxkbcommon-x11-devel xcb-util-devel xcb-proto xorg-x11-drv-evdev-devel xorg-x11-drv-libinput-devel \
    xorg-x11-font-utils xorg-x11-proto-devel xorg-x11-server-devel xorg-x11-xauth \
    # GL
    libglvnd libglvnd-devel libglvnd-core-devel libglvnd-egl libglvnd-gles libglvnd-opengl \
    libgudev  mesa-libEGL mesa-libGL-devel mesa-libglapi \
    # 其他
    elfutils-libelf-devel libicu-devel libinput-devel libjpeg-turbo-devel libpng-devel libwacom libgudev-devel \
    mtdev-devel nspr-devel nss-devel nss-util-devel openssl-devel systemd-devel tslib-devel \
    # 调试与工具
    vim tar gzip which expat expat-devel libunwind libunwind-devel

RUN yum install -y wget

RUN yum install -y \
    libXi-devel libXcomposite-devel libXcursor-devel libXtst-devel \
    ffmpeg-libs ffmpeg-devel ffmpeg libvpx-devel libwebp-devel opus-devel \
    libstdc++-static


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

# 切换到构建用户
USER ${USER_NAME}
WORKDIR /home/${USER_NAME}

RUN wget -O Miniconda3-latest-Linux-aarch64.sh https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-aarch64.sh && \
    bash Miniconda3-latest-Linux-aarch64.sh -b -p /home/${USER_NAME}/miniconda3 && \
    rm Miniconda3-latest-Linux-aarch64.sh

ENV PATH=/home/${USER_NAME}/miniconda3/bin:$PATH

RUN conda init
# 接受conda的Terms of Service
RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && \
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
# 添加conda-forge channel以获取Python 2.7
RUN conda config --add channels conda-forge
# conda安装python2环境（使用conda-forge channel）
RUN conda create -n py2 python=2.7 -c conda-forge -y

# 设置 Mesa 源码目录
WORKDIR /home/${USER_NAME}/qt5
VOLUME ["/home/${USER_NAME}/qt5"]

# 提供默认命令，便于进入容器
CMD ["/bin/bash"]