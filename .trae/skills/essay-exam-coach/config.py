import os

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(SKILL_DIR, 'data')
NOTES_DIR = os.path.join(SKILL_DIR, 'notes')
DOCS_DIR = os.path.join(SKILL_DIR, 'docs')

KNOWLEDGE_GRAPH_FILE = os.path.join(DATA_DIR, 'knowledge_graph.json')
QUESTIONS_FILE = os.path.join(DATA_DIR, 'questions.json')
PROGRESS_FILE = os.path.join(SKILL_DIR, 'progress.json')
QUESTION_BANK_FILE = os.path.join(DOCS_DIR, '申论题库.md')

DIFFICULTY_LEVELS = ['easy', 'medium', 'hard']

MASTERY_LEVELS = {
    0.0: '未学习',
    0.25: '入门',
    0.5: '熟悉',
    0.75: '掌握',
    1.0: '精通'
}

DIFFICULTY_LABELS = {
    'easy': '初级',
    'medium': '中级',
    'hard': '高级'
}

QUESTION_TYPES = {
    'summary': '归纳概括题',
    'analysis': '综合分析题',
    'solution': '提出对策题',
    'application': '应用文写作',
    'essay': '大作文'
}

TOPIC_MODULES = {
    '归纳概括': ['概括主要内容', '概括主要问题', '概括主要对策', '概括主要成效', '概括主要特点'],
    '综合分析': ['词句理解', '现象评析', '观点分析', '比较分析', '原因分析'],
    '提出对策': ['针对问题提对策', '对策可行性分析', '对策有效性评估', '对策优先级排序', '对策创新思维'],
    '应用文写作': ['倡议书写作', '公开信写作', '调研报告写作', '讲话稿写作', '工作汇报写作', '短评写作'],
    '大作文': ['策论文写作', '议论文写作', '立意提炼', '论证结构', '语言表达', '素材运用']
}

THEMES = [
    '经济转型',
    '社会管理',
    '文化建设',
    '生态建设'
]

WORD_LIMITS = {
    'summary': {'min': 150, 'max': 300},
    'analysis': {'min': 200, 'max': 400},
    'solution': {'min': 200, 'max': 400},
    'application': {'min': 500, 'max': 800},
    'essay': {'min': 800, 'max': 1000}
}

SCORE_RANGES = {
    'summary': {'min': 10, 'max': 20},
    'analysis': {'min': 15, 'max': 25},
    'solution': {'min': 15, 'max': 25},
    'application': {'min': 20, 'max': 30},
    'essay': {'min': 35, 'max': 50}
}

BANK_STRUCTURE = {
    '第一篇': {
        '第一章': '命题技术',
        '第二章': '阅卷规则'
    },
    '第二篇': {
        '第三章': '抓关键词',
        '第四章': {
            '第一节': '单一客观题',
            '第二节': '综合客观题',
            '第三节': '非常规题型'
        }
    },
    '第三篇': {
        '第五章': '议论文的三要素',
        '第六章': '文章的四个支点',
        '第七章': '文章的深加工',
        '真题示例': '大作文真题示例'
    },
    '第四篇': {
        '关键词': ['思想意识观念', '政策法律法规', '人才教育培训', '财物技术服务', '管理监督监管'],
        '关键句': ['政论文关键句', '策论文关键句']
    },
    '第五篇': {
        '高频考点': ['经济转型', '社会管理', '文化建设', '生态建设']
    },
    '附录': {
        '答题技巧': ['概括题', '分析题', '对策题', '应用文', '大作文']
    }
}