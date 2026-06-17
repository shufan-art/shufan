#!/bin/zsh
cd "$(dirname "$0")"

echo "准备推送到 GitHub..."
echo "当前目录：$(pwd)"
echo ""

git status --short --branch
echo ""

git push -u origin main

echo ""
echo "如果上面显示推送成功，就可以去 GitHub 开启 Pages："
echo "Settings -> Pages -> Branch: main -> Folder: /docs -> Save"
echo ""
echo "按回车键关闭窗口。"
read
