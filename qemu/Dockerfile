FROM ubuntu:24.04

# 设置环境变量避免交互式配置
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=zh_CN.UTF-8
ENV LANGUAGE=zh_CN:en_US
ENV LC_ALL=zh_CN.UTF-8
ENV TERM=xterm-256color

# 暴露端口
# 1234: 用于 GDB 调试
# 2222: 用于 SSH 连接
EXPOSE 1234 2222

# 安装基本工具和QEMU
RUN apt-get update && apt-get install -y \
    qemu-system-aarch64 \
    qemu-utils \
    wget \
    curl \
    git \
    zsh \
    sudo \
    language-pack-zh-hans \
    && rm -rf /var/lib/apt/lists/*

# 设置中文环境
RUN locale-gen zh_CN.UTF-8 && \
    update-locale LANG=zh_CN.UTF-8

# 切换到ubuntu用户进行配置
USER ubuntu
WORKDIR /home/ubuntu

# 安装oh-my-zsh和插件
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended && \
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
    git clone https://github.com/zsh-users/zsh-syntax-highlighting ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# 配置zsh
RUN sed -i 's/^plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting z extract)/' ~/.zshrc && \
    sed -i 's/^ZSH_THEME=.*/ZSH_THEME="agnoster"/' ~/.zshrc && \
    echo "export TERM=xterm-256color" >> ~/.zshrc && \
    echo "export LANG=zh_CN.UTF-8" >> ~/.zshrc && \
    echo "export LANGUAGE=zh_CN:en_US" >> ~/.zshrc && \
    echo "export LC_ALL=zh_CN.UTF-8" >> ~/.zshrc

# 创建工作目录
WORKDIR /workspace

# 设置默认shell为zsh
SHELL ["/bin/zsh", "-c"]