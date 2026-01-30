#!/bin/bash

# ukui-kwin RPM 构建脚本
# 使用方法: ./run.sh

set -e

PWD=$(pwd)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="wqhot/oe2203sp4:v1.0"
CONTAINER_NAME="oe2203sp4-builder"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查源码目录是否存在
if [ ! -d "${PWD}/ukui-kwin" ]; then
    echo -e "${RED}错误: 未找到 ukui-kwin 目录${NC}"
    echo "请确保当前目录下存在 ukui-kwin 目录，包含以下文件："
    echo "  - ukui-kwin-1.0.5.tar.gz"
    echo "  - ukui-kwin.spec"
    echo "  - 0001-fix-ukui-kwin-data-install-error.patch"
    echo "  - 0002-fix-mate-terminal-theme.patch"
    exit 1
fi

# 检查必需文件
REQUIRED_FILES=("ukui-kwin-1.0.5.tar.gz" "ukui-kwin.spec")
MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "${PWD}/ukui-kwin/${file}" ]; then
        MISSING_FILES+=("${file}")
    fi
done

if [ ${#MISSING_FILES[@]} -ne 0 ]; then
    echo -e "${RED}错误: 缺少必需文件:${NC}"
    for file in "${MISSING_FILES[@]}"; do
        echo "  - ${file}"
    done
    exit 1
fi

# 检查 Docker 镜像是否存在，如果不存在则构建
if ! docker images | grep -q "^ukui-kwin-build"; then
    echo -e "${YELLOW}构建 Docker 镜像...${NC}"
    docker build -t ${IMAGE_NAME} -f "${SCRIPT_DIR}/Dockerfile" "${SCRIPT_DIR}"
    if [ $? -ne 0 ]; then
        echo -e "${RED}Docker 镜像构建失败！${NC}"
        exit 1
    fi
    echo -e "${GREEN}Docker 镜像构建完成${NC}"
fi

# 创建输出目录
mkdir -p "${PWD}/rpm-output"

# 运行容器并构建 RPM
echo -e "${GREEN}开始构建 ukui-kwin RPM 包...${NC}"
echo ""

docker run -it --rm \
    --name ${CONTAINER_NAME} \
    -v "${PWD}/ukui-kwin:/home/builduser/ukui-kwin-source:ro" \
    -v "${PWD}/rpm-output:/home/builduser/rpm-output" \
    -e USER_ID=$(id -u) \
    -e GROUP_ID=$(id -g) \
    ${IMAGE_NAME} \
    /bin/bash -c "
        set -e
        
        echo '=== 设置 rpmbuild 环境 ==='
        # 设置 rpmbuild 目录结构
        mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
        
        echo '=== 复制源码文件 ==='
        # 复制源码和补丁到 SOURCES 目录
        if ls /home/builduser/ukui-kwin-source/ukui-kwin-*.tar.gz 1> /dev/null 2>&1; then
            cp /home/builduser/ukui-kwin-source/ukui-kwin-*.tar.gz ~/rpmbuild/SOURCES/
            echo '✓ 源码包已复制'
        else
            echo '警告: 未找到源码包'
        fi
        
        if ls /home/builduser/ukui-kwin-source/*.patch 1> /dev/null 2>&1; then
            cp /home/builduser/ukui-kwin-source/*.patch ~/rpmbuild/SOURCES/
            echo '✓ 补丁文件已复制'
        else
            echo '警告: 未找到补丁文件'
        fi
        
        # 复制 spec 文件到 SPECS 目录
        if ls /home/builduser/ukui-kwin-source/*.spec 1> /dev/null 2>&1; then
            cp /home/builduser/ukui-kwin-source/*.spec ~/rpmbuild/SPECS/
            echo '✓ spec 文件已复制'
        else
            echo '错误: 未找到 spec 文件'
            exit 1
        fi
        
        echo ''
        echo '=== 开始构建 RPM 包 ==='
        cd ~/rpmbuild/SPECS
        SPEC_FILE=\$(ls *.spec | head -n 1)
        echo \"使用 spec 文件: \${SPEC_FILE}\"
        
        # 构建 RPM 包（显示详细输出）
        rpmbuild -ba \${SPEC_FILE} || {
            echo '错误: rpmbuild 构建失败'
            echo '查看构建日志:'
            tail -50 ~/rpmbuild/BUILD/*/CMakeFiles/CMakeOutput.log 2>/dev/null || true
            exit 1
        }
        
        echo ''
        echo '=== 复制构建结果 ==='
        # 复制构建结果到输出目录
        if [ -d ~/rpmbuild/RPMS ]; then
            cp -r ~/rpmbuild/RPMS/* /home/builduser/rpm-output/ 2>/dev/null || true
            echo '✓ 二进制 RPM 包已复制'
        fi
        
        if [ -d ~/rpmbuild/SRPMS ]; then
            cp -r ~/rpmbuild/SRPMS/* /home/builduser/rpm-output/ 2>/dev/null || true
            echo '✓ 源码 RPM 包已复制'
        fi
        
        echo ''
        echo '=== 构建完成 ==='
        echo '生成的 RPM 包:'
        ls -lh /home/builduser/rpm-output/ 2>/dev/null || echo '未找到输出文件'
    "

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ 构建成功！${NC}"
    echo -e "RPM 包位于: ${GREEN}${PWD}/rpm-output/${NC}"
    echo ""
    echo "生成的文件:"
    ls -lh "${PWD}/rpm-output/" 2>/dev/null || echo "未找到输出文件"
else
    echo ""
    echo -e "${RED}✗ 构建失败！${NC}"
    exit 1
fi

