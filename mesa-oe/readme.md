# 一次性注册多架构支持
docker run --privileged --rm tonistiigi/binfmt --install all

docker build -t wqhot/mesa-oe:v1.1 .

docker run -it --rm -v $(pwd)/panfork-mesa:/home/builduser/mesa -e USER_ID=$(id -u) -e GROUP_ID=$(id -g) wqhot/mesa-oe:v1.1 /bin/bash

meson -Dgallium-drivers=panfrost -Dvulkan-drivers= -Dllvm=disabled -Dplatforms=x11 --prefix=/usr

DESTDIR=../install ninja install

docker run -it --rm -v $(pwd)/panfork-mesa:/home/builduser/rpmbuild -e USER_ID=$(id -u) -e GROUP_ID=$(id -g) wqhot/rpmbuilder:v1.0 /bin/bash