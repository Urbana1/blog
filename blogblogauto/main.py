import openai
import os
import toml
from datetime import datetime

# 設定読み込み
config = toml.load("settings.toml")

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_article(topic, offer):
    prompt = f"{topic} についてブログ記事を書いてください。最後にハピタスのリンク（{offer}）を紹介文に入れてください。"
    response = openai.ChatCompletion.create(
        model=config["openai"]["model"],
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

def main():
    topic = config["runtime"]["topic"]
    offer = config["runtime"]["offer"]
    dry_run = config["runtime"]["dry_run"]

    article = generate_article(topic, offer)

    if dry_run:
        # ローカル用にHTMLファイルを保存
        filename = f"dryrun_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"<html><body><h1>{topic}</h1><p>{article}</p></body></html>")
        print(f"[DRY RUN] 記事を生成しました: {filename}")
    else:
        # 本番ならここでブログAPIに投稿処理を書く
        print("記事を生成しました（本番モード）:")
        print(article)

if __name__ == "__main__":
    main()
