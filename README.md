# RAGチャットボット ハンズオン

Docker Composeを使って、TXTファイルの内容を検索して回答するRAGチャットボットを作成します。まず通常のAIチャットを作り、そこに文書登録とベクトル検索の機能を追加します。

RAGの基本技術（チャンク化・Embedding・ベクトル検索・回答生成）は講義で扱った内容を利用します。この実習では、実際に動かして結果を確認します。

## 1. 用意するもの

- Windows、macOS、Linuxのパソコン
- Git
- **Docker Desktop**（Windows / macOS）または **Docker Engine + Docker Compose V2**（Linux）
- OpenAIまたはAnthropicのAPIキー（回答生成に使用）
- Codex、Claude CodeなどのAIコーディングツール（利用する場合）

**Python・uv・Chromaなどをパソコンへ直接インストールする必要はありません。** Pythonや必要なライブラリはDockerコンテナ内で動作します。

APIの利用には契約・課金設定が必要な場合があります。APIを使わない場合は、講師の画面で動作を見る形でも参加できます。AIコーディングツールの利用には別途準備が必要な場合があります。

## 2. 起動する

### 2-1. プロジェクトを取得する

ターミナルを開いて実行します。

~~~bash
git clone https://github.com/actiom-inc/rag-chatbot-practice-202610.git
cd rag-chatbot-practice-202610
~~~

### 2-2. APIキーを設定する

macOS / Linux：

~~~bash
cp .env.example .env
~~~

Windows PowerShell：

~~~powershell
Copy-Item .env.example .env
~~~

作成した **.env** ファイルをエディタで開き、使用するAPIを設定します。

OpenAIを使用する場合：

~~~dotenv
LLM_PROVIDER=openai
OPENAI_API_KEY=自分のAPIキー
~~~

Anthropicを使用する場合：

~~~dotenv
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=自分のAPIキー
~~~

モデルIDを変更したい場合は、同じファイルの **OPENAI_MODEL** または **ANTHROPIC_MODEL** を編集します。利用できるモデルは契約状況によって異なります。

**APIキーは秘密情報です。** 公開リポジトリにコミットしたり、AIコーディングツールへ貼り付けたりしないでください。設定ファイルの中身を画面共有しないでください。

### 2-3. Dockerイメージを作成する

~~~bash
docker compose build
~~~

最初のビルドではコンテナと機械学習ライブラリをダウンロードするため、時間がかかり、まとまったディスク容量を使用する場合があります。

### 2-4. Embeddingモデルを準備する

~~~bash
docker compose run --rm app python scripts/preflight.py --download-model
~~~

文書と質問をベクトル化するためのモデルをダウンロードします。モデルのダウンロードは初回だけで、以後はDockerボリュームに保存されたキャッシュを利用します。このコマンドはOpenAI・Anthropicの回答生成APIを呼びません。

### 2-5. アプリを起動する

~~~bash
docker compose up -d
~~~

ブラウザで **http://localhost:8501** を開きます。

「RAGチャットボット ハンズオン」と表示されたら準備完了です。この段階ではチャットの送信機能はありません。

アプリを停止するとき：

~~~bash
docker compose down
~~~

※停止しても、登録した文書とEmbeddingモデルのキャッシュは残ります。

## 3. STEPごとに実装する

AIコーディングツールは**パソコン上のプロジェクトフォルダ**で実行してください。Dockerコンテナの中でAIコーディングツールを動かす必要はありません。

AIコーディングツールへ指示文を1つずつ渡し、編集されたコードをブラウザで確認します。ファイルはDockerへ共有されているため、通常はイメージの再ビルド不要で変更が反映されます。画面に反映されないときはブラウザを再読み込みしてください。

| STEP | 実装する機能 | AIへの指示文 | 完了条件 |
| --- | --- | --- | --- |
| 1 | 通常のAIチャット | [step1.md](prompts/step1.md) | 質問し、回答が返ってくる |
| 2 | TXTファイルの登録・検索 | [step2.md](prompts/step2.md) | 保存件数と検索結果が表示される |
| 3 | 資料に基づくRAG回答 | [step3.md](prompts/step3.md) | 登録資料に固有の質問へ答えられる |
| 4 | 回答と検索結果の確認 | [step4.md](prompts/step4.md) | 検索件数・根拠の有無による違いを観察できる |

**STEP 1：チャットを作る**

[step1.md](prompts/step1.md) に従って実装します。「こんにちは」と質問し、回答が返ったら、続けてもう一度質問してください。会話履歴が残れば成功です。

**STEP 2：ファイルを登録して検索する**

[step2.md](prompts/step2.md) に従って実装します。[01_ai_training.txt](samples/01_ai_training.txt) を登録し、「申込期限」を検索してください。資料の文章が表示され、アプリを再起動しても登録件数が残れば成功です。

**STEP 3：RAGチャットを完成させる**

[step3.md](prompts/step3.md) に従って実装します。「研修の申込期限は？」と質問し、「2026年11月30日」と回答され、参照された資料も確認できれば成功です。

**STEP 4：検索結果と回答を比べる**

[step4.md](prompts/step4.md) に従い、検索件数などの設定を変更しながら次の質問を試します。

| 質問 | 確認すること |
| --- | --- |
| 研修の申込期限は？ | 2026年11月30日と答えるか |
| いつまでに参加申請すればよい？ | 言い換えでも同じ根拠を取得できるか |
| 来年度のAI研修予算は？ | 資料にない情報を推測で答えないか |

余裕があれば、[04_travel_policy.txt](samples/04_travel_policy.txt) も登録してください。先ほどの講義で登場した宿泊費の例と同じ条件で、「大阪出張で1泊13,000円のホテルを使える？」と質問し、宿泊費上限と例外条件の両方が参照されているか確認できます。

## 4. うまく実装できないとき

各STEPの完成版コードが用意されています。途中からやり直す場合は、**必要なSTEPのコマンドを1つだけ**実行してください。

~~~bash
docker compose run --rm --user 0:0 app python scripts/restore_checkpoint.py step1
docker compose run --rm --user 0:0 app python scripts/restore_checkpoint.py step2
docker compose run --rm --user 0:0 app python scripts/restore_checkpoint.py step3
docker compose run --rm --user 0:0 app python scripts/restore_checkpoint.py step4
~~~

この操作は対象のコードを**上書き**します。復元時だけホストファイルへの書き込み権限を確保するためコンテナをrootで実行します。元のコードはDockerボリュームの **.data/backups/** にバックアップされます。登録済みの資料は残ります。復帰後はアプリの画面を再読み込みしてください。

エラーが表示された場合は、ログを確認できます。

~~~bash
docker compose logs --tail=100 app
~~~

Dockerコンテナが起動しているか確認するとき：

~~~bash
docker compose ps
~~~

## 5. サンプル資料

すべて演習用の架空の資料です。

| ファイル | 内容 |
| --- | --- |
| [01_ai_training.txt](samples/01_ai_training.txt) | AI研修の申込期限、開催日、費用 |
| [02_remote_work.txt](samples/02_remote_work.txt) | 在宅勤務の申請とセキュリティ |
| [03_helpdesk.txt](samples/03_helpdesk.txt) | 情報システム部のFAQ |
| [04_travel_policy.txt](samples/04_travel_policy.txt) | 国内宿泊費の上限・例外条件・精算方法 |

## 6. 利用上の注意

- **実際の社内機密文書、顧客情報、個人情報は使用しないでください。**
- 文書のEmbedding生成とChromaベクトルDBはDockerコンテナ内で動作します。
- 質問すると、検索された資料本文と質問はOpenAIまたはAnthropicのAPIへ送信されます。
- 登録したベクトルDBとダウンロード済みモデルはDockerボリュームに保存され、コンテナ停止後も残ります。
- **docker compose down --volumes** を実行すると、保存済みの資料とモデルキャッシュが両方削除されます。通常の停止には **docker compose down** を使ってください。
- このアプリは研修用の簡易実装であり、ユーザー認証やアクセス権限などの本番運用機能はありません。
- 対応するファイル形式はUTF-8のTXTファイルです。PDF読み込みは今回の実装対象に含まれません。
