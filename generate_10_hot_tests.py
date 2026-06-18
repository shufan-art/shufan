from pathlib import Path
import json
import re

from generate_test import OUTPUT_DIR, render_html


BASE_DIR = Path(__file__).parent
SOURCE = BASE_DIR / "爆款标题测试题库10套.md"


TEST_META = [
    {
        "slug": "hard-or-change",
        "title": "你该继续硬撑，还是换一种活法？",
        "eyebrow": "LIFE RESET CHECK",
        "subtitle": "30 道题，看清你现在是该坚持，还是该转向",
        "style": "neutral-pace",
        "dimensions": ["能量状态", "方向适配", "现实压力", "转向勇气"],
        "share_line": "不是所有坚持都叫成长，有些只是太久没有听见自己。",
        "intro_paragraphs": [
            "你有没有过这种感觉：每天都在往前走，却越来越不像自己。",
            "你说服自己再坚持一下，可身体和情绪已经开始悄悄提醒你。",
            "这个测试会帮你分清：你是在真正深耕，还是在硬撑一段不适合的生活。",
        ],
        "value_statement": "这个测试会从能量状态、方向适配、现实压力、转向勇气四个维度，帮你判断：你现在更适合继续撑住，还是换一种活法。",
        "category": "life",
    },
    {
        "slug": "be-controlled",
        "title": "你会被哪种人反复拿捏？",
        "eyebrow": "RELATIONSHIP BLIND SPOT",
        "subtitle": "30 道题，看清你最容易在哪种关系里失去判断",
        "style": "soft-love",
        "dimensions": ["情绪牵引", "上头模式", "边界感", "安全感需求"],
        "share_line": "真正让你被拿捏的，往往不是对方多厉害，而是你太想被坚定选择。",
        "intro_paragraphs": [
            "有些人一出现，你就很难保持原来的节奏。",
            "你明知道对方忽冷忽热，却还是忍不住想确认自己是不是特别的那个。",
            "这个测试会帮你看清：你到底容易被哪种人、哪种关系模式反复牵动。",
        ],
        "value_statement": "这个测试会从情绪牵引、上头模式、边界感、安全感需求四个维度，帮你判断你最容易被哪类人拿捏。",
        "category": "love",
    },
    {
        "slug": "sensitive-type",
        "title": "你是哪种高敏感体质？",
        "eyebrow": "SENSITIVE ENERGY MAP",
        "subtitle": "30 道题，看懂你的敏感不是缺点，而是哪种天赋",
        "style": "soft-love",
        "dimensions": ["情绪感知", "环境感官", "关系共情", "边界恢复"],
        "share_line": "敏感不是麻烦，它只是提醒你：你的感受系统比别人更细。",
        "intro_paragraphs": [
            "你是不是经常因为一句话、一个眼神、一个氛围变化想很久？",
            "别人觉得没什么的细节，你却能很快捕捉到不对劲。",
            "这个测试会帮你分辨：你的高敏感更偏情绪、环境、关系，还是自我保护。",
        ],
        "value_statement": "这个测试会从情绪感知、环境感官、关系共情、边界恢复四个维度，帮你看懂自己的敏感类型。",
        "category": "sensitive",
    },
    {
        "slug": "hot-or-steady-love",
        "title": "你适合被热烈追求，还是被稳定陪伴？",
        "eyebrow": "LOVE NEEDS CHECK",
        "subtitle": "30 道题，看清你真正需要哪一种爱",
        "style": "soft-love",
        "dimensions": ["心动浓度", "陪伴需求", "安全感", "个人空间"],
        "share_line": "有人适合点燃你，有人适合安放你，关键是你真正需要哪一种。",
        "intro_paragraphs": [
            "热烈的喜欢很动人，稳定的陪伴也很珍贵。",
            "但不是每个人都适合高浓度的爱，也不是每个人都能在平淡里安心。",
            "这个测试会帮你看清：你更适合被热烈追求，还是被稳定陪伴。",
        ],
        "value_statement": "这个测试会从心动浓度、陪伴需求、安全感、个人空间四个维度，帮你判断你真正适合的爱。",
        "category": "love",
    },
    {
        "slug": "money-talent",
        "title": "一分钟测出你天生适合靠什么赚钱！",
        "eyebrow": "MONEY TALENT CHECK",
        "subtitle": "30 道题，看见你最容易变现的能力",
        "style": "neutral-pace",
        "dimensions": ["表达能力", "服务能力", "资源整合", "产品化能力"],
        "share_line": "你不是没有赚钱能力，只是可能还没把最轻松的能力放到正确位置。",
        "intro_paragraphs": [
            "很多人不是赚不到钱，而是不知道自己最适合靠什么赚钱。",
            "有的人适合内容表达，有的人适合服务陪伴，有的人适合整合资源，有的人适合把技能产品化。",
            "这个测试会帮你看见：你最值得放大的赚钱能力是什么。",
        ],
        "value_statement": "这个测试会从表达能力、服务能力、资源整合、产品化能力四个维度，帮你找到更适合自己的变现方向。",
        "category": "money",
    },
    {
        "slug": "life-script",
        "title": "你的性格已经替你选好了人生剧本！",
        "eyebrow": "LIFE SCRIPT MAP",
        "subtitle": "30 道题，看清你的性格正在把你带向哪里",
        "style": "neutral-pace",
        "dimensions": ["选择模式", "关系模式", "成长路径", "人生主线"],
        "share_line": "你的性格不是限制，它只是一直在替你选择熟悉的剧情。",
        "intro_paragraphs": [
            "你有没有发现，人生里有些情节会反复出现。",
            "相似的人、相似的选择、相似的卡点，总会把你带回熟悉的位置。",
            "这个测试会帮你看清：你的性格正在替你写下哪一种人生剧本。",
        ],
        "value_statement": "这个测试会从选择模式、关系模式、成长路径、人生主线四个维度，帮你看懂自己的性格剧本。",
        "category": "life",
    },
    {
        "slug": "wrong-person",
        "title": "测一测，你和哪类人注定走不长久！",
        "eyebrow": "RELATIONSHIP FIT CHECK",
        "subtitle": "30 道题，看清你最不适合消耗在哪类关系里",
        "style": "soft-love",
        "dimensions": ["相处边界", "沟通方式", "情绪消耗", "长期适配"],
        "share_line": "合适不是靠忍出来的，不合适也常常早有信号。",
        "intro_paragraphs": [
            "有些人不是不好，只是不适合你。",
            "你越努力磨合，越容易把自己变得不像自己。",
            "这个测试会帮你看清：你和哪类人最容易走不长久，也最容易被消耗。",
        ],
        "value_statement": "这个测试会从相处边界、沟通方式、情绪消耗、长期适配四个维度，帮你识别不适合你的关系类型。",
        "category": "love",
    },
    {
        "slug": "strong-or-growth-love",
        "title": "你适合强者恋爱，还是养成系恋爱？",
        "eyebrow": "LOVE ROLE CHECK",
        "subtitle": "30 道题，看清你在关系里更适合被托举，还是一起升级",
        "style": "soft-love",
        "dimensions": ["崇拜感", "参与感", "成长耐心", "关系平衡"],
        "share_line": "强者恋爱和养成系恋爱没有高低，只有适不适合你。",
        "intro_paragraphs": [
            "你是更容易被成熟强大的人吸引，还是会心动于一个人的潜力？",
            "有些关系让你安心，有些关系让你觉得自己很重要。",
            "这个测试会帮你看清：你更适合强者恋爱，还是养成系恋爱。",
        ],
        "value_statement": "这个测试会从崇拜感、参与感、成长耐心、关系平衡四个维度，帮你判断适合你的恋爱模式。",
        "category": "love",
    },
    {
        "slug": "like-signals",
        "title": "真正喜欢你的人，其实早有信号",
        "eyebrow": "LIKE SIGNAL CHECK",
        "subtitle": "30 道题，帮你分清好感、暧昧和真正喜欢",
        "style": "soft-love",
        "dimensions": ["语言表达", "持续行动", "稳定回应", "关系诚意"],
        "share_line": "真正喜欢你的人，不会只给你上头，也会给你安心。",
        "intro_paragraphs": [
            "你有没有分不清，对方是喜欢你，还是只是刚好会聊天？",
            "暧昧有时候很像喜欢，但真正的喜欢通常会有更稳定的信号。",
            "这个测试会帮你判断：你最容易相信哪些信号，又最容易忽略哪些细节。",
        ],
        "value_statement": "这个测试会从语言表达、持续行动、稳定回应、关系诚意四个维度，帮你看懂真正喜欢的信号。",
        "category": "love",
    },
    {
        "slug": "love-clarity",
        "title": "你的恋爱清醒度到了第几级？",
        "eyebrow": "LOVE CLARITY LEVEL",
        "subtitle": "30 道题，看清你在爱情里到底有多清醒",
        "style": "soft-love",
        "dimensions": ["边界感", "判断力", "自我价值", "及时止损"],
        "share_line": "恋爱清醒不是不心动，而是心动时也没有弄丢自己。",
        "intro_paragraphs": [
            "喜欢一个人之后，你还能不能守住自己的节奏？",
            "你能不能分清心动、执念、合适和长期可靠？",
            "这个测试会帮你看清：你的恋爱清醒度到了第几级。",
        ],
        "value_statement": "这个测试会从边界感、判断力、自我价值、及时止损四个维度，帮你判断你的恋爱清醒度。",
        "category": "love",
    },
]


OPTION_BANKS = {
    "life": [
        ("我会先撑住，确保现实不失控", "A"),
        ("我想换个方式，重新找回主动权", "B"),
        ("我需要先恢复状态，再做决定", "C"),
        ("我会重新规划，做一个低风险尝试", "D"),
    ],
    "love": [
        ("我很容易被情绪和回应牵动", "A"),
        ("我更在意稳定、确定和被放在心上", "B"),
        ("我会先观察边界和长期适配", "C"),
        ("我需要先确认自己舒服不舒服", "D"),
    ],
    "sensitive": [
        ("我最容易捕捉到情绪变化", "A"),
        ("我对环境和细节特别敏感", "B"),
        ("我很容易共情，也容易被影响", "C"),
        ("我需要边界和独处来恢复自己", "D"),
    ],
    "money": [
        ("我适合靠表达、内容和影响力放大价值", "A"),
        ("我适合靠服务、陪伴和解决具体问题变现", "B"),
        ("我适合靠资源整合、信息差和链接机会赚钱", "C"),
        ("我适合把技能、经验或审美做成产品", "D"),
    ],
}


RESULTS = {
    "life": {
        "A": ("稳定硬撑型", "你很能扛，也很重视现实安全感。", "你的优势是靠谱、负责、能坚持，但你也容易把“不能停”误认为“还适合”。接下来最重要的是确认：这份坚持有没有真实反馈。"),
        "B": ("转向重启型", "你内心已经开始渴望新的活法。", "你不是冲动，而是已经感觉到旧节奏不再适配。适合先做低成本试错，给自己一个小入口，而不是立刻推翻全部生活。"),
        "C": ("能量修复型", "你现在最需要的不是答案，而是把状态补回来。", "当人太累时，任何选择都会看起来很难。你适合先减少消耗，恢复一点掌控感，再判断要继续还是转向。"),
        "D": ("清醒规划型", "你适合用更聪明的方式调整人生节奏。", "你并不想盲目放弃，也不想一直硬撑。你真正需要的是计划、边界和一个可验证的小行动。"),
    },
    "love": {
        "A": ("情绪上头型", "你很容易被对方的回应、距离和态度牵动。", "你的喜欢很真，也很投入，但要小心把不确定感当成心动。真正适合你的关系，不该让你一直猜。"),
        "B": ("稳定安全型", "你最需要的是被认真对待和稳定放在心上。", "你适合长期、清晰、有行动感的关系。比起刺激，你更需要一个说到做到、持续回应你的人。"),
        "C": ("清醒观察型", "你会心动，但也会看这个人值不值得长期相处。", "你的判断力是优势。只是别让过度理性把真实感受全部压掉，合适也需要一点松弛和靠近。"),
        "D": ("自我边界型", "你正在学会把注意力从对方身上收回自己。", "你真正需要的关系，是让你更像自己，而不是一直委屈、讨好、证明。你的边界感会帮你筛掉不适合的人。"),
    },
    "sensitive": {
        "A": ("情绪雷达型", "你能很快察觉别人语气和情绪的变化。", "你的感受力很细，但不要把所有变化都自动归因到自己身上。学会区分别人的情绪和你的责任，会让你轻松很多。"),
        "B": ("环境感官型", "你对声音、光线、气味和空间氛围特别敏锐。", "你需要更稳定、舒服的环境来保存能量。对你来说，减少刺激不是矫情，而是有效管理自己。"),
        "C": ("共情吸收型", "你很容易理解别人，也容易把别人的情绪带回自己身上。", "你的温柔是能力，但需要边界保护。不是每一种痛苦都需要你亲自承接。"),
        "D": ("边界恢复型", "你敏感，但也正在发展自我保护能力。", "你最适合先建立恢复系统，比如独处、书写、减少无效社交。你的敏感会在边界里变成天赋。"),
    },
    "money": {
        "A": ("内容表达型", "你适合靠表达、观点、审美或内容影响力赚钱。", "你需要把自己的经验和观察稳定输出。低价产品、测评、咨询入口、内容账号都适合作为起步方式。"),
        "B": ("服务陪伴型", "你适合靠解决具体问题和提供陪伴型服务变现。", "你的价值在于让别人感觉被理解、被带着走。适合做咨询、陪跑、社群服务或细分人群方案。"),
        "C": ("资源整合型", "你适合靠信息差、链接能力和项目协作赚钱。", "你不一定要亲自做所有事，但你要学会发现需求、组织资源、促成成交。"),
        "D": ("技能产品型", "你适合把技能、方法或经验打包成可重复交付的产品。", "你的优势在于把复杂东西整理清楚。适合做模板、工具包、课程、小程序或标准化服务。"),
    },
}


def parse_sections():
    text = SOURCE.read_text(encoding="utf-8")
    sections = []
    current = None
    for line in text.splitlines():
        header = re.match(r"^##\s+\d+\.\s+(.+)$", line)
        question = re.match(r"^\d+\.\s+(.+)$", line)
        if header:
            current = {"title": header.group(1).strip(), "questions": []}
            sections.append(current)
        elif question and current is not None:
            current["questions"].append(question.group(1).strip())
    return sections


def build_questions(lines, category):
    options = OPTION_BANKS[category]
    return [
        {
            "text": line,
            "options": [{"text": text, "type": option_type} for text, option_type in options],
        }
        for line in lines[:30]
    ]


def build_results(category):
    result = {}
    for key, (name, summary, section) in RESULTS[category].items():
        result[key] = {
            "name": name,
            "summary": summary,
            "sections": [
                section,
                "你可以把这个结果当成一个提醒：不是给自己贴标签，而是看清现在最值得调整的地方。",
                "接下来 7 天，选一个最小行动去验证它。真正有用的测试，不是让你立刻改变人生，而是让你更愿意靠近自己。",
            ],
        }
    return result


def build_config(meta, question_lines):
    category = meta["category"]
    return {
        "slug": meta["slug"],
        "theme": meta["title"],
        "eyebrow": meta["eyebrow"],
        "title": meta["title"],
        "subtitle": meta["subtitle"],
        "subtitle_lines": [
            meta["subtitle"],
            "不用纠结标准答案，凭第一感觉选就好。",
        ],
        "price_hint": "娱乐测试，仅供自我探索参考，不构成心理或职业诊断。",
        "intro": meta["intro_paragraphs"][0],
        "intro_paragraphs": meta["intro_paragraphs"],
        "value_statement": meta["value_statement"],
        "dimensions": meta["dimensions"],
        "style": meta["style"],
        "share_line": meta["share_line"],
        "questions": build_questions(question_lines, category),
        "results": build_results(category),
    }


def normalize_title(title):
    title = title.replace("测一测，", "").replace("一分钟测出", "")
    return re.sub(r"[\s，,？?！!、：:]", "", title)


def main():
    sections = parse_sections()
    by_title = {section["title"]: section["questions"] for section in sections}
    generated = []
    for meta in TEST_META:
        question_lines = by_title.get(meta["title"])
        if question_lines is None:
            wanted = normalize_title(meta["title"])
            for source_title, source_questions in by_title.items():
                source = normalize_title(source_title)
                if source.startswith(wanted) or wanted in source or source in wanted:
                    question_lines = source_questions
                    break
        if not question_lines or len(question_lines) < 30:
            raise RuntimeError(f"题目不足 30 道：{meta['title']}")
        config = build_config(meta, question_lines)
        page_dir = OUTPUT_DIR / meta["slug"]
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "test_config.json").write_text(
            json.dumps(config, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        (page_dir / "index.html").write_text(render_html(config), encoding="utf-8")
        generated.append(meta["slug"])

    print("已生成 10 套测试：")
    for slug in generated:
        print(f"- {slug}")


if __name__ == "__main__":
    main()
