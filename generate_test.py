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


def build_love_questions():
    rows = [
        ["你刚认识一个有好感的人，最先被什么打动？", "对方对我特别上心", "对方的气味、声音或外形很吸引我", "相处舒服，不用刻意表现", "对方给我稳定回应"],
        ["你会在什么情况下开始反复想一个人？", "他一点点冷淡，我就开始不安", "见过面后身体记住了那种感觉", "聊天很顺，价值观也接近", "他让我觉得自己被认真对待"],
        ["如果对方突然不回消息，你更可能怎么想？", "是不是我哪里做错了", "会有点想念，但更多是被吊起欲望", "先观察，不急着下结论", "会在意他是不是还可靠"],
        ["你最容易把哪种感觉当成喜欢？", "想一直确认他爱不爱我", "心跳快、上头、想靠近", "相处自然，有共同语言", "被照顾、被保护、很安心"],
        ["你在暧昧期最受不了什么？", "忽冷忽热", "没有身体张力", "聊不到一起", "承诺不清楚"],
        ["你更容易因为哪句话心软？", "我只对你这样", "我很想见你", "我懂你的想法", "我会一直在"],
        ["如果一个人很帅但不稳定，你会？", "容易陷进去，想证明自己特别", "很容易被吸引，先享受当下", "会喜欢，但不会立刻交出自己", "会退后，因为我需要确定感"],
        ["如果一个人条件普通但很稳定，你会？", "如果他很爱我，我会慢慢依赖", "可能不够上头", "看相处质量，不急着否定", "会很加分，稳定让我安心"],
        ["你最常在感情里犯的错是？", "把对方看得太重", "把心动当长期合适", "想太多，启动太慢", "太需要确定答案"],
        ["你最容易被哪种人吸引？", "会给我强烈情绪波动的人", "有性张力、有魅力的人", "成熟、有边界、聊得来的人", "温柔稳定、愿意陪我的人"],
        ["你确认喜欢一个人时，身体反应重要吗？", "重要，但我更在意他爱不爱我", "非常重要，没有反应就很难喜欢", "重要，但不是唯一标准", "有就更好，没有也会看安全感"],
        ["你会因为一个人对你好而喜欢他吗？", "很容易，我会被偏爱打动", "不一定，没吸引力就不行", "可能会，但要看是否真的合拍", "会，稳定的好对我很重要"],
        ["你在关系里最想要什么？", "被坚定选择", "强烈心动和亲密感", "互相理解、共同成长", "稳定陪伴和安全感"],
        ["暧昧最上头的瞬间是什么？", "他突然只对我特殊", "靠近、对视、触碰的瞬间", "发现我们很同频", "他认真回应我的需求"],
        ["你更害怕哪种结局？", "我很爱，但他没那么爱", "热度过了就没感觉", "判断错人浪费时间", "关系不稳定让我消耗"],
        ["朋友说你恋爱脑，你的反应是？", "可能吧，我真的容易陷进去", "我只是容易被吸引，不一定想长期", "我其实很清醒，只是慢热", "我不是恋爱脑，我只是需要安全感"],
        ["你会偷偷研究对方的动态吗？", "会，而且越看越在意", "会看，但更多是确认吸引感", "偶尔看，不会影响节奏", "会看他是否稳定一致"],
        ["如果对方很会撩，你会？", "很容易当真", "很容易被点燃", "会心动，但会看行动", "会开心，但也会看是否靠谱"],
        ["你更相信哪种喜欢？", "离不开、放不下、很在乎", "身体诚实，见面就知道", "舒服自然，越相处越确定", "稳定踏实，不用猜来猜去"],
        ["你会因为孤独进入一段关系吗？", "有可能，我怕没人陪", "如果有吸引力，可能会试试", "不太会，我需要确认合适", "会心动于陪伴，但会看稳定性"],
        ["你最需要提醒自己的是？", "不要把全部情绪交给一个人", "不要把上头误认为真爱", "不要因为太清醒错过感受", "不要用控制换安全感"],
        ["对方哪种行为最让你加分？", "公开偏爱我", "见面有强烈吸引和默契", "尊重我的节奏和想法", "说到做到，稳定出现"],
        ["你分不清喜欢时，通常是因为？", "情绪太满，看不清自己", "身体很想靠近，但心里不确定", "理性和感性在打架", "太想要安全感，容易误判"],
        ["你最容易沉迷哪种关系？", "忽冷忽热但偶尔很甜", "暧昧刺激但不确定", "慢慢了解、越聊越深", "被照顾、被惦记、被保护"],
        ["如果只选一个，你更想要？", "被爱得很明显", "心动得很强烈", "相处得很舒服", "关系很稳定"],
        ["你会把对方幻想得很完美吗？", "会，我容易自动加滤镜", "会被吸引力放大优点", "不太会，我会看真实相处", "会，但我更看他能不能给安全感"],
        ["在喜欢的人面前，你最像哪一种？", "容易患得患失", "容易害羞但很想靠近", "表面淡定，心里观察", "想确认关系是否可靠"],
        ["你更容易在哪个阶段上头？", "对方开始冷下来时", "第一次见面或亲密互动后", "深入聊天之后", "对方持续稳定对我好之后"],
        ["你判断一个人适不适合长期，最看重？", "他是不是足够爱我", "吸引力能不能持续", "三观、沟通和边界", "责任感和稳定性"],
        ["做完这个测试，你最想知道什么？", "我是不是太恋爱脑了", "我是不是只是生理性喜欢", "我到底适合哪种关系", "我为什么总需要安全感"],
    ]
    questions = []
    for row in rows:
        questions.append(
            {
                "text": row[0],
                "options": [
                    {"text": row[1], "type": "A"},
                    {"text": row[2], "type": "B"},
                    {"text": row[3], "type": "C"},
                    {"text": row[4], "type": "D"},
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


def build_love_results(theme):
    return {
        "A": {
            "name": "恋爱脑投入型",
            "summary": "你不是不会爱，而是太容易把一个人放到情绪中心。",
            "sections": [
                "你一旦喜欢上一个人，就很容易把注意力、期待和安全感都放到对方身上。对方一句话、一个眼神、一次回复速度，都可能影响你一整天的状态。",
                "你的可贵之处是很真诚，也很有投入感。你不是随便喜欢，你只是太渴望被坚定选择，所以会把一点点偏爱看得很重。",
                "你需要提醒自己：真正适合你的关系，不应该让你一直猜、一直等、一直证明自己值得被爱。未来 7 天，试着把注意力收回一点，先问自己舒服不舒服。",
            ],
        },
        "B": {
            "name": "生理性喜欢上头型",
            "summary": "你很容易被吸引力点燃，但这不一定等于长期适合。",
            "sections": [
                "你对气味、声音、外形、氛围和亲密张力很敏感。一个人如果刚好踩中你的身体偏好，你会很快产生想靠近、想见面、想继续探索的冲动。",
                "你的优势是感受力很强，不会骗自己。你能很快判断一个人有没有吸引力，这种直觉在关系里很重要。",
                "你需要区分：心动是真的，但心动不等于承诺；上头是真的，但上头不等于合适。未来 7 天，如果你很想靠近一个人，也请同时观察他的稳定性和尊重感。",
            ],
        },
        "C": {
            "name": "清醒慢热型",
            "summary": "你不是不心动，只是比起上头，你更需要确认这个人值不值得。",
            "sections": [
                "你对关系有自己的判断标准，不会因为一点暧昧就立刻交出全部。你可能会心动，但你会一边感受，一边观察对方的边界、沟通和长期适配度。",
                "你的优势是清醒、有分寸，也更不容易被短期情绪带走。你适合慢慢相处，在稳定互动中确认喜欢。",
                "你的卡点是有时太理性，容易错过真实的感受。未来 7 天，除了问这个人合不合适，也问问自己：和他在一起时，我有没有变得更松弛？",
            ],
        },
        "D": {
            "name": "安全感依恋型",
            "summary": "你最在意的不是刺激，而是对方能不能稳定地把你放在心上。",
            "sections": [
                "你在关系里很看重回应、承诺和一致性。比起忽冷忽热的刺激，你更容易被一个人长期、稳定、温柔的行动打动。",
                "你的优势是适合经营长期关系，也懂得珍惜真正对你好的人。你要的不是轰轰烈烈，而是不用每天猜对方到底在不在乎。",
                "你需要注意的是，不要因为太想要安全感，就把控制、确认和反复试探当作爱。未来 7 天，试着观察一个人的行动，而不是只盯着一句话。",
            ],
        },
    }


def build_lieflat_questions():
    rows = [
        ["最近面对生活和工作，你最常出现的状态是？", "能省力就省力，先保住自己", "别人冲我也得冲，不然会落后", "会做取舍，重要的事认真做", "很累但停不下来，心里一直紧绷"],
        ["看到别人很拼、很卷时，你第一反应是？", "他们厉害，但我不想跟", "有压力，感觉自己也要加速", "先看这件事值不值得投入", "会焦虑，觉得自己好像不够努力"],
        ["如果今天只完成了一半任务，你会怎么想？", "也可以，明天再说", "不行，我得补回来", "看优先级，重要的完成就够了", "会自责，但又没力气继续"],
        ["你最想从当前状态里获得什么？", "轻松一点，不要被消耗", "更快变强，拿到结果", "节奏稳定，长期可持续", "别再被焦虑推着走"],
        ["你如何理解“躺平”？", "是一种自救，先别把自己耗干", "有点危险，容易被人甩开", "可以休息，但不能完全放弃选择", "我也想躺，但现实不允许"],
        ["你如何理解“内卷”？", "没必要，很多竞争都不值得", "有时候必须卷，结果不会骗人", "要卷也得卷在关键处", "我讨厌内卷，但经常被卷进去"],
        ["遇到新机会时，你通常会？", "先观望，不想轻易折腾", "马上研究，怕错过窗口", "判断成本和收益，再决定", "想抓住，但又怕自己撑不住"],
        ["你最容易被哪句话击中？", "人先活好，比什么都重要", "你不努力，就会被替代", "把力气用在真正值得的地方", "我已经很累了，为什么还不敢停"],
        ["如果休息一天，你会？", "很享受，终于喘口气", "有负罪感，觉得浪费时间", "会安排真正恢复能量的休息", "身体在休息，脑子还在焦虑"],
        ["你现在最缺的是什么？", "空间和松弛感", "目标和爆发力", "清晰边界和节奏", "安全感和确定感"],
        ["别人催你上进时，你会？", "反感，我有自己的活法", "被刺激到，想证明自己", "听一听，但不完全照单全收", "更焦虑，觉得自己哪里都不够"],
        ["你对“努力”的真实感受是？", "不是不努力，是不想无意义消耗", "努力是基本盘，不努力没安全感", "努力要有方向，否则就是浪费", "我一直努力，但好像没得到反馈"],
        ["你更害怕哪种结果？", "把自己累坏了还没意义", "被同龄人远远甩开", "忙了很多却没做对选择", "一直卡在焦虑里出不来"],
        ["你做决定时最看重什么？", "会不会让我更轻松", "能不能让我更快赢", "是否符合长期目标", "会不会让我更有安全感"],
        ["如果可以重设生活节奏，你会选？", "少一点目标，多一点自由", "更高效率，更快成长", "有冲刺也有恢复", "先把混乱和焦虑降下来"],
        ["你最常见的拖延原因是？", "不想做没意义的事", "压力太大，怕做不好", "还没确认优先级", "脑子太乱，启动很难"],
        ["面对竞争，你更像哪一种？", "能避开就避开，不想卷进去", "会被激起胜负欲", "只参加值得的竞争", "明明不想卷，却被环境推着走"],
        ["你现在的能量水平更接近？", "低电量，想省着用", "高紧绷，靠意志撑着", "中等，但需要合理分配", "忽高忽低，很不稳定"],
        ["如果有人说你太佛系，你会？", "我只是看开了", "会有点不服，想证明自己", "佛系不等于放弃，我有节奏", "其实我是累到没办法"],
        ["如果有人说你太卷，你会？", "我不想变成那样", "可能吧，但我想赢", "要看卷的对象值不值", "我也不想，但停下来更慌"],
        ["你最想摆脱哪种状态？", "被外界标准绑架", "努力很久没有结果", "忙乱但不聚焦", "一直焦虑、一直内耗"],
        ["你认为自己真正需要的是？", "降低消耗，重新生活", "集中火力，打一次翻身仗", "找到适合自己的节奏", "先从压力里缓过来"],
        ["接下来一个月，你更想做什么？", "少做一点，恢复自己", "多冲一点，拿到突破", "重排优先级，稳步推进", "先解决最焦虑的一件事"],
        ["做完这个测试，你最想知道什么？", "我是不是适合躺平一点", "我是不是该继续卷", "我的节奏到底该怎么调", "我为什么总是又累又停不下来"],
    ]
    questions = []
    for row in rows:
        questions.append(
            {
                "text": row[0],
                "options": [
                    {"text": row[1], "type": "A"},
                    {"text": row[2], "type": "B"},
                    {"text": row[3], "type": "C"},
                    {"text": row[4], "type": "D"},
                ],
            }
        )
    return questions


def build_lieflat_results(theme):
    return {
        "A": {
            "name": "主动躺平修复型",
            "summary": "你不是没有追求，而是已经开始本能地拒绝无意义消耗。",
            "sections": [
                "你对外界的竞争标准有一定免疫力，不太愿意为了别人眼里的“上进”牺牲自己的生活感。你更在意的是：这件事值不值得、会不会把自己耗空。",
                "你的优势是清醒、会止损，也更懂得保护自己的能量。你不是不能努力，而是不想把力气交给没有回报的内卷。",
                "你需要注意的是，休息和放弃之间要有边界。未来 7 天，可以给自己定一个很小的恢复型目标：少消耗一点，但也保留一点掌控感。",
            ],
        },
        "B": {
            "name": "内卷冲刺驱动型",
            "summary": "你对结果很敏感，也很容易被竞争感点燃。",
            "sections": [
                "你心里有很强的胜负欲和不甘心。看到别人往前冲，你很难完全无动于衷，因为你害怕自己错过机会、被甩开、被替代。",
                "你的优势是行动力强、目标感重，关键时刻能逼自己顶上去。只要方向正确，你很容易在短期内做出明显变化。",
                "你需要警惕的是，不是所有赛道都值得卷。未来 7 天，请先确认：你现在努力的事，是在接近自己的目标，还是只是在缓解焦虑。",
            ],
        },
        "C": {
            "name": "清醒节奏掌控型",
            "summary": "你不想盲目躺，也不想盲目卷，你更适合建立自己的节奏。",
            "sections": [
                "你比较能看清努力和消耗的区别。你知道什么时候该冲，也知道什么时候该停下来整理方向。对你来说，最重要的不是姿态，而是节奏。",
                "你的优势是判断力、边界感和长期思维。你不容易被短期情绪带着跑，更适合用稳定系统替代一时鸡血。",
                "你的卡点是有时想得太多，启动偏慢。未来 7 天，给自己排一个“三件事清单”：一件必须做，一件可以做，一件明确不做。",
            ],
        },
        "D": {
            "name": "被迫内耗卡住型",
            "summary": "你看起来像在躺平和内卷之间摇摆，其实是压力太满了。",
            "sections": [
                "你不是不想前进，也不是只想摆烂，而是长期处在一种“想努力但很累、想休息又不敢”的拉扯里。你的能量被焦虑分走了太多。",
                "你的优势是敏感、负责，也很在意自己有没有变好。只是当压力堆太久，行动力会被自责和混乱压住。",
                "你现在最需要的不是继续逼自己，而是先把压力拆小。未来 7 天，只处理一件最影响你的事，把它做小、做具体、做到能完成。",
            ],
        },
    }


def is_love_theme(theme):
    return any(word in theme for word in ["恋爱", "喜欢", "生理性", "暧昧", "关系", "心动"])


def is_lieflat_theme(theme):
    return any(word in theme for word in ["躺平", "内卷", "米氏盒", "摆烂"])


def build_config(theme):
    if is_love_theme(theme):
        return {
            "theme": theme,
            "eyebrow": "LOVE PATTERN NAVIGATOR",
            "title": "你是恋爱脑，还是生理性喜欢？",
            "subtitle": "30 道题，看清你的心动到底是哪一种",
            "subtitle_lines": [
                "不是每一次放不下，都是爱得太深。",
                "也不是每一次想靠近，都适合走到长期。",
            ],
            "price_hint": "娱乐测试，仅供情感自我探索参考，不构成心理诊断。",
            "intro": "这个测试会通过 30 个选择题，帮你分辨自己更接近恋爱脑、生理性喜欢、清醒慢热，还是安全感依恋。",
            "intro_paragraphs": [
                "你有没有过这种感觉：明明才认识不久，却会忍不住等消息、翻动态、猜对方每一句话的意思。",
                "有时候你以为自己很喜欢一个人，但真正让你上头的，可能是身体吸引、暧昧刺激，或者被坚定选择的感觉。",
                "很多人的感情困惑，不是不会爱，而是没有分清：你是在爱这个人，还是在迷恋一种被点燃、被需要、被回应的状态。",
            ],
            "value_statement": "这个测试会从情绪投入、身体吸引、长期适配、安全感需求四个维度，帮你判断：你现在更接近恋爱脑投入，还是生理性喜欢上头。",
            "dimensions": ["情绪投入", "身体吸引", "长期适配", "安全感需求"],
            "style": "soft-love",
            "share_line": "喜欢一个人不难，难的是看清自己到底在被什么吸引。",
            "questions": build_love_questions(),
            "results": build_love_results(theme),
        }
    if is_lieflat_theme(theme):
        return {
            "theme": theme,
            "eyebrow": "LIFE PACE CHECK",
            "title": "你适合躺平，还是内卷？",
            "subtitle": "24 道题，看清你现在真正需要的生活节奏",
            "subtitle_lines": [
                "不是每一次想躺平，都是不上进。",
                "也不是每一次很努力，都是真的在变好。",
            ],
            "price_hint": "娱乐测试，仅供自我探索参考，不构成职业或心理诊断。",
            "intro": "这个测试会通过 24 个选择题，帮你分辨自己更接近主动躺平、内卷冲刺、清醒节奏，还是被迫内耗。",
            "intro_paragraphs": [
                "你有没有过这种感觉：一边想把生活过轻松一点，一边又害怕自己真的落后。",
                "看到别人学习、搞钱、换赛道，你会被刺激到；可轮到自己行动时，又觉得身心都很疲惫。",
                "很多人的卡住，不是因为不努力，也不是因为太懒，而是没有分清：你现在需要休息，还是需要换一种更有效的用力方式。",
            ],
            "value_statement": "这个测试会从能量状态、竞争压力、行动节奏、内耗来源四个维度，帮你判断：你现在更适合主动降耗，还是集中发力。",
            "dimensions": ["能量状态", "竞争压力", "行动节奏", "内耗来源"],
            "style": "neutral-pace",
            "share_line": "真正重要的不是躺平还是内卷，而是找到不消耗自己的节奏。",
            "questions": build_lieflat_questions(),
            "results": build_lieflat_results(theme),
        }
    return {
        "theme": theme,
        "title": theme,
        "subtitle": "16 道题，看见你的隐藏倾向和下一步方向",
        "price_hint": "娱乐测试，仅供自我探索参考",
        "intro": "这个测试会通过 16 个选择题，帮你看见自己更接近哪一种状态。",
        "style": "warm",
        "share_line": "你不是没有答案，只是需要一个更适合自己的方向。",
        "questions": build_questions(theme),
        "results": build_results(theme),
    }


def render_html(config):
    data = json.dumps(config, ensure_ascii=False)
    title = html.escape(config["title"])
    subtitle = html.escape(config["subtitle"])
    price_hint = html.escape(config["price_hint"])
    intro = html.escape(config.get("intro", f"这个测试会通过 {len(config['questions'])} 个选择题，帮你看见自己更接近哪一种状态。"))
    eyebrow = html.escape(config.get("eyebrow", "SELF DISCOVERY TEST"))
    subtitle_lines = [html.escape(line) for line in config.get("subtitle_lines", [])]
    intro_paragraphs = [html.escape(line) for line in config.get("intro_paragraphs", [config.get("intro", "")])]
    value_statement = html.escape(config.get("value_statement", intro))
    dimensions = [html.escape(item) for item in config.get("dimensions", [])]
    share_line = html.escape(config.get("share_line", "你不是没有答案，只是需要一个更适合自己的方向。"))
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    if config.get("style") == "soft-love":
        colors = {
            "text": "#4a2935",
            "bg": "linear-gradient(180deg, #fff4f7 0%, #fff9fb 46%, #fff2ee 100%)",
            "tag_bg": "transparent",
            "tag_text": "#bd6d87",
            "sub": "#8d6675",
            "panel_border": "rgba(232, 166, 188, 0.42)",
            "panel_shadow": "0 18px 48px rgba(190, 87, 124, 0.14)",
            "notice": "#a27a88",
            "progress": "#f6d8e2",
            "primary": "#c85d84",
            "secondary": "#f9dfe8",
            "secondary_text": "#8d4260",
            "option_bg": "rgba(255, 255, 255, 0.78)",
            "option_hover": "#fff0f5",
            "result": "#a23e65",
            "share_bg": "rgba(255, 240, 246, 0.86)",
            "accent": "#d78ca6",
            "button_text": "#fffafc",
        }
    elif config.get("style") == "neutral-pace":
        colors = {
            "text": "#2f3633",
            "bg": "linear-gradient(180deg, #f6f4ee 0%, #fbfaf6 48%, #eef3ed 100%)",
            "tag_bg": "transparent",
            "tag_text": "#6f7d75",
            "sub": "#6f756f",
            "panel_border": "rgba(126, 146, 132, 0.34)",
            "panel_shadow": "0 18px 44px rgba(65, 78, 68, 0.12)",
            "notice": "#7d847e",
            "progress": "#dfe7dd",
            "primary": "#43524a",
            "secondary": "#e7ebe5",
            "secondary_text": "#4f5c55",
            "option_bg": "rgba(255, 255, 255, 0.76)",
            "option_hover": "#eef4ee",
            "result": "#4f685b",
            "share_bg": "rgba(240, 246, 239, 0.88)",
            "accent": "#7f9a8a",
            "button_text": "#fffdf7",
        }
    elif config.get("style") == "pink":
        colors = {
            "text": "#34232b",
            "bg": "linear-gradient(180deg, #fff5f8 0%, #fffafd 48%, #fff3f6 100%)",
            "tag_bg": "#ffe1ec",
            "tag_text": "#a93562",
            "sub": "#765866",
            "panel_border": "#f3cddd",
            "panel_shadow": "0 12px 34px rgba(185, 82, 124, 0.12)",
            "notice": "#946476",
            "progress": "#f9dce8",
            "primary": "#d94f86",
            "secondary": "#f7dde8",
            "secondary_text": "#7d3956",
            "option_bg": "#fff9fb",
            "option_hover": "#fff0f6",
            "result": "#8f315b",
            "share_bg": "#fff0f6",
        }
    else:
        colors = {
            "text": "#2b211d",
            "bg": "#fff8f2",
            "tag_bg": "#ffe2cc",
            "tag_text": "#8a3d12",
            "sub": "#6d5a50",
            "panel_border": "#f0d8c7",
            "panel_shadow": "0 8px 24px rgba(112, 65, 32, 0.08)",
            "notice": "#85624e",
            "progress": "#f6e6db",
            "primary": "#dc6b2f",
            "secondary": "#f4e5d9",
            "secondary_text": "#5b3a27",
            "option_bg": "#fffaf6",
            "option_hover": "#fff1e6",
            "result": "#6d4a36",
            "share_bg": "#fff3e9",
        }

    if subtitle_lines:
        subtitle_block = "\n".join(f'      <div>{line}</div>' for line in subtitle_lines)
    else:
        subtitle_block = f"      <div>{subtitle}</div>"
    intro_block = "\n".join(f"      <p>{paragraph}</p>" for paragraph in intro_paragraphs)
    dimension_block = ""
    if dimensions:
        dimension_items = "\n".join(f'        <div class="dimension">{item}</div>' for item in dimensions)
        dimension_block = f"""
      <div class="dimensions">
{dimension_items}
      </div>"""

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
      color: {colors["text"]};
      background: {colors["bg"]};
      line-height: 1.7;
    }}
    body::before {{
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      background:
        radial-gradient(circle at 18% 10%, rgba(255, 199, 216, 0.36), transparent 28%),
        radial-gradient(circle at 86% 18%, rgba(223, 232, 218, 0.55), transparent 24%),
        radial-gradient(circle at 50% 92%, rgba(196, 212, 196, 0.32), transparent 32%);
      z-index: -1;
    }}
    .page {{
      width: min(760px, 100%);
      margin: 0 auto;
      padding: 44px 22px 56px;
    }}
    .hero {{
      padding: 28px 0 26px;
      text-align: center;
    }}
    .tag {{
      display: inline-block;
      padding: 0;
      background: {colors["tag_bg"]};
      color: {colors["tag_text"]};
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 15px;
      letter-spacing: 0.2em;
      margin-bottom: 36px;
    }}
    h1 {{
      margin: 0;
      font-size: clamp(34px, 7vw, 48px);
      line-height: 1.25;
      letter-spacing: 0;
      font-weight: 900;
    }}
    .subtitle {{
      margin: 24px 0 0;
      color: {colors["sub"]};
      font-size: clamp(18px, 4.5vw, 24px);
      font-weight: 700;
      line-height: 1.65;
    }}
    .divider {{
      width: 92px;
      height: 1px;
      background: #cfd5d8;
      margin: 44px auto 0;
    }}
    .panel {{
      background: rgba(255, 255, 255, 0.78);
      border: 1px solid {colors["panel_border"]};
      border-radius: 18px;
      padding: 28px;
      box-shadow: {colors["panel_shadow"]};
      backdrop-filter: blur(10px);
    }}
    .intro-panel {{
      background: transparent;
      border: 0;
      box-shadow: none;
      padding: 20px 0 0;
      font-size: clamp(17px, 4.2vw, 22px);
      color: #654654;
      line-height: 1.95;
    }}
    .intro-panel p {{
      margin: 0 0 22px;
    }}
    .value {{
      margin-top: 22px;
      color: {colors["text"]};
      font-weight: 850;
    }}
    .dimensions {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      margin: 36px 0 34px;
    }}
    .dimension {{
      border: 1px solid rgba(215, 140, 166, 0.42);
      background: rgba(255, 255, 255, 0.56);
      color: #9b5c73;
      min-height: 62px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: clamp(16px, 4vw, 20px);
      font-weight: 750;
      border-radius: 14px;
    }}
    .notice {{
      margin: 24px 0 0;
      color: {colors["notice"]};
      font-size: 14px;
    }}
    .progress {{
      height: 8px;
      background: {colors["progress"]};
      border-radius: 999px;
      overflow: hidden;
      margin: 18px 0;
    }}
    .bar {{
      height: 100%;
      width: 0;
      background: {colors["primary"]};
      transition: width .25s ease;
    }}
    .question-count {{
      color: {colors["notice"]};
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
      border: 1px solid {colors["panel_border"]};
      background: {colors["option_bg"]};
      color: {colors["text"]};
      padding: 14px 14px;
      border-radius: 8px;
      margin: 10px 0;
      font-size: 16px;
      cursor: pointer;
    }}
    .option:hover {{
      border-color: {colors["primary"]};
      background: {colors["option_hover"]};
    }}
    .actions {{
      display: flex;
      gap: 10px;
      margin-top: 16px;
    }}
    button.primary, button.secondary {{
      border: 0;
      border-radius: 16px;
      padding: 18px 16px;
      font-size: 22px;
      font-weight: 850;
      cursor: pointer;
    }}
    .primary {{
      background: {colors["primary"]};
      color: {colors.get("button_text", "white")};
      width: 100%;
      box-shadow: 0 14px 30px rgba(200, 93, 132, 0.24);
    }}
    .secondary {{
      background: {colors["secondary"]};
      color: {colors["secondary_text"]};
    }}
    .result-title {{
      font-size: 24px;
      font-weight: 800;
      margin: 4px 0 8px;
    }}
    .result-summary {{
      color: {colors["result"]};
      font-weight: 700;
      margin-bottom: 16px;
    }}
    .result-section {{
      border-top: 1px solid {colors["panel_border"]};
      padding-top: 14px;
      margin-top: 14px;
    }}
    .share {{
      background: {colors["share_bg"]};
      border-left: 4px solid {colors["primary"]};
      padding: 12px;
      border-radius: 6px;
      margin-top: 18px;
    }}
    .report-panel {{
      background: #11151a;
      color: #f7f3e8;
      border-color: rgba(211, 174, 92, 0.24);
      box-shadow: 0 24px 70px rgba(17, 21, 26, 0.28);
    }}
    .report-top {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      color: #d3ae5c;
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 0.08em;
      border-bottom: 1px solid rgba(211, 174, 92, 0.18);
      padding-bottom: 16px;
      margin-bottom: 22px;
    }}
    .type-pill {{
      display: inline-block;
      padding: 5px 14px;
      border-radius: 999px;
      background: rgba(211, 174, 92, 0.14);
      color: #d8b96f;
      font-size: 13px;
      font-weight: 800;
    }}
    .report-name {{
      margin: 12px 0 4px;
      font-size: clamp(34px, 8vw, 52px);
      line-height: 1.15;
      font-weight: 950;
      letter-spacing: 0;
      text-align: center;
    }}
    .report-subtitle {{
      text-align: center;
      color: #bfc4c7;
      font-size: 17px;
      margin-bottom: 18px;
    }}
    .report-score {{
      text-align: center;
      color: #d8b96f;
      font-size: 36px;
      line-height: 1.1;
      font-weight: 950;
      margin: 18px 0;
    }}
    .report-score span {{
      color: #bfc4c7;
      font-size: 15px;
      font-weight: 750;
      margin-left: 8px;
    }}
    .core-box {{
      border: 1px solid rgba(211, 174, 92, 0.18);
      background: rgba(255, 255, 255, 0.04);
      border-radius: 8px;
      padding: 18px;
      margin: 22px 0;
    }}
    .core-label {{
      color: #d8b96f;
      font-weight: 850;
      margin-bottom: 8px;
    }}
    .gold-line {{
      color: #d8b96f;
      text-align: center;
      font-weight: 850;
      margin: 20px 0 18px;
    }}
    .locked-report {{
      position: relative;
      overflow: hidden;
      border-radius: 10px;
      border: 1px solid rgba(211, 174, 92, 0.16);
      background: rgba(255, 255, 255, 0.03);
      padding: 18px;
      max-height: 220px;
      margin-top: 18px;
    }}
    .locked-content {{
      filter: blur(4px);
      opacity: 0.56;
    }}
    .locked-item {{
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      padding: 12px 0;
    }}
    .lock-overlay {{
      position: absolute;
      inset: auto 0 0;
      padding: 54px 18px 18px;
      text-align: center;
      background: linear-gradient(180deg, rgba(17, 21, 26, 0) 0%, rgba(17, 21, 26, 0.94) 44%, #11151a 100%);
    }}
    .lock-icon {{
      width: 36px;
      height: 36px;
      border-radius: 999px;
      border: 1px solid rgba(211, 174, 92, 0.52);
      color: #d8b96f;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 10px;
      font-size: 20px;
    }}
    .unlock-title {{
      color: #f7f3e8;
      font-size: 18px;
      font-weight: 900;
    }}
    .unlock-text {{
      color: #d8b96f;
      font-size: 13px;
      margin-top: 5px;
    }}
    .report-actions {{
      display: grid;
      gap: 10px;
      margin-top: 18px;
    }}
    .report-button {{
      border: 0;
      border-radius: 8px;
      padding: 16px;
      background: #d8b96f;
      color: #171717;
      font-size: 18px;
      font-weight: 950;
      cursor: pointer;
    }}
    .report-secondary {{
      border: 1px solid rgba(211, 174, 92, 0.28);
      border-radius: 8px;
      padding: 14px;
      background: transparent;
      color: #d8b96f;
      font-size: 15px;
      font-weight: 850;
      cursor: pointer;
    }}
    .hidden {{ display: none; }}
    .footer {{
      text-align: center;
      color: {colors["notice"]};
      font-size: 12px;
      margin-top: 26px;
    }}
    @media (max-width: 520px) {{
      .page {{
        padding: 36px 24px 48px;
      }}
      .panel {{
        padding: 22px;
      }}
      .dimensions {{
        gap: 10px;
      }}
      .dimension {{
        min-height: 54px;
      }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <section class="hero">
      <span class="tag">• {eyebrow} •</span>
      <h1>{title}</h1>
      <div class="subtitle">
{subtitle_block}
      </div>
      <div class="divider"></div>
    </section>

    <section id="start" class="intro-panel">
{intro_block}
      <p class="value">{value_statement}</p>
{dimension_block}
      <button class="primary" onclick="startTest()">开始测试</button>
      <p class="notice">{price_hint}</p>
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

    function escapeText(value) {{
      return String(value || "").replace(/[&<>"']/g, char => ({{
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
      }}[char]));
    }}

    function renderReportPreview(result, winner, scores) {{
      const preview = TEST.report_preview;
      const report = preview.reports[winner];
      const topScore = scores[winner] || 0;
      const score = Math.min(96, (report.base_score || 78) + Math.max(0, topScore - 8));
      const locked = (report.locked || []).map(item => `<div class="locked-item">${{escapeText(item)}}</div>`).join("");
      return `
        <div class="report-top">
          <span>${{escapeText(preview.label || "你的专属报告")}}</span>
          <span>${{escapeText(preview.kicker || "REPORT")}}</span>
        </div>
        <div style="text-align:center"><span class="type-pill">你的类型</span></div>
        <div class="report-name">${{escapeText(report.name || result.name)}}</div>
        <div class="report-subtitle">${{escapeText(report.summary || result.summary)}}</div>
        <div class="report-score">${{score}}<span>${{escapeText(report.index_label || "专属指数")}}</span></div>
        <div class="core-box">
          <div class="core-label">核心结论</div>
          <div>${{escapeText(report.core || result.summary)}}</div>
        </div>
        <div class="gold-line">「${{escapeText(report.gold || TEST.share_line)}}」</div>
        <div class="locked-report">
          <div class="locked-content">${{locked}}</div>
          <div class="lock-overlay">
            <div class="lock-icon">锁</div>
            <div class="unlock-title">${{escapeText(preview.unlock_title || "完整报告 · 解锁查看")}}</div>
            <div class="unlock-text">${{escapeText(preview.unlock_text || "解锁后查看完整分析和行动建议")}}</div>
          </div>
        </div>
        <div class="report-actions">
          <button class="report-button" onclick="alert('这里后续可以接 1.9 元付费链接或公众号回复关键词。')">${{escapeText(preview.button_text || "解锁完整报告")}}</button>
          <button class="report-secondary" onclick="startTest()">重新测试</button>
        </div>
      `;
    }}

    function showResult() {{
      const scores = {{ A: 0, B: 0, C: 0, D: 0 }};
      answers.forEach(type => scores[type] += 1);
      const winner = Object.keys(scores).sort((a, b) => scores[b] - scores[a])[0];
      const result = TEST.results[winner];
      document.getElementById("bar").style.width = "100%";
      if (TEST.report_preview && TEST.report_preview.enabled) {{
        document.getElementById("result").classList.add("report-panel");
        document.getElementById("result").innerHTML = renderReportPreview(result, winner, scores);
        show("result");
        return;
      }}
      document.getElementById("result").classList.remove("report-panel");
      document.getElementById("result").innerHTML = `
        <div class="question-count">你的测试结果</div>
        <div class="result-title">${{result.name}}</div>
        <div class="result-summary">${{result.summary}}</div>
        ${{result.sections.map(section => `<div class="result-section">${{section}}</div>`).join("")}}
        <div class="share">适合截图分享的一句话：{share_line}</div>
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
