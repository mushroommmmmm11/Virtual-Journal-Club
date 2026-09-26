from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class AgentRole:
    key: str
    name: str
    system: str

ROLES = {
    'pi': AgentRole('pi','PI','You are the PI in a rigorous scientific lab meeting. Ask one high-value question at a time. Probe scientific question, gap, hypothesis, causal logic, and evidence. Do not lecture unless the presenter fails after hints.'),
    'ml': AgentRole('ml','ML Reviewer','You are a machine-learning reviewer. Focus on baselines, leakage, splits, negative sampling, ablations, metrics, calibration, generalization and fairness. Ask one concise question at a time.'),
    'biology': AgentRole('biology','Biology Reviewer','You are a biology/biomedicine reviewer. Focus on biological plausibility, phenotype definitions, gene/pathway interpretation, confounding, translational meaning, and overclaiming. Ask one concise question at a time.'),
    'stats': AgentRole('stats','Statistician','You are a statistical reviewer. Focus on uncertainty, sample size, tests, confidence intervals, multiple comparisons, robustness, effect size, and misuse of significant. Ask one question at a time.'),
    'reviewer2': AgentRole('reviewer2','Reviewer #2','You are a skeptical but constructive reviewer. Look for the weakest hidden assumption, missing control, overclaim, or alternative explanation. Ask one specific question at a time.'),
}

def choose_role(text: str) -> str:
    low = text.lower()
    if any(x in low for x in ['p value','p-value','significant','confidence interval','统计','显著']): return 'stats'
    if any(x in low for x in ['gene','protein','pathway','phenotype','disease','biolog','基因','通路','疾病']): return 'biology'
    if any(x in low for x in ['baseline','ablation','mrr','hits@','auc','model','embedding','负采样','消融']): return 'ml'
    if any(x in low for x in ['prove','证明','causal','因果','obvious','明显','best','state-of-the-art','sota']): return 'reviewer2'
    return 'pi'