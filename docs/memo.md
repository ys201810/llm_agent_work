# memo
[Building Your First LLM Agent Application](https://developer.nvidia.com/blog/building-your-first-llm-agent-application/)を元にLLMエージェントを作成してみる。  

## やること
住友商事の決算情報から、以下の質問に回答するエージェントを作ってみる。  
「2023年の第2四半期と第3四半期の間で、収益はどれだけ成長しましたか？」

## データ
[住友商事の決算情報](https://www.sumitomocorp.com/ja/jp/ir/report)の決算説明会の会社説明のテキストを利用する。  
[2023/2Q](https://www.sumitomocorp.com/-/media/Files/hq/ir/report/summary/2023/2309Scripts.pdf?sc_lang=ja)
[2023/3Q](https://www.sumitomocorp.com/-/media/Files/hq/ir/report/summary/2023/2312Scripts.pdf?sc_lang=ja)

## メモ
### プロンプト変更
「あなたは特定の分野の専門家です。複雑な質問をよりシンプルなサブタスクに分解することがあなたの任務です。」   
だと、不完全な分類になることがあったので、後ろに「全ての関連するサブクエスチョンをリストアップしてください。」をつけた。
