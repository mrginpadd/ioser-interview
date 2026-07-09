import os

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(SKILL_DIR, 'data')
MODULES_DIR = os.path.join(SKILL_DIR, 'modules')
UTILS_DIR = os.path.join(SKILL_DIR, 'utils')

KNOWLEDGE_GRAPH_FILE = os.path.join(DATA_DIR, 'knowledge_graph.json')
QUESTIONS_FILE = os.path.join(DATA_DIR, 'questions.json')
PROGRESS_FILE = os.path.join(DATA_DIR, 'progress.json')

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
    'concept': '概念题',
    'code': '代码题',
    'scenario':