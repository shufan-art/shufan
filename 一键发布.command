#!/bin/zsh
cd "$(dirname "$0")"

echo "开始一键发布..."
echo "目标网站：https://shufan-art.github.io/shufan/"
echo ""

python3 publish_to_github_pages.py

if [ -d "site" ]; then
  cp -R site/. .
fi

git remote set-url origin "https://github.com/shufan-art/shufan.git"

git add index.html .nojekyll tests generate_test.py publish_to_github_pages.py "网页上传版/index.html" "网页上传版/test_config.json" 2>/dev/null

if git diff --cached --quiet; then
  echo "没有发现新的网页改动，准备直接推送当前版本。"
else
  git commit -m "publish test page"
fi

echo ""
echo "正在上传到 GitHub..."
echo ""

git fetch origin main >/dev/null 2>&1 || true

if git push -u origin main --force-with-lease; then
  echo ""
  echo "发布成功！"
  echo "等 30 秒到 2 分钟后打开："
  echo "https://shufan-art.github.io/shufan/"
else
  echo ""
  echo "发布失败。"
  echo "如果提示 Authentication failed，请先双击 首次GitHub授权.command。"
fi

echo ""
echo "按回车键关闭窗口。"
read
