import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict
import io
import base64

def create_knowledge_graph(sections: List[Dict]) -> str:
    """Generate base64 encoded knowledge graph image"""
    G = nx.Graph()
    
    # Add nodes (entities/concepts)
    entities = set()
    for section in sections:
        for word in section["title"].split() + section["content"].split()[:20]:
            if word.isalpha() and len(word) > 3:
                entities.add(word.lower())
    
    G.add_nodes_from(list(entities)[:15])  # Limit for visualization
    
    # Add edges (co-occurrence)
    for i, entity1 in enumerate(G.nodes()):
        for entity2 in list(G.nodes())[i+1:]:
            if entity1 in entity2 or entity2 in entity1:
                G.add_edge(entity1, entity2, weight=2)
            elif len(set(entity1) & set(entity2)) > 2:
                G.add_edge(entity1, entity2, weight=1)
    
    # Draw graph
    plt.figure(figsize=(10,8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, 
           node_color="skyblue", font_size=8)
    
    # Convert to base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')