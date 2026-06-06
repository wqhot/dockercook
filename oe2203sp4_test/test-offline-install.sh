#!/bin/bash

# ============================================
# 离线安装测试脚本
# ============================================

echo "========================================="
echo "离线安装测试"
echo "========================================="
echo ""

# 获取宿主机IP
HOST_IP="host.docker.internal"

echo "宿主机地址: $HOST_IP"
echo ""

# 测试网络连接
echo ">>> 测试网络连接..."
echo ""

# 测试Apache (Node.js下载)
echo "1. 测试Apache连接 (Node.js下载):"
if curl -s -I http://$HOST_IP/nodejs/install.sh | grep -q "200 OK"; then
    echo "   ✅ Apache可访问: http://$HOST_IP/nodejs/"
else
    echo "   ❌ Apache不可访问"
fi

# 测试npm镜像
echo ""
echo "2. 测试npm镜像连接:"
if curl -s http://$HOST_IP:4873/ | grep -q "Verdaccio"; then
    echo "   ✅ npm镜像可访问: http://$HOST_IP:4873/"
else
    echo "   ❌ npm镜像不可访问"
fi

# 测试外网访问（应该失败）
echo ""
echo "3. 测试外网访问（应该失败）:"
if curl -s --connect-timeout 5 https://www.baidu.com > /dev/null 2>&1; then
    echo "   ⚠️  外网可访问（建议禁用）"
else
    echo "   ✅ 外网不可访问（正确）"
fi

echo ""
echo "========================================="
echo "测试完成"
echo "========================================="
echo ""
echo "手动测试步骤："
echo ""
echo "1. 下载安装脚本："
echo "   wget http://$HOST_IP/nodejs/install.sh"
echo ""
echo "2. 安装Node.js："
echo "   chmod +x install.sh"
echo "   ./install.sh $HOST_IP"
echo ""
echo "3. 使用npm安装包："
echo "   export PATH=/opt/nodejs/bin:\$PATH"
echo "   npm install @openai/codex"
