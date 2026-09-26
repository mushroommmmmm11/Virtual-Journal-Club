# Virtual Journal Club

一个“你来讲论文，AI 组员负责追问”的语音优先虚拟组会。

## v0.1 已实现

- PDF 上传、文本解析和轻量检索
- 5 个科研角色：PI / ML Reviewer / Biology Reviewer / Statistician / Reviewer #2
- Moderator 路由：根据你的汇报内容选择最合适的提问者
- 三种模式：Journal Club / Presentation / Defense
- 浏览器语音输入（Chrome / Edge Web Speech API）
- 浏览器 TTS 朗读 AI 问题
- OpenAI 模型后端（通过环境变量配置）
- 自动导出 weekly_meeting.md
- Docker 启动
- 无 API Key 时仍可进入 fallback 训练模式

> v0.1 先跑通“你讲 → AI 听 → 论文上下文 → reviewer 追问 → 你继续答”的完整闭环。低延迟 realtime audio、Figure/PPT 感知会放到下一阶段。

## 快速启动

### 本地 Python

1. clone 仓库并进入目录。
2. 创建 Python 3.12 虚拟环境。
3. 安装 requirements.txt。
4. 把 .env.example 复制为 .env，并填入 OPENAI_API_KEY 与 OPENAI_MODEL。
5. 运行：uvicorn backend.main:app --reload
6. 浏览器打开：http://127.0.0.1:8000

Windows PowerShell 示例：

    git clone https://github.com/mushroommmmmm11/Virtual-Journal-Club.git
    cd Virtual-Journal-Club
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    copy .env.example .env
    uvicorn backend.main:app --reload

### Docker

    docker build -t virtual-journal-club .
    docker run --rm -p 8000:8000 --env-file .env virtual-journal-club

## 推荐使用流程

1. 上传本周重点论文 PDF。
2. 选择 Journal Club。
3. 打开麦克风，先自己讲：Problem → Gap → Hypothesis → Method → Experiment → Evidence。
4. 每讲完一个完整观点点“发送这一段”。
5. Moderator 自动选择 reviewer，只允许一个 agent 提一个问题。
6. 你先回答；AI 默认采用追问/提示，而不是直接把答案喂给你。
7. 最后导出 Markdown，补完 Reflection。

## 三种模式

### Journal Club
训练你重建论文的科研逻辑：Problem → Gap → Hypothesis → Method → Experiment → Evidence。

### Presentation
以连续汇报为主；Reviewer 尽量少打断，只对关键逻辑漏洞、过度解读和重要 claim 提问。

### Defense
模拟答辩；问题更尖锐，强调设计选择、替代解释、实验充分性和证据边界。

## 当前架构

    Browser microphone / text
            |
            v
      FastAPI /api/talk
            |
            v
      Moderator router
            |
      PI / ML / Biology / Stats / Reviewer #2
            |
            v
      Paper retrieval
            |
            v
        LLM response
            |
            v
      Browser TTS + transcript

## 下一阶段（v0.2）

- WebSocket + VAD 真正 realtime streaming audio
- Figure / Table 图像输入
- PPT 当前页感知
- PDF section / figure caption 结构化索引
- reviewer follow-up 状态机
- “追问 → 提示 → 再提示 → 最后解释”的 Socratic ladder
- 会后自动生成 Paper of the Week / Weakness / New Hypothesis / Next Experiment
- 每周文献 inbox 与阅读计划

## 设计原则

这个项目不是“AI 替你读论文”。它的目标是制造一个外部机制，反复逼你回答：

- 为什么这是一个 scientific question？
- 证据在哪里？
- 这个实验究竟证明了什么？
- 有没有替代解释？
- 如果核心假设不成立，方法还剩下什么？

因此默认一次只允许一个 reviewer 问一个问题。