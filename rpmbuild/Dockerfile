FROM --platform=arm64 hub.oepkgs.net/openeuler/openeuler:22.03-lts-sp4

# 安装依赖项
RUN yum makecache

RUN yum install -y rpm-build rpmdevtools vim \
    && yum clean all

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

WORKDIR /home/${USER_NAME}/rpmbuild
VOLUME ["/home/${USER_NAME}/rpmbuild"]