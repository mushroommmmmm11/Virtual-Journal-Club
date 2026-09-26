from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from .agents import ROLES, choose_role
from .llm import llm
from .paper import PaperStore

MODES = {'presentation', 'defense', 'journal_club'}

@dataclass
class Turn:
    speaker: str
    text: str

@dataclass
class MeetingSession:
    paper: PaperStore
    mode: str = 'journal_club'
    turns: list[Turn] = field(default_factory=list)

    async def handle_presenter(self, text: str) -> dict:
        self.turns.append(Turn('Presenter', text))
        role_key = choose_role(text)
        role = ROLES[role_key]
        context = self.paper.search(text, 4)
        paper_context = '\n\n'.join(f'[p.{c.page}] {c.text}' for c in context)
        mode_rule = {
            'presentation': 'Interrupt only for a major scientific flaw or overclaim; otherwise ask a short clarifying question.',
            'defense': 'Act like a thesis defense. Ask a demanding question and follow the answer rather than giving a mini-lecture.',
            'journal_club': 'Train the presenter to reconstruct Problem -> Gap -> Hypothesis -> Method -> Experiment -> Evidence.'
        }[self.mode]
        user = (
            f'Mode: {self.mode}\nRule: {mode_rule}\n\nPresenter said:\n{text}\n\n'
            f'Relevant paper excerpts:\n{paper_context or "(No paper loaded yet.)"}\n\n'
            'Ask exactly ONE question. Prefer Socratic probing. If the presenter appears unsure, give a hint before explaining.'
        )
        reply = await llm.ask(role.system, user)
        self.turns.append(Turn(role.name, reply))
        return {'agent': role.name, 'role': role_key, 'message': reply}

    def export_markdown(self) -> str:
        stamp = datetime.now().strftime('%Y-%m-%d')
        lines = [
            f'# Weekly Research Meeting — {stamp}',
            '',
            f'- Mode: {self.mode}',
            f'- Paper: {self.paper.title or "Not loaded"}',
            '',
            '## Transcript',
            ''
        ]
        for t in self.turns:
            lines += [f'**{t.speaker}:** {t.text}', '']
        lines += [
            '## Reflection','',
            '- Scientific question:',
            '- Gap:',
            '- Hypothesis:',
            '- Key experiment:',
            '- Main evidence:',
            '- Weakest point:',
            '- What I learned:',
            '- Connection to my project:',
            '- Experiment to try next:'
        ]
        return '\n'.join(lines)