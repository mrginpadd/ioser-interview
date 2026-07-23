"""
申论备考助手
提供智能出题、实时批改、进度追踪等功能

注意：本Skill的核心逻辑由 rules.md 规则文件驱动，
而非Python代码。rules.md定义了出题规则、评分标准、
交互命令等，AI会根据规则动态生成题目和批改答案。
"""

import os
import sys

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)


class EssayExamCoach:
    def __init__(self):
        pass

    def get_question(self, question_type=None, theme=None, difficulty=None):
        return None

    def evaluate_answer(self, user_answer):
        return None

    def show_progress(self):
        return None

    def get_wrong_questions(self):
        return None

    def simulate_exam(self):
        return None

    def show_notes(self, question_type=None):
        return None


def main():
    coach = EssayExamCoach()
    print("🎉 申论备考助手已启动！")
    print("\n可用命令：")
    print("  出题         - 根据当前难度出题")
    print("  出一道 [题型] 的题 - 指定题型出题")
    print("  出一道 [主题] 的题 - 指定主题出题")
    print("  批改         - 批改当前作答")
    print("  模拟考试     - 完整模拟考试")
    print("  查看进度     - 查看学习进度")
    print("  查看错题     - 复习错题")
    print("  切换难度     - 切换难度等级")
    print("  查看题库     - 查看题目列表")
    print("  练习大作文   - 专门练习大作文")
    print("  查看笔记     - 查看笔记目录")
    print("  help         - 显示帮助")
    print("  exit         - 退出")
    print("\n开始学习吧！输入 '出题' 获取申论题目")


if __name__ == "__main__":
    main()