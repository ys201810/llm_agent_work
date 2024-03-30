# *-* coding: utf-8 *-*
from llm_agent_work_utils import get_config, call_llm
from collections import namedtuple
from pathlib import Path


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
    with open(config.base_path / 'prompts' / 'decompose.txt', 'r') as f:
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


def extract_company_name(question: str, config: namedtuple):
    """
    会社名を抽出する
    """
    with open(config.base_path / 'prompts' / 'extract_company_name.txt', 'r') as f:
        extract_company_name_prompt = f.read()
    extract_company_name_prompt = extract_company_name_prompt.format(user_question=question)

    chat_completion = call_llm(prompt=extract_company_name_prompt, config=config)

    try:
        # JSON文字列を辞書に変換し、サブクエスチョンを取り出す
        response_data = chat_completion.choices[0].message.content.strip()
        company_name = eval(response_data)["company_name"]
        if len(company_name) != 1:
            print('会社名が複数あります。一つの会社名のみを指定してください')
            exit(1)
        return company_name[0]
    except:
        # エラーが発生した場合は空のリストを返す
        return []


def extract_target_period(question: str, config: namedtuple):
    """
    会社名を抽出する
    """
    with open(config.base_path / 'prompts' / 'extract_target_period.txt', 'r') as f:
        extract_target_period_prompt = f.read()
    extract_target_period_prompt = extract_target_period_prompt.format(user_question=question)

    chat_completion = call_llm(prompt=extract_target_period_prompt, config=config)

    try:
        # JSON文字列を辞書に変換し、サブクエスチョンを取り出す
        response_data = chat_completion.choices[0].message.content.strip()
        year = eval(response_data)["year"]
        quarter = eval(response_data)["quarter"]
        return year, quarter
    except:
        # エラーが発生した場合は空のリストを返す
        return []


def get_context(year: str, quarter: str, company_name: str, config: namedtuple):
    """
    コンテキストを取得する
    """
    if not year or not quarter or not company_name:
        return ''
    with open(config.base_path / 'data' / company_name / 'annual_financial_results' / f'{year}_{quarter.lower()}.txt', 'r') as f:
        context = f.read()
    return context

def agent_core(question, memory, config: namedtuple):
    memory.add_question(question)
    print(f'大元の質問: {question}')
    # 1. 質問を分解する。
    decomposed_questions = decompose_question(question, config)
    print(f'分解した質問: {decomposed_questions}')
    # 2. 会社名を取得する。
    company_name = extract_company_name(question, config)
    answers = []
    for decomposed_question in decomposed_questions:
        print(f'対象の質問:{decomposed_question}')
        is_calc_final = False
        # 3. 質問の中から、対象期間を抽出する。
        year, quarter = extract_target_period(decomposed_question, config)
        if year or quarter:
            print(f'質問内の対象期間: {year}年{quarter}')
        # 4. 会社名、対象期間を用いて、コンテキストを取得する。
        context = get_context(year, quarter, company_name, config)
        if not context:
            context = ' '.join(memory.answer_trace)
            is_calc_final = True
        answer = call_llm(prompt=decomposed_question, config=config, context=context, is_calc_final=is_calc_final)
        answer = answer.choices[0].message.content
        answers.append(answer)
        print(f'回答: {answer}')
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

    base_path = Path(__file__).parent.parent
    config_file = base_path / 'config' / 'config.yaml'
    config = get_config(config_file, base_path)

    # メモリモジュールのインスタンス化
    memory = MemoryModule()

    # エージェントに質問をする
    question = "住友商事の2023年2Qと2023年3Qの収益の差を教えてください。"
    final_answer = agent_core(question, memory, config)

    print("最終回答:", final_answer)


if __name__ == "__main__":
    main()