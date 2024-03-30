# coding=utf-8
import pathlib

import yaml
from collections import namedtuple
from openai import OpenAI


def get_config(config_file: str, base_path: pathlib.Path) -> (str, str, pathlib.Path):
    """
    APIKEYを取得する。
    :param config_file(str): APIKEYが記載されているyamlファイルのパス
    :return: openai_api_key(str), deepl_api_key(str): OpenAIとDeepLのAPIKEY
    """
    Config = namedtuple('Config',[
        'openai_api_key',
        'openai_model',
        'base_path',
    ])

    with open(config_file, 'r') as inf:
        config = yaml.safe_load(inf)
    openai_api_key = config['openai']['api_key']
    openai_model = config['openai']['model']
    config = Config(
        openai_api_key=openai_api_key,
        openai_model=openai_model,
        base_path=base_path
    )

    return config


def call_llm(prompt: str, config: namedtuple, context: str = None, is_calc_final: bool = False):
    client = OpenAI(
        # This is the default and can be omitted
        api_key=config.openai_api_key,
    )

    if context:
        if is_calc_final:
            prompt = "[指示]の内容を[参考情報]を元に計算してください。\n[指示]" + prompt + "\n\n[参考情報]" + context
        else:
            with open(config.base_path / 'prompts' / 'extract_target_money.txt', 'r') as f:
                prompt_with_context = f.read()
            prompt = prompt_with_context.format(context=context, user_question=prompt)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt + "\n　上記の回答を、以下の内容を踏まえて回答してください。\n\n" + context if context else prompt,
            }
        ],
        model=config.openai_model,
        temperature=0.0,
    )

    return chat_completion