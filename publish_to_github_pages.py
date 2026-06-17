from pathlib import Path
from datetime import datetime
import html
import shutil


BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
DOCS_DIR = BASE_DIR / "docs"
TESTS_DIR = DOCS_DIR / "tests"


def find_tests():
    if not OUTPUT_DIR.exists():
        return []
    tests = []
    for folder in sorted(OUTPUT_DIR.iterdir()):
        index_file = folder / "index.html"
        config_file = folder / "test_config.json"
        if folder.is_dir() and index_file.exists() and config_file.exists():
            tests.append(folder)
    return tests


def copy_tests(test_folders):
    TESTS_DIR.mkdir(parents=True, exist_ok=True)
    published = []
    for folder in test_folders:
        target = TESTS_DIR / folder.name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(folder, target)
        published.append(
            {
                "name": folder.name,
                "path": f"tests/{folder.name}/index.html",
            }
        )
    return published


def build_homepage(published):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    links = "\n".join(
        f'<a class="card" href="{html.escape(item["path"])}">{html.escape(item["name"])}</a>'
        for item in published
    )
    if not links:
        links = '<div class="empty">还没有生成测试页。</div>'

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>自我探索测试</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
      background: #fff8f2;
      color: #2b211d;
      line-height: 1.7;
    }}
    main {{
      width: min(820px, 100%);
      margin: 0 auto;
      padding: 36px 18px 56px;
    }}
    h1 {{
      margin: 0 0 10px;
      font-size: 30px;
      line-height: 1.25;
      letter-spacing: 0;
    }}
    .intro {{
      margin: 0 0 24px;
      color: #6d5a50;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 14px;
    }}
    .card {{
      display: block;
      padding: 16px;
      border: 1px solid #f0d8c7;
      border-radius: 8px;
      background: #fff;
      color: #2b211d;
      text-decoration: none;
      box-shadow: 0 8px 24px rgba(112, 65, 32, 0.08);
    }}
    .card:hover {{
      border-color: #dc6b2f;
      background: #fff3e9;
    }}
    .empty {{
      padding: 18px;
      border-radius: 8px;
      background: #fff;
      color: #8a6a58;
    }}
    footer {{
      margin-top: 28px;
      color: #9a8171;
      font-size: 12px;
      text-align: center;
    }}
  </style>
</head>
<body>
  <main>
    <h1>自我探索测试</h1>
    <p class="intro">选择一个测试，换个角度理解自己。测试仅供娱乐和自我探索参考。</p>
    <section class="grid">
      {links}
    </section>
    <footer>更新时间：{now}</footer>
  </main>
</body>
</html>
"""


def main():
    test_folders = find_tests()
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    published = copy_tests(test_folders)
    (DOCS_DIR / "index.html").write_text(build_homepage(published), encoding="utf-8")
    (DOCS_DIR / ".nojekyll").write_text("", encoding="utf-8")

    print("GitHub Pages 文件已生成")
    print(f"发布目录：{DOCS_DIR}")
    print(f"测试页数量：{len(published)}")
    print("下一步：把通用测试壳文件夹推到 GitHub，然后在 GitHub Pages 里选择 docs 目录发布。")


if __name__ == "__main__":
    main()
