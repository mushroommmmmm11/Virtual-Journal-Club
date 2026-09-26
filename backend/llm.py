from __future__ import annotations
from openai import AsyncOpenAI
from .config import settings

class LLM:
    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    async def ask(self, system: str, user: str) -> str:
        if not self.client:
            return '我还没有配置模型 API。先按组会规则追问你一句：你刚才这段话里，哪一个结论是由实验直接支持的，哪一个只是你的推断？'
        r = await self.client.responses.create(
            model=settings.openai_model,
            instructions=system,
            input=user,
        )
        return r.output_text.strip()

llm = LLM()