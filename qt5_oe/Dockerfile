# 使用 openEuler 22.03 LTS SP4 的 ARM64 镜像（支持在 x86_64 上通过 --platform=arm64 运行）
FROM --platform=arm64 wqhot/qt5_oe:v1.0
USER root

# 使用华为云镜像加速（提升国内构建速度）
RUN yum makecache

# 安装所有构建依赖（包括系统工具、编译器、Mesa 所需的开发库）
RUN yum install -y \
    qt5 \
    qt5-devel 

RUN dnf install -y rpm-build

COPY *.spec /root/

RUN yum install -y dnf-plugins-core

RUN yum-builddep -y /root/qt5-qt3d.spec && \
    yum-builddep -y /root/qt5-qtbase.spec && \
    yum-builddep -y /root/qt5-qtcharts.spec && \
    yum-builddep -y /root/qt5-qtconnectivity.spec && \
    yum-builddep -y /root/qt5-qtdeclarative.spec && \
    yum-builddep -y /root/qt5-qtdoc.spec && \
    yum-builddep -y /root/qt5-qtgraphicaleffects.spec && \
    yum-builddep -y /root/qt5-qtimageformats.spec && \
    yum-builddep -y /root/qt5-qtlocation.spec && \
    yum-builddep -y /root/qt5-qtmultimedia.spec && \
    yum-builddep -y /root/qt5-qtquickcontrols.spec && \
    yum-builddep -y /root/qt5-qtquickcontrols2.spec && \
    yum-builddep -y /root/qt5-qtscript.spec && \
    yum-builddep -y /root/qt5-qtsensors.spec && \
    yum-builddep -y /root/qt5-qtserialbus.spec && \
    yum-builddep -y /root/qt5-qtserialport.spec && \
    yum-builddep -y /root/qt5-qtspeech.spec && \
    yum-builddep -y /root/qt5-qtsvg.spec && \
    yum-builddep -y /root/qt5-qttools.spec && \
    yum-builddep -y /root/qt5-qttranslations.spec && \
    yum-builddep -y /root/qt5-qtvirtualkeyboard.spec && \
    yum-builddep -y /root/qt5-qtwayland.spec && \
    yum-builddep -y /root/qt5-qtwebchannel.spec && \
    yum-builddep -y /root/qt5-qtwebengine.spec && \
    yum-builddep -y /root/qt5-qtwebkit.spec && \
    yum-builddep -y /root/qt5-qtwebsockets.spec && \
    yum-builddep -y /root/qt5-qtx11extras.spec && \
    yum-builddep -y /root/qt5-qtxmlpatterns.spec && \
    rm -rf /root/*.spec


ARG USER_NAME=builduser
USER ${USER_NAME}

WORKDIR /home/${USER_NAME}/rpmbuild
VOLUME ["/home/${USER_NAME}/rpmbuild"]

# 提供默认命令，便于进入容器
CMD ["/bin/bash"]