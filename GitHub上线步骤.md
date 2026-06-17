# GitHub Pages 上线步骤

这个方案适合你说的 “git”。

## 一、生成网页

先生成一个测试网页：

```bash
python3 generate_test.py "你适合稳定上班，还是自由赚钱？"
```

## 二、整理成 GitHub Pages 目录

运行：

```bash
python3 publish_to_github_pages.py
```

运行后会生成：

```text
docs/index.html
docs/tests/测试主题/index.html
```

GitHub Pages 可以直接发布 `docs` 文件夹。

## 三、上传到 GitHub

第一次使用时：

```bash
git init
git add .
git commit -m "init test pages"
git branch -M main
git remote add origin 你的GitHub仓库地址
git push -u origin main
```

后面每次更新：

```bash
git add .
git commit -m "add new test"
git push
```

## 四、打开 GitHub Pages

进入 GitHub 仓库：

1. Settings
2. Pages
3. Source 选择 `Deploy from a branch`
4. Branch 选择 `main`
5. Folder 选择 `/docs`
6. Save

几分钟后，GitHub 会给你一个访问链接。

## 五、以后完整流程

以后你只需要：

```bash
python3 generate_test.py "新的测试主题"
python3 publish_to_github_pages.py
git add .
git commit -m "add new test"
git push
```

然后新测试就会上线。

