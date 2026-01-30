FROM wqhot/gcc9:v1.5

# Install required dependencies
RUN export DEBIAN_FRONTEND=noninteractive && \
    apt update -y && \
    apt install -y libdrm-dev && \
    apt install -y libvulkan-dev vulkan-tools vulkan-utils vulkan-validationlayers-dev

RUN apt install -y libgbm-dev
