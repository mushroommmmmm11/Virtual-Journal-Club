from backend.agents import choose_role
from backend.paper import PaperStore, PaperChunk

def test_role_routing():
    assert choose_role('MRR improved after the ablation') == 'ml'
    assert choose_role('the gene pathway is biologically plausible') == 'biology'
    assert choose_role('the result is statistically significant') == 'stats'

def test_paper_search():
    p=PaperStore()
    p.chunks=[PaperChunk(1,'knowledge graph embeddings for epilepsy'),PaperChunk(2,'unrelated control text')]
    assert p.search('epilepsy knowledge graph',1)[0].page == 1