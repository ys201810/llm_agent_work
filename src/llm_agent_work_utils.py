# coding=utf-8
import yaml
from collections import namedtuple
from openai import OpenAI


def get_config(config_file: str) -> (str, str):
    """
    APIKEYを取得する。
    :param config_file(str): APIKEYが記載されているyamlファイルのパス
    :return: openai_api_key(str), deepl_api_key(str): OpenAIとDeepLのAPIKEY
    """
    Config = namedtuple('Config',[
        'openai_api_key',
        'openai_model',
    ])

    with open(config_file, 'r') as inf:
        config = yaml.safe_load(inf)
    openai_api_key = config['openai']['api_key']
    openai_model = config['openai']['model']
    config = Config(
        openai_api_key=openai_api_key,
        openai_model=openai_model,
    )

    return config


def call_llm(prompt: str, config: namedtuple):
    client = OpenAI(
        # This is the default and can be omitted
        api_key=config.openai_api_key,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=config.openai_model,
        temperature=0.0,
    )

    return chat_completion