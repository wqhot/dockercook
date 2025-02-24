FROM --platform=linux/amd64 ubuntu:18.04

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y sudo && \
    apt-get install -y repo git python ssh make gcc libssl-dev liblz4-tool \
    expect g++ patchelf chrpath gawk texinfo diffstat binfmt-support \
    qemu-user-static live-build bison flex fakeroot cmake \
    gcc-multilib g++-multilib unzip device-tree-compiler ncurses-dev

ENV LANG=zh_CN.UTF-8 \
    LANGUAGE=zh_CN:zh \
    LC_ALL=zh_CN.UTF-8

RUN apt-get install -y language-pack-zh-hans && \
    locale-gen zh_CN.UTF-8 && \
    update-locale LANG=zh_CN.UTF-8

RUN apt-get install -y zsh openssh-server vim curl && \
    apt-get clean all

ARG USER_NAME=wq
ARG USER_ID=1000
ARG GROUP_ID=1000
RUN groupadd -g ${GROUP_ID} ${USER_NAME} && \
    useradd -u ${USER_ID} -g ${GROUP_ID} -m -s /bin/bash ${USER_NAME} && \
    echo "${USER_NAME} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

WORKDIR /home/${USER_NAME}/sdk
RUN chown -R ${USER_NAME}:${USER_NAME} /home/${USER_NAME}
USER ${USER_NAME}

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended && \
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
    git clone https://github.com/zsh-users/zsh-syntax-highlighting ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

RUN sed -i 's/^plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting z extract web-search)/' ~/.zshrc && \
    sed -i 's/^ZSH_THEME=.*/ZSH_THEME="agnoster"/' ~/.zshrc && \
    echo "export TERM=xterm-256color" >> ~/.zshrc

WORKDIR /home/${USER_NAME}    
VOLUME ["/home/${USER_NAME}/sdk"]