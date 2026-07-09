"""
iOS Objective-C 面试助手
提供知识图谱浏览、面试题练习、答题评分等功能
"""

import os
import sys

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)

from modules.graph_manager import GraphManager
from modules.question_generator import QuestionGenerator
from modules.answer_evaluator import AnswerEvaluator
from modules.progress_tracker import ProgressTracker


class iOSInterviewAssistant:
    def __init__(self):
        self.graph_manager = GraphManager()
        self.question_generator = QuestionGenerator()
        self.answer_evaluator = AnswerEvaluator()
        self.progress_tracker = ProgressTracker()

    def show_graph(self):
        return self.graph_manager.show_graph()

    def get_question(self, category=None, difficulty=None):
        question = self.question_generator.generate_question(category, difficulty)
        if question:
            self.current_question = question
            return question
        return None

    def evaluate_answer(self, user_answer):
        if not hasattr(self, 'current_question') or not self.current_question:
            return {"error": "请先获取题目"}
        
        result = self.answer_evaluator.evaluate(self.current_question, user_answer)
        self.progress_tracker.update_progress(
            self.current_question['category'],
            result['score'],
            self.current_question['id']
        )
        return result

    def show_progress(self):
        return self.progress_tracker.get_progress_report()

    def get_wrong_questions(self):
        return self.progress_tracker.get_wrong_questions()

    def reset_progress(self):
        return self.progress_tracker.reset_progress()


def main():
    assistant = iOSInterviewAssistant()
    print("🎉 iOS Objective-C 面试助手已启动！")
    print("\n可用命令：")
    print("  graph     - 查看知识图谱")
    print("  question  - 获取面试题 (可选参数: category difficulty)")
    print("  progress  - 查看学习进度")
    print("  wrong     - 查看错题本")
    print("  reset     - 重置进度")
    print("  help      - 显示帮助")
    print("  exit      - 退出")
    print("\n开始学习吧！输入 'graph' 查看知识图谱")


if __name__ == "__main__":
    main()
