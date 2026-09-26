from __future__ import annotations
from pathlib import Path
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .meeting import MeetingSession, MODES
from .paper import PaperStore

ROOT = Path(__file__).resolve().parents[1]
UPLOADS = ROOT / 'uploads'
OUTPUTS = ROOT / 'outputs'
UPLOADS.mkdir(exist_ok=True)
OUTPUTS.mkdir(exist_ok=True)

app = FastAPI(title='Virtual Journal Club', version='0.1.0')
paper = PaperStore()
session = MeetingSession(paper=paper)

class TalkRequest(BaseModel):
    text: str

class ModeRequest(BaseModel):
    mode: str

@app.get('/api/health')
async def health():
    return {'ok': True, 'paper': paper.title or None, 'mode': session.mode}

@app.post('/api/paper')
async def upload_paper(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith('.pdf'):
        raise HTTPException(400, 'Please upload a PDF.')
    path = UPLOADS / f'{uuid.uuid4().hex}.pdf'
    path.write_bytes(await file.read())
    info = paper.load_pdf(path)
    session.turns.clear()
    return info

@app.post('/api/mode')
async def set_mode(req: ModeRequest):
    if req.mode not in MODES:
        raise HTTPException(400, f'mode must be one of {sorted(MODES)}')
    session.mode = req.mode
    return {'mode': session.mode}

@app.post('/api/talk')
async def talk(req: TalkRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(400, 'Empty presenter text.')
    return await session.handle_presenter(text)

@app.get('/api/export', response_class=PlainTextResponse)
async def export():
    md = session.export_markdown()
    path = OUTPUTS / 'weekly_meeting.md'
    path.write_text(md, encoding='utf-8')
    return md

app.mount('/', StaticFiles(directory=ROOT / 'frontend', html=True), name='frontend')