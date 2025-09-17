# NotebookLM 自動検索

このスクリプトは、Playwrightを利用してNotebookLMの検索を自動化します。

## プロジェクト構造

プロジェクトは以下のファイルに分割されています。

- `main.py`: メインの実行スクリプト。他のモジュールをインポートして処理を調整します。
- `config.py`: 設定情報（パス、URL、セレクタ、タイムアウトなど）を定義します。
- `auth.py`: Googleアカウントへのログイン処理を担当します。
- `project_manager.py`: NotebookLMのプロジェクト一覧の取得を担当します。
- `search_automation.py`: 検索の実行と結果の保存を担当します。
- `requirements.txt`: 必要なPythonライブラリをリストします。
- `.gitignore`: Gitで無視するファイルを指定します。

## 使い方

### 0. Conda環境の構築

以下の手順で仮想環境を構築し、アクティベートしてください。

```bash
conda create -n NotebookAutoSearch python=3.12  # 環境名とPythonバージョンは適宜変更してください
conda activate NotebookAutoSearch
```

### 1. 依存関係のインストール

まず、必要なライブラリをインストールします。

```bash
pip install -r requirements.txt
playwright install
```

### 2. 初回セットアップ

以下のコマンドを実行して、ブラウザでGoogleアカウントにログインします。認証情報が `./secure/user_data` ディレクトリに保存されます。

```bash
python main.py setup
```

実行するとブラウザが起動するので、手動でログインしてください。ログインが完了すると、このスクリプトは自動で終了します。

### 3. プロジェクト一覧の表示

以下のコマンドで、利用可能なプロジェクトの一覧を表示できます。

```bash
python main.py list
```

### 4. 検索の実行

プロジェクト名と検索したい言葉を指定して、検索を実行します。

```bash
python main.py search "プロジェクト名" "検索したい言葉"
```

複数の言葉で検索することも可能です。

```bash
python main.py search "プロジェクト名" "言葉1" "言葉2"
```

検索結果は、`output` ディレクトリにMarkdownファイルとして保存されます。
