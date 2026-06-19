#!/bin/zsh
cd "$(dirname "$0")"

echo "发布诊断"
echo "目标网站：https://shufan-art.github.io/shufan/"
echo ""

echo "1. 检查本地网页文件..."
python3 publish_to_github_pages.py
if [ -d "site" ]; then
  cp -R site/. .
fi

git remote set-url origin "https://shufan-art@github.com/shufan-art/shufan.git"

echo ""
echo "2. 检查 GitHub 授权是否存在..."
credential_info=$(printf "protocol=https\nhost=github.com\nusername=shufan-art\n\n" | git credential-osxkeychain get | sed '/^password=/d')
if echo "$credential_info" | grep -q "username=shufan-art"; then
  echo "钥匙串里有 shufan-art 的授权记录。"
else
  echo "没有找到 shufan-art 的授权记录。"
  echo "请先双击：首次GitHub授权.command"
  echo ""
  echo "按回车键关闭窗口。"
  read
  exit 1
fi

echo ""
echo "3. 保存本地最新页面..."
git add index.html .nojekyll tests site generate_test.py generate_10_hot_tests.py publish_to_github_pages.py "一键发布.command" "发布诊断.command" "网页上传版/index.html" "网页上传版/test_config.json" "爆款标题测试题库10套.md" 2>/dev/null
if git diff --cached --quiet; then
  echo "没有新的本地改动。"
else
  git commit -m "publish fixed test pages"
fi

echo ""
echo "4. 测试能不能访问 GitHub..."
if git ls-remote origin >/tmp/xiong_github_check.log 2>&1; then
  echo "GitHub 可以访问，授权也通过。"
else
  echo "GitHub 访问失败。下面是失败原因："
  cat /tmp/xiong_github_check.log
  echo ""
  echo "如果看到 Authentication failed：重新运行 首次GitHub授权.command"
  echo "如果看到 Could not resolve host：网络连不上 GitHub，换网络或稍后再试"
  echo "如果看到 403：Token 权限不够，需要重新生成 classic token，并勾选 repo"
  echo ""
  echo "按回车键关闭窗口。"
  read
  exit 1
fi

echo ""
echo "5. 强制发布本地最终版..."
if git push -u origin main --force >/tmp/xiong_github_push.log 2>&1; then
  echo ""
  echo "发布成功！"
  echo "等 30 秒到 2 分钟后打开："
  echo "https://shufan-art.github.io/shufan/"
else
  echo ""
  echo "发布失败。下面是失败原因："
  cat /tmp/xiong_github_push.log
  echo ""
  echo "如果看到 Authentication failed：重新运行 首次GitHub授权.command"
  echo "如果看到 Could not resolve host：网络连不上 GitHub"
  echo "如果看到 403 或 Permission：Token 没有 repo 权限，或账号不是 shufan-art"
fi

echo ""
echo "按回车键关闭窗口。"
read
