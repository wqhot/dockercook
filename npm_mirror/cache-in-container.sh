#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Usage: $0 <package-name> [<package-name2> ...]"
  echo ""
  echo "Example:"
  echo "  $0 @openai/codex @anthropic-ai/claude-code"
  exit 1
fi

echo "Fetching package metadata and collecting all platform-specific packages..."

# 收集所有需要安装的包
ALL_PACKAGES=()

for pkg in "$@"; do
  echo "Processing $pkg..."
  ALL_PACKAGES+=("$pkg")
  
  # 获取optionalDependencies（平台特定包）
  OPTIONAL=$(curl -s "https://registry.npmjs.org/$pkg" 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    latest = data.get('dist-tags', {}).get('latest')
    if latest and latest in data['versions']:
        optional = data['versions'][latest].get('optionalDependencies', {})
        for opt_pkg, opt_value in optional.items():
            # 输出格式：包名:值（值可能是版本号或npm:别名）
            print(f'{opt_pkg}:{opt_value}')
except:
    pass
" 2>/dev/null)
  
  if [ -n "$OPTIONAL" ]; then
    while IFS= read -r line; do
      # 解析别名格式：@openai/codex-darwin-arm64:npm:@openai/codex@0.137.0-darwin-arm64
      if echo "$line" | grep -q "npm:"; then
        # 提取 npm: 后面的部分，例如 @openai/codex@0.137.0-darwin-arm64
        actual_pkg_with_version=$(echo "$line" | sed 's/.*npm:\(.*\)/\1/')
        echo "  + Adding platform package: $actual_pkg_with_version"
        ALL_PACKAGES+=("$actual_pkg_with_version")
      else
        # 普通包名，格式：包名:版本
        opt_pkg=$(echo "$line" | cut -d: -f1)
        # 检查包是否真实存在于npm registry
        EXISTS=$(curl -s "https://registry.npmjs.org/$opt_pkg" 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print('yes' if 'name' in data and 'error' not in data else 'no')
except:
    print('no')
" 2>/dev/null)
        
        if [ "$EXISTS" = "yes" ]; then
          echo "  + Adding platform package: $opt_pkg"
          ALL_PACKAGES+=("$opt_pkg")
        fi
      fi
    done <<< "$OPTIONAL"
  fi
done

echo ""
echo "Creating package.json with ${#ALL_PACKAGES[@]} packages..."
docker exec npm-mirror sh -c "mkdir -p /tmp/cache"

cat > /tmp/package.json << EOF
{
  "dependencies": {
EOF

FIRST=true
for pkg in "${ALL_PACKAGES[@]}"; do
  if [ "$FIRST" = true ]; then
    FIRST=false
  else
    echo "," >> /tmp/package.json
  fi
  
  # 检查是否是 别名格式（包含@版本号）
  if echo "$pkg" | grep -q "@.*@.*"; then
    # 例如：@openai/codex@0.137.0-linux-x64
    # 提取包名和版本
    pkg_name=$(echo "$pkg" | sed 's/\(.*\)@.*/\1/')
    version=$(echo "$pkg" | sed 's/.*@\(.*\)/\1/')
    # 提取平台信息（例如：linux-x64）
    platform=$(echo "$version" | grep -o '[^-]*-[^-]*$')
    # 生成唯一别名
    alias_name=$(echo "$pkg_name" | sed 's/@//; s/\//-/')_$platform
    echo "    \"$alias_name\": \"npm:$pkg_name@$version\"" >> /tmp/package.json
  else
    echo "    \"$pkg\": \"*\"" >> /tmp/package.json
  fi
done

echo "  }" >> /tmp/package.json
echo "}" >> /tmp/package.json

docker cp /tmp/package.json npm-mirror:/tmp/cache/package.json

echo ""
echo "Installing packages in container (ignoring platform restrictions)..."
docker exec npm-mirror sh -c "cd /tmp/cache && npm install --registry http://localhost:4873 --ignore-scripts --force"

echo ""
echo "Cleaning up..."
echo "Generated package.json:"
docker exec npm-mirror cat /tmp/cache/package.json
docker exec npm-mirror rm -rf /tmp/cache
rm -f /tmp/package.json

echo ""
echo "✅ Done! Checking cached packages..."
echo ""
echo "📦 Cached tarballs:"
docker exec npm-mirror find /verdaccio/storage/ -name "*.tgz" 2>/dev/null | sort

echo ""
echo "📊 Statistics:"
echo "   - Total packages: $(docker exec npm-mirror find /verdaccio/storage/ -type d -mindepth 2 2>/dev/null | wc -l)"
echo "   - Total tarballs: $(docker exec npm-mirror find /verdaccio/storage/ -name "*.tgz" 2>/dev/null | wc -l)"
