# openEuler 22.03 SP4 离线安装测试

测试从本地Apache和npm镜像离线安装Node.js和npm包。

## 快速开始

### 1. 构建并启动容器

```bash
cd /home/wq/dev/dockercook/oe2203sp4_test
docker compose up -d --build
```

### 2. 进入容器

```bash
docker exec -it oe2203sp4-test bash
```

### 3. 禁止外网访问（可选）

在容器内执行：

```bash
# 删除默认网关（禁止外网访问）
ip route del default

# 验证外网不可访问
curl -I https://www.baidu.com
# 应该超时或失败
```

### 4. 运行测试脚本

```bash
./test-offline-install.sh
```

## 手动测试步骤

### 1. 下载安装脚本

```bash
wget http://host.docker.internal/nodejs/install.sh
chmod +x install.sh
```

### 2. 安装Node.js

```bash
./install.sh host.docker.internal
```

### 3. 使用npm安装包

```bash
export PATH=/opt/nodejs/bin:$PATH
node --version
npm --version

# 从本地镜像安装包
npm install @openai/codex
npm install @anthropic-ai/claude-code
```

## 网络说明

| 服务 | 容器内地址 | 说明 |
|------|-----------|------|
| Apache | `http://host.docker.internal/nodejs/` | Node.js下载 |
| npm镜像 | `http://host.docker.internal:4873/` | Verdaccio |

## 故障排查

### Apache不可访问

检查Apache是否运行：
```bash
# 在宿主机执行
curl http://localhost/nodejs/install.sh
```

### npm镜像不可访问

检查Verdaccio容器是否运行：
```bash
# 在宿主机执行
docker ps | grep npm-mirror
curl http://localhost:4873/
```

### 外网可访问

删除默认网关：
```bash
# 在容器内执行
ip route del default
```

## 清理

```bash
docker compose down
```
