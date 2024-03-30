# llm_agent_work
住友商事の2023年2Qと3Qの利益の差の質問に回答できるLLMエージェントを作成する。  

## 参考
[Building Your First LLM Agent Application](https://developer.nvidia.com/blog/building-your-first-llm-agent-application/)  

## 動作方法
### configファイルの作成

```
$ cd llm_agent_work
$ mkdir config
$ touch config/config.yaml 
$ vi config/config.yaml
```

以下のようにconfig.yamlを記述してください。  

```
openai:
  api_key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  model: gpt-3.5-turbo  # gpt-4
```

### 実行

```
$ cd llm_agent_work/src
$ poetry run python main.py
```

### 実行結果
```
大元の質問: 住友商事の2023年2Qと2023年3Qの収益の差を教えてください。
分解した質問: ['2023年2Qの収益を計算する', '2023年3Qの収益を計算する', '2Qと3Qの収益の差を計算する']
対象の質問:2023年2Qの収益を計算する
質問内の対象期間: 2023年2Q
回答: 2023年の第2四半期の収益は2,849億円です。
対象の質問:2023年3Qの収益を計算する
質問内の対象期間: 2023年3Q
回答: 2023年の3Qの収益は3,600億円です。
対象の質問:2Qと3Qの収益の差を計算する
回答: 2Qと3Qの収益の差を計算すると、
3,600億円 - 2,849億円 = 751億円
となります。
最終回答: 2023年の第2四半期の収益は2,849億円です。 + 2023年の3Qの収益は3,600億円です。 + 2Qと3Qの収益の差を計算すると、
3,600億円 - 2,849億円 = 751億円
となります。
```

まぁ違うんだけど。。  

## メモ
全然汎用的に使えない感じになっているので雰囲気だけ。  
APIコール回数が多く、もっと簡略化できそう。  
is_calc_finalのフラグがとても分かりづらい。(最終の計算かどうかを判定しているけど、きったない。。)  
COTとか、RATが良さそうなので、このコードをこれ以上ブラッシュアップするつもりはない・・・。  
