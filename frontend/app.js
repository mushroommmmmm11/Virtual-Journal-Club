const $ = (id) => document.getElementById(id);
let recognizing = false;
let recognition = null;

function addMsg(who, text, ai=false){
  const d=document.createElement('div');
  d.className='msg'+(ai?' ai':'');
  const w=document.createElement('div'); w.className='who'; w.textContent=who;
  const t=document.createElement('div'); t.textContent=text;
  d.appendChild(w); d.appendChild(t); $('chat').appendChild(d); d.scrollIntoView();
}

$('upload').onclick = async () => {
  const f=$('pdf').files[0]; if(!f) return alert('先选择 PDF');
  const fd=new FormData(); fd.append('file',f);
  $('paperStatus').textContent='解析中…';
  const r=await fetch('/api/paper',{method:'POST',body:fd});
  const j=await r.json();
  $('paperStatus').textContent=r.ok?(j.title+' · '+j.pages+' 页'):(j.detail||'上传失败');
};

$('mode').onchange = async () => {
  await fetch('/api/mode',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mode:$('mode').value})});
};

$('send').onclick = async () => {
  const text=$('text').value.trim(); if(!text) return;
  addMsg('Presenter',text); $('text').value='';
  const r=await fetch('/api/talk',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:text})});
  const j=await r.json();
  if(!r.ok) return addMsg('System',j.detail||'请求失败',true);
  addMsg(j.agent,j.message,true);
  if('speechSynthesis' in window){const u=new SpeechSynthesisUtterance(j.message);u.lang='zh-CN';speechSynthesis.speak(u);}
};

const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
if(SR){
  recognition=new SR(); recognition.lang='zh-CN'; recognition.continuous=true; recognition.interimResults=true;
  recognition.onresult=(e)=>{
    let finalText=''; let interim='';
    for(let i=e.resultIndex;i<e.results.length;i++){const t=e.results[i][0].transcript;if(e.results[i].isFinal)finalText+=t;else interim+=t;}
    if(finalText) $('text').value += finalText;
    $('mic').textContent=interim?('🎙️ '+interim.slice(0,18)):'⏹ 停止语音';
  };
  recognition.onend=()=>{recognizing=false;$('mic').textContent='🎙️ 开始语音';};
}
$('mic').onclick=()=>{
  if(!recognition)return alert('当前浏览器不支持 Web Speech API，请使用 Chrome/Edge 或直接输入文字。');
  if(recognizing){recognition.stop();recognizing=false;}else{recognition.start();recognizing=true;$('mic').textContent='⏹ 停止语音';}
};

$('export').onclick=async()=>{const r=await fetch('/api/export');$('md').textContent=await r.text();};