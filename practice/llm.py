"""OpenAI / Anthropicに対する最小限のテキスト生成インターフェース。"""
import os

from practice import settings


def generate_reply(
    messages: list[dict[str, str]],
    *,
    system_prompt: str = "あなたは日本語で簡潔に回答するアシスタントです。",
) -> str:
    """roleとcontentのリストを送り、生成された本文を返す。"""
    problem = settings.check_api_settings()
    if problem:
        raise ValueError(problem)
    if not messages:
        raise ValueError("送信するメッセージがありません。")

    history = [
        {"role": item["role"], "content": item["content"]}
        for item in messages
        if item["role"] in {"user", "assistant"}
    ]

    if settings.PROVIDER == "openai":
        from openai import OpenAI

        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        result = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "system", "content": system_prompt}, *history],
            max_completion_tokens=512,
        )
        return result.choices[0].message.content or "回答を生成できませんでした。"

    from anthropic import Anthropic

    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    result = client.messages.create(
        model=settings.ANTHROPIC_MODEL,
        system=system_prompt,
        messages=history,
        max_tokens=512,
    )
    return "".join(block.text for block in result.content if block.type == "text") or "回答を生成できませんでした。"
