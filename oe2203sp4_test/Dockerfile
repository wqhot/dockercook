FROM openeuler/openeuler:22.03-lts-sp4

LABEL description="openEuler 22.03 SP4 - 离线安装测试环境"

# 安装基础工具
RUN yum install -y \
    wget \
    curl \
    tar \
    xz \
    && yum clean all

# 创建工作目录
WORKDIR /root

# 复制测试脚本
COPY test-offline-install.sh /root/
RUN chmod +x /root/test-offline-install.sh

CMD ["/bin/bash"]
