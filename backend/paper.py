from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re
import fitz

@dataclass
class PaperChunk:
    page: int
    text: str

class PaperStore:
    def __init__(self) -> None:
        self.title: str = ''
        self.chunks: list[PaperChunk] = []

    def load_pdf(self, path: str | Path) -> dict:
        doc = fitz.open(path)
        chunks: list[PaperChunk] = []
        for idx, page in enumerate(doc):
            text = re.sub(r'\s+', ' ', page.get_text('text')).strip()
            if text:
                for start in range(0, len(text), 1800):
                    chunks.append(PaperChunk(page=idx + 1, text=text[start:start+1800]))
        self.chunks = chunks
        self.title = Path(path).stem
        return {'title': self.title, 'pages': len(doc), 'chunks': len(chunks)}

    def search(self, query: str, k: int = 5) -> list[PaperChunk]:
        if not self.chunks:
            return []
        terms = {t.lower() for t in re.findall(r'[A-Za-z0-9_\-]+', query) if len(t) > 2}
        def score(chunk: PaperChunk) -> int:
            low = chunk.text.lower()
            return sum(low.count(t) for t in terms)
        ranked = sorted(self.chunks, key=score, reverse=True)
        return [c for c in ranked[:k] if score(c) > 0] or ranked[:min(k, len(ranked))]