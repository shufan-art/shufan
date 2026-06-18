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

if [[ "$username" == ghp_* || "$username" == github_pat_* ]]; then
  echo ""
  echo "你把 Token 粘到了用户名这里。"
  echo "请关闭窗口，重新运行本脚本。"
  echo "用户名这里应该填：shufan-art"
  echo "Token 要粘贴到下一步的 Token 输入框。"
  echo ""
  echo "按回车键关闭窗口。"
  read
  exit 1
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

printf "protocol=https\nhost=github.com\nusername=%s\n\n" "$username" | git credential-osxkeychain erase
printf "protocol=https\nhost=github.com\n\n" | git credential-osxkeychain erase
printf "protocol=https\nhost=github.com\nusername=%s\npassword=%s\n\n" "$username" "$token" | git credential-osxkeychain store
git remote set-url origin "https://${username}@github.com/shufan-art/shufan.git"

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
