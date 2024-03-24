# *-* coding: utf-8 *-*
from llm_agent_work_utils import get_config, call_llm
from openai import OpenAI
from collections import namedtuple


class MemoryModule:
    """
    質問と回答のペアを記憶するクラス
    """
    def __init__(self):
        self.question_trace = []
        self.answer_trace = []

    def add_question(self, question: str):
        self.question_trace.append(question)

    def add_answer(self, answer: str):
        self.answer_trace.append(answer)

    def get_last_question(self):
        return self.question_trace[-1] if self.question_trace else None

    def get_last_answer(self):
        return self.answer_trace[-1] if self.answer_trace else None


def decompose_question(question: str, config: namedtuple):
    """
    質問を分解する
    """
    with open('prompts/decompose.txt', 'r') as f:
        decompose_prompt = f.read()
    decompose_prompt = decompose_prompt.format(user_question=question)

    chat_completion = call_llm(prompt=decompose_prompt, config=config)

    try:
        # JSON文字列を辞書に変換し、サブクエスチョンを取り出す
        response_data = chat_completion.choices[0].message.content.strip()
        decomposed_questions = eval(response_data)["sub-questions"]
        return decomposed_questions
    except:
        # エラーが発生した場合は空のリストを返す
        return []


def agent_core(question, memory, config: namedtuple):
    memory.add_question(question)
    decomposed_questions = decompose_question(question, config)
    answers = []
    for decomposed_question in decomposed_questions:
        answer = call_llm(prompt=decomposed_question, config=config)
        answer = answer.choices[0].message.content
        answers.append(answer)
        memory.add_answer(answer)
    # すべての回答を統合して最終回答を生成します
    final_answer = " + ".join(answers)
    return final_answer


def test_decompose():
    config_file = 'config/config.yaml'
    config = get_config(config_file)
    question = "住友商事の2023年2Qと2023年3Qの収益の差を教えてください。"
    sub_questions = decompose_question(question, config)
    print("分解されたサブクエスチョン:", sub_questions)
    exit(1)


def main():
    # decomposeの動作確認
    # test_decompose()

    config_file = 'config/config.yaml'
    config = get_config(config_file)

    # メモリモジュールのインスタンス化
    memory = MemoryModule()

    # エージェントに質問をする
    question = "住友商事の2023年2Qと2023年3Qの収益の差を教えてください。"
    final_answer = agent_core(question, memory, config)

    print("最終回答:", final_answer)


if __name__ == "__main__":
    main()