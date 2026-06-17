from pathlib import Path
from datetime import datetime
import html
import json
import re
import sys


BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"


def safe_slug(text):
    text = re.sub(r"[\\/:*?\"<>|#%&{}$!'@+`=]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    return text[:40] or "test"


def build_questions(theme):
    templates = [
        "当你想到「{theme}」时，你第一反应更接近哪一种？",
        "如果现在必须做一个选择，你更看重什么？",
        "遇到不确定的时候，你通常会怎么处理？",
        "别人眼里的你，更像下面哪一种？",
        "你最容易在哪个地方卡住？",
        "你真正想要的状态，更接近哪一种？",
        "如果给你一次重新选择的机会，你会优先改变什么？",
        "你最害怕的结果是什么？",
        "你身上最稳定的优势是什么？",
        "你最容易被哪句话打动？",
        "你现在最需要补上的能力是什么？",
        "当别人催你做决定时，你会怎么反应？",
        "你更相信哪一种成长方式？",
        "你最想摆脱的状态是什么？",
        "如果未来三个月有一个突破，你希望它发生在哪里？",
        "做完这个测试后，你最想获得什么答案？",
    ]

    options = [
        [
            "先稳定下来，再慢慢优化",
            "想换一种活法，重新打开可能性",
            "有点焦虑，但不知道该从哪里开始",
            "希望有人帮我看清自己的真实方向",
        ],
        [
            "安全感和确定性",
            "自由度和成长空间",
            "短期回报和现实压力",
            "内心感受和长期适配",
        ],
        [
            "先观察，不轻易行动",
            "先试试看，在行动里找答案",
            "反复纠结，怕选错",
            "找人分析，希望获得外部确认",
        ],
        [
            "靠谱、稳定、能坚持",
            "有想法、不甘心、想突破",
            "敏感、想很多、容易内耗",
            "温柔、有感受力、容易共情",
        ],
        [
            "不敢轻易离开熟悉环境",
            "想法很多，但落地不够",
            "容易被情绪影响判断",
            "太在意别人的评价",
        ],
        [
            "稳定、有节奏、少消耗",
            "自由、有选择、有成长",
            "不再焦虑，能安心往前走",
            "被理解，也更理解自己",
        ],
        [
            "改变自己的节奏",
            "改变自己的圈子",
            "改变自己的行动方式",
            "改变自己看待问题的角度",
        ],
        [
            "努力很久但没有变化",
            "明明有潜力却一直困住",
            "选错方向浪费时间",
            "没有人真正懂我",
        ],
        [
            "耐心和执行力",
            "好奇心和创造力",
            "感知力和反思力",
            "共情力和连接力",
        ],
        [
            "你已经走得很稳了",
            "你可以拥有更大的可能性",
            "你不是不行，只是太累了",
            "你需要的不是答案，而是看见自己",
        ],
        [
            "持续深耕的能力",
            "快速试错的能力",
            "情绪复原的能力",
            "清晰表达自己的能力",
        ],
        [
            "先拖一拖，等想清楚",
            "直接做一个小尝试",
            "更焦虑，担心被推着走",
            "想听听可信的人怎么说",
        ],
        [
            "慢慢积累，长期主义",
            "主动出击，边做边调",
            "先修复状态，再谈突破",
            "先理解自己，再选择方向",
        ],
        [
            "重复但没成长",
            "想做但不敢做",
            "一直焦虑停不下来",
            "总是被别人的期待拉走",
        ],
        [
            "工作和收入",
            "自由和选择",
            "情绪和状态",
            "关系和自我认同",
        ],
        [
            "我现在最适合怎么走",
            "我还有哪些可能性",
            "我为什么总是卡住",
            "我到底是哪一种人",
        ],
    ]

    questions = []
    for index, template in enumerate(templates):
        questions.append(
            {
                "text": template.format(theme=theme),
                "options": [
                    {"text": options[index][0], "type": "A"},
                    {"text": options[index][1], "type": "B"},
                    {"text": options[index][2], "type": "C"},
                    {"text": options[index][3], "type": "D"},
                ],
            }
        )
    return questions


def build_results(theme):
    return {
        "A": {
            "name": "稳定深耕型",
            "summary": f"你面对「{theme}」时，更需要的是稳定节奏和清晰路径。",
            "sections": [
                "你不是没有想法，而是更适合在确定感里慢慢发力。你擅长把一件事持续做深，也更容易在长期积累里看到结果。",
                "你的优势是靠谱、能坚持、抗波动能力强。只要方向选对，你不需要频繁折腾，也能慢慢做出自己的成绩。",
                "你的卡点是容易为了安全感牺牲真实需求。未来 7 天，你可以先列出一件最值得深耕的小事，并给它安排一个固定行动时间。",
            ],
        },
        "B": {
            "name": "自由探索型",
            "summary": f"你面对「{theme}」时，真正想要的是更大的空间和更多选择。",
            "sections": [
                "你心里有很强的探索欲，不太适合一直待在完全固定的轨道里。你需要通过尝试来确认自己，而不是只靠想象做决定。",
                "你的优势是敏锐、有想法、愿意看见新机会。只要给自己一个低成本试错的入口，你会比想象中更快找到方向。",
                "你的卡点是容易想太多、启动太慢。未来 7 天，请做一个最小尝试：发一条内容、问一个人、做一个小作品，先让事情动起来。",
            ],
        },
        "C": {
            "name": "能量修复型",
            "summary": f"你面对「{theme}」时，最先需要处理的不是选择，而是状态。",
            "sections": [
                "你不是不努力，也不是没有能力，只是现在可能被压力和消耗占据了太多注意力。你需要先把能量补回来，判断才会更清楚。",
                "你的优势是感受细腻、复盘能力强，能够从经历里提炼出很深的东西。只要状态恢复，你会重新拥有行动力。",
                "你的卡点是容易把暂时的低能量误判成自己不行。未来 7 天，请先减少一个消耗源，再完成一件很小但能带来掌控感的事。",
            ],
        },
        "D": {
            "name": "自我看见型",
            "summary": f"你面对「{theme}」时，最想要的是被理解，也更清楚地理解自己。",
            "sections": [
                "你很在意内在感受，也容易从细节里捕捉到别人忽略的信息。你适合先弄清楚自己真正想要什么，再去做具体选择。",
                "你的优势是共情力、表达力和觉察力。你适合把自己的经历、观察、感受整理出来，它们可能会成为你连接他人的能力。",
                "你的卡点是容易被外界评价带偏。未来 7 天，请写下 3 个你真正想要的关键词，不解释给别人听，先自己承认它们。",
            ],
        },
    }


def build_config(theme):
    return {
        "theme": theme,
        "title": theme,
        "subtitle": "16 道题，看见你的隐藏倾向和下一步方向",
        "price_hint": "娱乐测试，仅供自我探索参考",
        "questions": build_questions(theme),
        "results": build_results(theme),
    }


def render_html(config):
    data = json.dumps(config, ensure_ascii=False)
    title = html.escape(config["title"])
    subtitle = html.escape(config["subtitle"])
    price_hint = html.escape(config["price_hint"])
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
      color: #2b211d;
      background: #fff8f2;
      line-height: 1.7;
    }}
    .page {{
      width: min(760px, 100%);
      margin: 0 auto;
      padding: 22px 16px 48px;
    }}
    .hero {{
      padding: 28px 0 18px;
    }}
    .tag {{
      display: inline-block;
      padding: 4px 10px;
      border-radius: 999px;
      background: #ffe2cc;
      color: #8a3d12;
      font-size: 13px;
      margin-bottom: 14px;
    }}
    h1 {{
      margin: 0;
      font-size: 30px;
      line-height: 1.25;
      letter-spacing: 0;
    }}
    .subtitle {{
      margin: 12px 0 0;
      color: #6d5a50;
      font-size: 16px;
    }}
    .panel {{
      background: #fff;
      border: 1px solid #f0d8c7;
      border-radius: 8px;
      padding: 18px;
      box-shadow: 0 8px 24px rgba(112, 65, 32, 0.08);
    }}
    .notice {{
      margin: 14px 0 0;
      color: #85624e;
      font-size: 13px;
    }}
    .progress {{
      height: 8px;
      background: #f6e6db;
      border-radius: 999px;
      overflow: hidden;
      margin: 18px 0;
    }}
    .bar {{
      height: 100%;
      width: 0;
      background: #dc6b2f;
      transition: width .25s ease;
    }}
    .question-count {{
      color: #8a6a58;
      font-size: 14px;
      margin-bottom: 8px;
    }}
    .question {{
      font-size: 20px;
      font-weight: 700;
      margin-bottom: 16px;
    }}
    .option {{
      width: 100%;
      text-align: left;
      border: 1px solid #eed6c5;
      background: #fffaf6;
      color: #2b211d;
      padding: 14px 14px;
      border-radius: 8px;
      margin: 10px 0;
      font-size: 16px;
      cursor: pointer;
    }}
    .option:hover {{
      border-color: #dc6b2f;
      background: #fff1e6;
    }}
    .actions {{
      display: flex;
      gap: 10px;
      margin-top: 16px;
    }}
    button.primary, button.secondary {{
      border: 0;
      border-radius: 8px;
      padding: 12px 16px;
      font-size: 16px;
      cursor: pointer;
    }}
    .primary {{
      background: #dc6b2f;
      color: white;
      width: 100%;
    }}
    .secondary {{
      background: #f4e5d9;
      color: #5b3a27;
    }}
    .result-title {{
      font-size: 24px;
      font-weight: 800;
      margin: 4px 0 8px;
    }}
    .result-summary {{
      color: #6d4a36;
      font-weight: 700;
      margin-bottom: 16px;
    }}
    .result-section {{
      border-top: 1px solid #f1ded0;
      padding-top: 14px;
      margin-top: 14px;
    }}
    .share {{
      background: #fff3e9;
      border-left: 4px solid #dc6b2f;
      padding: 12px;
      border-radius: 6px;
      margin-top: 18px;
    }}
    .hidden {{ display: none; }}
    .footer {{
      text-align: center;
      color: #9a8171;
      font-size: 12px;
      margin-top: 20px;
    }}
  </style>
</head>
<body>
  <main class="page">
    <section class="hero">
      <span class="tag">自我探索测试</span>
      <h1>{title}</h1>
      <p class="subtitle">{subtitle}</p>
      <p class="notice">{price_hint}</p>
    </section>

    <section id="start" class="panel">
      <p>这个测试会通过 16 个选择题，帮你看见自己更接近哪一种状态。</p>
      <p>不用纠结标准答案，凭第一感觉选就好。</p>
      <button class="primary" onclick="startTest()">开始测试</button>
    </section>

    <section id="quiz" class="panel hidden">
      <div class="question-count" id="count"></div>
      <div class="progress"><div class="bar" id="bar"></div></div>
      <div class="question" id="question"></div>
      <div id="options"></div>
      <div class="actions">
        <button class="secondary" onclick="goBack()">上一题</button>
      </div>
    </section>

    <section id="result" class="panel hidden"></section>

    <div class="footer">生成时间：{generated_at}</div>
  </main>

  <script>
    const TEST = {data};
    let current = 0;
    let answers = [];

    function show(id) {{
      document.getElementById("start").classList.add("hidden");
      document.getElementById("quiz").classList.add("hidden");
      document.getElementById("result").classList.add("hidden");
      document.getElementById(id).classList.remove("hidden");
    }}

    function startTest() {{
      current = 0;
      answers = [];
      show("quiz");
      renderQuestion();
    }}

    function renderQuestion() {{
      const q = TEST.questions[current];
      document.getElementById("count").textContent = `第 ${{current + 1}} / ${{TEST.questions.length}} 题`;
      document.getElementById("bar").style.width = `${{(current / TEST.questions.length) * 100}}%`;
      document.getElementById("question").textContent = q.text;
      document.getElementById("options").innerHTML = q.options.map((opt, index) => `
        <button class="option" onclick="chooseOption('${{opt.type}}')">${{String.fromCharCode(65 + index)}}. ${{opt.text}}</button>
      `).join("");
    }}

    function chooseOption(type) {{
      answers[current] = type;
      if (current < TEST.questions.length - 1) {{
        current += 1;
        renderQuestion();
      }} else {{
        showResult();
      }}
    }}

    function goBack() {{
      if (current === 0) {{
        show("start");
        return;
      }}
      current -= 1;
      renderQuestion();
    }}

    function showResult() {{
      const scores = {{ A: 0, B: 0, C: 0, D: 0 }};
      answers.forEach(type => scores[type] += 1);
      const winner = Object.keys(scores).sort((a, b) => scores[b] - scores[a])[0];
      const result = TEST.results[winner];
      document.getElementById("bar").style.width = "100%";
      document.getElementById("result").innerHTML = `
        <div class="question-count">你的测试结果</div>
        <div class="result-title">${{result.name}}</div>
        <div class="result-summary">${{result.summary}}</div>
        ${{result.sections.map(section => `<div class="result-section">${{section}}</div>`).join("")}}
        <div class="share">适合截图分享的一句话：你不是没有答案，只是需要一个更适合自己的方向。</div>
        <div class="actions">
          <button class="primary" onclick="startTest()">重新测试</button>
        </div>
      `;
      show("result");
    }}
  </script>
</body>
</html>
"""


def main():
    if len(sys.argv) < 2:
        theme = "你适合稳定上班，还是自由赚钱？"
    else:
        theme = " ".join(sys.argv[1:]).strip()

    config = build_config(theme)
    slug = safe_slug(theme)
    page_dir = OUTPUT_DIR / slug
    page_dir.mkdir(parents=True, exist_ok=True)

    config_path = page_dir / "test_config.json"
    html_path = page_dir / "index.html"
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    html_path.write_text(render_html(config), encoding="utf-8")

    print("生成完成")
    print(f"主题：{theme}")
    print(f"网页：{html_path}")
    print(f"配置：{config_path}")


if __name__ == "__main__":
    main()
