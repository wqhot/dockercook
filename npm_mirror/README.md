# npm本地镜像服务器

基于Verdaccio构建的本地npm包镜像缓存服务器，支持自动缓存所有平台的包。

## 快速开始

### 1. 启动服务

```bash
cd /home/wq/dev/dockercook/npm_mirror
docker compose up -d --build
```

### 2. 缓存npm包及其所有平台版本

使用 `cache-in-container.sh` 脚本缓存包：

```bash
# 缓存指定包（自动包含所有平台版本）
./cache-in-container.sh "@openai/codex" "@anthropic-ai/claude-code"

# 缓存其他包
./cache-in-container.sh "lodash" "axios" "react"
```

该脚本会：
- 自动获取包的最新版本
- 自动发现并下载所有平台特定的包（x64, arm64, win32, darwin, linux等）
- 自动缓存所有依赖

### 3. 使用本地镜像

在你的项目中配置npm使用本地镜像：

```bash
# 设置registry
npm config set registry http://localhost:4873

# 安装包（从本地缓存获取）
npm install -g @openai/codex @anthropic-ai/claude-code

# 或在项目中使用
npm install
```

## 文件说明

### 服务端文件

- `Dockerfile` - Verdaccio镜像构建文件
- `docker-compose.yaml` - Docker Compose配置
- `conf/config.yaml` - Verdaccio服务器配置
- `conf/htpasswd` - 用户认证文件
- `cache-in-container.sh` - npm包缓存脚本
- `prepare-server.sh` - 准备Node.js下载脚本
- `storage/` - 缓存的npm包存储

### 客户端文件（由服务端生成）

- `install.sh` - Node.js安装脚本（通过Apache提供）
- `node-v*-linux-*.tar.xz` - Node.js二进制包（通过Apache提供）

## 常用命令

```bash
# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f

# 停止服务
docker compose down

# 重启服务
docker compose restart

# 查看已缓存的包
docker exec npm-mirror find /verdaccio/storage/ -name "*.tgz"
```

## 缓存示例

缓存 `@anthropic-ai/claude-code` 后，会自动下载以下所有平台的包：

- `@anthropic-ai/claude-code` - 主包
- `@anthropic-ai/claude-code-linux-x64` - Linux x64
- `@anthropic-ai/claude-code-linux-arm64` - Linux arm64
- `@anthropic-ai/claude-code-win32-x64` - Windows x64
- `@anthropic-ai/claude-code-win32-arm64` - Windows arm64
- `@anthropic-ai/claude-code-darwin-x64` - macOS x64
- `@anthropic-ai/claude-code-darwin-arm64` - macOS arm64
- `@anthropic-ai/claude-code-linux-x64-musl` - Linux x64 (musl)
- `@anthropic-ai/claude-code-linux-arm64-musl` - Linux arm64 (musl)

## 管理

Verdaccio Web UI: http://localhost:4873

## 注意事项

- 所有缓存的包保存在 `storage/` 目录，即使容器重启数据也不会丢失
- 配置文件在 `conf/` 目录
- 服务默认运行在 4873 端口
- 脚本会自动检测并下载所有平台的包，无需手动指定

---

## Node.js离线安装

除了npm包镜像，本项目还提供Node.js的在线安装方案（仅连接服务器，不连互联网）。

### 工作流程

```
服务端（有网络+Apache）          客户端（只能访问服务端）
    │                                  │
    ├─ 1. 启动Verdaccio                │
    ├─ 2. 缓存npm包                    │
    ├─ 3. 准备Node.js                  │
    │   ./prepare-server.sh            │
    │   (放到Apache目录)                │
    │                                  │
    └─ 提供服务 ──────────────────────>├─ 4. 下载安装脚本
       - http://server/nodejs/         │   wget http://server/nodejs/install.sh
       - http://server:4873/           │
                                       ├─ 5. 安装Node.js
                                       │   ./install.sh <server-ip>
                                       │
                                       └─ 6. 使用npm安装包
                                           npm install <package>
```

### 服务端操作（有网络+Apache）

#### 1. 启动npm镜像服务

```bash
# 启动Verdaccio
docker compose up -d --build

# 缓存需要的npm包
./cache-in-container.sh "@openai/codex" "@anthropic-ai/claude-code"
```

#### 2. 准备Node.js下载

```bash
# 下载Node.js并准备客户端安装脚本
./prepare-server.sh 22.12.0

# 生成的文件在 web-files/nodejs/ 目录
```

#### 3. 复制到Apache

```bash
# 复制到Apache目录（需要root权限）
sudo cp -r web-files/nodejs /var/www/html/

# 或自定义Apache目录
cp -r web-files/nodejs /path/to/apache/
```

准备完成后，服务端提供：
- **Node.js下载**: `http://<server-ip>/nodejs/`
- **npm镜像**: `http://<server-ip>:4873/`

### 客户端操作（只能访问服务端）

#### 3. 下载安装脚本

```bash
# 从服务端下载安装脚本
wget http://<server-ip>/nodejs/install.sh
chmod +x install.sh
```

#### 4. 安装Node.js

```bash
# 安装（默认安装到/opt/nodejs）
./install.sh <server-ip>

# 或指定版本
./install.sh <server-ip> 22.12.0

# 或自定义安装目录
INSTALL_DIR=/usr/local/nodejs ./install.sh <server-ip>
```

#### 5. 使用

```bash
# 重新加载环境变量
source ~/.bashrc

# 验证
node --version  # v22.12.0
npm --version   # 10.9.0

# 安装npm包（自动从服务端获取）
npm install -g @openai/codex  # 全局包安装在~/.nvm
npm install @anthropic-ai/claude-code  # 本地包安装在当前目录

# 验证全局包
codex --version  # 命令在~/.nvm/bin
```

### npm全局包配置

安装后，npm全局包会自动配置到`~/.nvm`目录：

| 目录 | 说明 |
|------|------|
| `~/.nvm/bin` | 全局包命令 |
| `~/.nvm/lib/node_modules` | 全局包代码 |
| `~/.nvm/share` | man pages等 |

**PATH配置**（自动添加到`~/.bashrc`）：
```bash
export PATH=/opt/nodejs/bin:$PATH      # Node.js和npm
export PATH=~/.nvm/bin:$PATH           # npm全局包命令
``` install @anthropic-ai/claude-code
```

### 服务端提供的资源

| 资源 | 地址 | 说明 |
|------|------|------|
| Node.js下载 | `http://<server>/nodejs/` | x64和arm64二进制包 |
| 客户端安装脚本 | `http://<server>/nodejs/install.sh` | 自动安装脚本 |
| npm镜像 | `http://<server>:4873/` | Verdaccio镜像服务 |

### 支持的架构

| 架构 | Node.js | npm |
|------|---------|-----|
| Linux x64 | ✅ | ✅ |
| Linux arm64 | ✅ | ✅ |

### 常用Node.js版本

推荐使用LTS版本：
- **v22.12.0** - 当前LTS（推荐）
- **v20.18.0** - 上一代LTS
- **v18.20.0** - 旧版LTS

```bash
# 准备不同版本
./prepare-server.sh 22.12.0
./prepare-server.sh 20.18.0
```
