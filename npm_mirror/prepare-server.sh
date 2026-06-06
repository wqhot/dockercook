#!/bin/bash

# ============================================
# 服务端脚本：准备Node.js和客户端安装脚本
# 运行环境：有网络的服务器
# 输出：web-files/ 目录，需要手动复制到Apache
# ============================================

NODE_VERSION="${1:-22.12.0}"
MIRROR_DIR="$(cd "$(dirname "$0")" && pwd)"
WEB_FILES_DIR="$MIRROR_DIR/web-files"

echo "========================================="
echo "准备Node.js和安装脚本（服务端）"
echo "========================================="
echo "Node.js版本: $NODE_VERSION"
echo "输出目录: $WEB_FILES_DIR"
echo ""

# 下载Node.js二进制包
download_nodejs() {
    echo ">>> 下载Node.js二进制包..."
    mkdir -p "$WEB_FILES_DIR/nodejs"
    
    for arch in x64 arm64; do
        local filename="node-v$NODE_VERSION-linux-$arch.tar.xz"
        local url="https://nodejs.org/dist/v$NODE_VERSION/$filename"
        local filepath="$WEB_FILES_DIR/nodejs/$filename"
        
        if [ -f "$filepath" ]; then
            echo "  ✅ 已存在: $filename"
        else
            echo "  下载: $filename"
            curl -f -L -o "$filepath" "$url" || {
                echo "  ❌ 下载失败: $filename"
                return 1
            }
        fi
    done
    
    # 创建版本信息文件
    echo "$NODE_VERSION" > "$WEB_FILES_DIR/nodejs/VERSION"
    
    echo ""
    echo "✅ Node.js已下载"
}

# 创建客户端安装脚本
create_client_script() {
    echo ""
    echo ">>> 创建客户端安装脚本..."
    
    cat > "$WEB_FILES_DIR/nodejs/install.sh" << 'INSTALL_SCRIPT'
#!/bin/bash

# ============================================
# 客户端脚本：从服务端安装Node.js
# 运行环境：只能访问服务端的客户端
# 支持两种执行方式：
#   1. wget && ./install.sh
#   2. curl -sSL ... -o /tmp/install.sh && bash /tmp/install.sh
# ============================================

SERVER_IP="${1:-host.docker.internal}"
NODE_VERSION="${2:-NODE_VERSION_PLACEHOLDER}"
INSTALL_DIR="${INSTALL_DIR:-/opt/nodejs}"

echo "=========================================" >&2
echo "安装Node.js（客户端）" >&2
echo "=========================================" >&2
echo "服务器: $SERVER_IP" >&2
echo "Node.js版本: $NODE_VERSION" >&2
echo "安装目录: $INSTALL_DIR" >&2
echo "" >&2

# 检测架构
detect_arch() {
    local arch=$(uname -m)
    case $arch in
        x86_64|amd64) echo "x64" ;;
        aarch64|arm64) echo "arm64" ;;
        *) echo "❌ 不支持的架构: $arch" >&2; exit 1 ;;
    esac
}

# 下载Node.js
download_nodejs() {
    local arch=$(detect_arch)
    local filename="node-v$NODE_VERSION-linux-$arch.tar.xz"
    local url="http://$SERVER_IP/nodejs/$filename"
    local tmp_file="/tmp/$filename"

    echo ">>> 检测到架构: $arch" >&2
    echo ">>> 从服务端下载Node.js..." >&2
    echo "    URL: $url" >&2

    wget -q -O "$tmp_file" "$url" 2>&2 || {
        echo "❌ 下载失败" >&2
        exit 1
    }

    echo "✅ 下载完成" >&2
    # 返回文件路径（唯一输出到stdout的）
    echo "$tmp_file"
}

# 安装Node.js
install_nodejs() {
    local tar_file="$1"

    echo "" >&2
    echo ">>> 解压安装Node.js..." >&2
    mkdir -p "$INSTALL_DIR"
    tar -xf "$tar_file" -C "$INSTALL_DIR" --strip-components=1

    rm -f "$tar_file"

    echo "✅ 安装完成" >&2
}

# 配置npm镜像
configure_npm() {
    echo "" >&2
    echo ">>> 配置npm镜像..." >&2

    export PATH="$INSTALL_DIR/bin:$PATH"

    # 配置npm全局包安装目录为~/.nvm
    mkdir -p ~/.nvm/bin
    mkdir -p ~/.nvm/lib
    mkdir -p ~/.nvm/share

    npm config set prefix ~/.nvm
    npm config set registry "http://$SERVER_IP:4873"

    # 更新PATH，包含npm全局包目录
    export PATH=~/.nvm/bin:$PATH

    # 写入bashrc
    echo "" >> ~/.bashrc
    echo "# Node.js and npm configuration" >> ~/.bashrc
    echo "export PATH=$INSTALL_DIR/bin:\$PATH" >> ~/.bashrc
    echo "export PATH=~/.nvm/bin:\$PATH" >> ~/.bashrc

    echo "✅ npm已配置" >&2
    echo "   Registry: http://$SERVER_IP:4873" >&2
    echo "   全局包目录: ~/.nvm" >&2
    echo "   全局包命令: ~/.nvm/bin" >&2
}

# 显示使用说明
show_usage() {
    echo "" >&2
    echo "=========================================" >&2
    echo "安装完成！" >&2
    echo "=========================================" >&2
    echo "" >&2
    echo "Node.js: $($INSTALL_DIR/bin/node --version)" >&2
    echo "npm: $($INSTALL_DIR/bin/npm --version)" >&2
    echo "" >&2
    echo "配置信息:" >&2
    echo "  Node.js目录: $INSTALL_DIR" >&2
    echo "  npm全局包目录: ~/.nvm" >&2
    echo "  npm全局包命令: ~/.nvm/bin" >&2
    echo "  npm镜像: http://$SERVER_IP:4873" >&2
    echo "" >&2
    echo "使用方法:" >&2
    echo "  source ~/.bashrc  # 或重新登录" >&2
    echo "  node --version" >&2
    echo "  npm install -g <package>  # 全局包将安装在~/.nvm" >&2
    echo "" >&2
    echo "示例:" >&2
    echo "  npm install -g @openai/codex" >&2
    echo "  codex --version" >&2
}

# 主流程
if [ "$SERVER_IP" = "需指定服务器IP" ]; then
    echo "用法: $0 <服务器IP> [Node.js版本]" >&2
    echo "" >&2
    echo "示例:" >&2
    echo "  $0 192.168.1.100" >&2
    echo "  $0 192.168.1.100 22.12.0" >&2
    echo "" >&2
    echo "可选环境变量:" >&2
    echo "  INSTALL_DIR=/opt/nodejs  # 安装目录" >&2
    exit 1
fi

tar_file=$(download_nodejs)
install_nodejs "$tar_file"
configure_npm
show_usage
INSTALL_SCRIPT

    # 替换版本号
    sed -i "s/NODE_VERSION_PLACEHOLDER/$NODE_VERSION/g" "$WEB_FILES_DIR/nodejs/install.sh"
    chmod +x "$WEB_FILES_DIR/nodejs/install.sh"
    
    echo "✅ 客户端脚本已创建"
}

# 显示使用说明
show_usage() {
    echo ""
    echo "========================================="
    echo "准备完成！"
    echo "========================================="
    echo ""
    echo "文件已准备在: $WEB_FILES_DIR/"
    echo ""
    echo "目录结构:"
    echo "  web-files/nodejs/"
    echo "    ├── node-v$NODE_VERSION-linux-x64.tar.xz"
    echo "    ├── node-v$NODE_VERSION-linux-arm64.tar.xz"
    echo "    ├── install.sh"
    echo "    └── VERSION"
    echo ""
    echo "下一步："
    echo "  1. 复制到Apache目录："
    echo "     cp -r $WEB_FILES_DIR/nodejs /var/www/html/"
    echo ""
    echo "  2. 客户端安装："
    echo "     wget http://<server-ip>/nodejs/install.sh"
    echo "     ./install.sh <server-ip>"
}

# 主流程
download_nodejs
create_client_script
show_usage
