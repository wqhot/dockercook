# 使用 openEuler 22.03 LTS SP4 的 ARM64 镜像（支持在 x86_64 上通过 --platform=arm64 运行）
FROM --platform=arm64 hub.oepkgs.net/openeuler/openeuler:22.03-lts-sp4

# 维护者信息
LABEL maintainer="wqhot@outlook.com"

# 设置非交互模式
ENV DEBIAN_FRONTEND=noninteractive

# 使用华为云镜像加速（提升国内构建速度）
RUN yum makecache

# 安装所有构建依赖（ukui-kwin 编译环境）
RUN yum install -y \
    # 基础构建工具
    git make gcc gcc-c++ bison byacc flex \
    python3 python3-pip openssh-server sudo lz4 \
    meson cmake extra-cmake-modules \
    pkg-config \
    # RPM 构建工具
    rpm-build rpmdevtools \
    # KF5 核心开发库
    kf5-kinit-devel kscreenlocker-devel kdecoration-devel \
    kf5-kactivities-devel kf5-kcompletion-devel kf5-kconfig-devel \
    kf5-kconfigwidgets-devel kf5-kcoreaddons-devel kf5-kcrash-devel \
    kf5-kdeclarative-devel kf5-kdoctools-devel kf5-kglobalaccel-devel \
    kf5-ki18n-devel kf5-kiconthemes-devel kf5-kidletime-devel \
    kf5-kcmutils-devel kf5-kio-devel kf5-knewstuff-devel \
    kf5-knotifications-devel kf5-kpackage-devel kf5-plasma-devel \
    kf5-kservice-devel kf5-ktextwidgets-devel kf5-kwayland-devel \
    kf5-kwidgetsaddons-devel kf5-kwindowsystem-devel kf5-kxmlgui-devel \
    kf5-kirigami2-devel kf5-kguiaddons-devel \
    # Qt5 开发库
    qt5-qtbase-devel qt5-qtbase-private-devel qt5-qtdeclarative-devel \
    qt5-qtscript-devel qt5-qttools-devel qt5-qtsensors-devel \
    qt5-qtx11extras-devel qt5-qtbase-static \
    # X11 和 XCB 相关开发库
    libX11-devel libXext-devel libXfixes-devel libXdamage-devel \
    libXrandr-devel libxshmfence-devel libXxf86vm-devel \
    libXcursor-devel libXi-devel libXtst-devel \
    libxcb-devel xcb-util-devel xcb-util-cursor xcb-util-cursor-devel \
    xcb-util-wm xcb-util-wm-devel xcb-util-image xcb-util-image-devel \
    xcb-util-keysyms xcb-util-keysyms-devel xcb-util-renderutil-devel \
    xorg-x11-proto-devel libxkbcommon-devel \
    # DRM 和图形相关
    libdrm-devel mesa-libEGL-devel libepoxy-devel libgbm-devel \
    # 输入和系统库
    libinput-devel libcap-devel libSM-devel libICE-devel \
    systemd-devel wayland-devel \
    # 字体和渲染
    fontconfig-devel freetype-devel \
    # KWin 相关
    kwin-devel plasma-breeze-devel \
    # 其他工具库
    gsettings-qt-devel \
    elfutils-libelf-devel libgudev-devel \
    expat expat-devel libunwind libunwind-devel \
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


# 切换到构建用户
USER ${USER_NAME}
WORKDIR /home/${USER_NAME}

# 安装 Python 构建工具
RUN pip install ninja mako pyyaml

# 设置 ukui-kwin 源码目录
WORKDIR /home/${USER_NAME}/ukui-kwin
VOLUME ["/home/${USER_NAME}/ukui-kwin"]

# 提供默认命令，便于进入容器
CMD ["/bin/bash"]