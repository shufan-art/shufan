#!/bin/zsh
cd "$(dirname "$0")"

echo "首次 GitHub 授权"
echo ""
echo "只需要做一次。以后发布网页就不用再输入账号密码。"
echo ""
echo "请先在浏览器打开这个页面创建 Token："
echo "https://github.com/settings/tokens"
echo ""
echo "如果看到 Generate new token，请选择 classic token。"
echo "权限只需要勾选 repo。"
echo ""

printf "GitHub 用户名，直接回车默认 shufan-art："
read username
if [ -z "$username" ]; then
  username="shufan-art"
fi

echo ""
echo "请粘贴 GitHub Token。粘贴时屏幕不会显示，这是正常的。"
printf "Token："
read -s token
echo ""

if [ -z "$token" ]; then
  echo "没有输入 Token，已停止。"
  echo "按回车键关闭窗口。"
  read
  exit 1
fi

printf "protocol=https\nhost=github.com\nusername=%s\npassword=%s\n\n" "$username" "$token" | git credential-osxkeychain store
git remote set-url origin "https://github.com/shufan-art/shufan.git"

echo ""
echo "授权信息已保存到系统钥匙串。"
echo "现在测试能不能访问 GitHub..."
echo ""

if git ls-remote origin >/dev/null 2>&1; then
  echo "成功！以后可以直接双击 一键发布.command。"
else
  echo "测试失败。常见原因：Token 填错、没有勾选 repo 权限，或网络暂时不通。"
fi

echo ""
echo "按回车键关闭窗口。"
read
