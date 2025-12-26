import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from .config import MiningConfig

def plot_support_confidence_bubble(rules: pd.DataFrame, out_path: str | None = None):
    """Scatter: support vs confidence, bubble size ~ lift."""
    if rules is None or rules.empty:
        return None

    plt.figure()
    sizes = 80 * np.clip(rules["lift"].to_numpy(), 1, 10)  # cap bubble size for readability
    plt.scatter(rules["support"], rules["confidence"], s=sizes, alpha=0.6)
    plt.xlabel("Support")
    plt.ylabel("Confidence")
    plt.title("Association Rules: Support vs Confidence (bubble ~ Lift)")
    plt.tight_layout()

    if out_path:
        plt.savefig(out_path, dpi=200)
    return plt.gcf()

def plot_top_rules_by_lift(rules: pd.DataFrame, cfg: MiningConfig, out_path: str | None = None):
    """Horizontal bar chart of top-N rules by lift."""
    if rules is None or rules.empty:
        return None

    top_rules = rules.head(cfg.top_rules_bar_n).copy()
    labels = (top_rules["antecedents_str"] + " → " + top_rules["consequents_str"]).tolist()

    plt.figure(figsize=(10, max(4, 0.5 * len(top_rules))))
    plt.barh(range(len(top_rules)), top_rules["lift"])
    plt.yticks(range(len(top_rules)), labels)
    plt.xlabel("Lift")
    plt.title(f"Top {len(top_rules)} Association Rules by Lift")
    plt.gca().invert_yaxis()
    plt.tight_layout()

    if out_path:
        plt.savefig(out_path, dpi=200)
    return plt.gcf()

def plot_rules_network_single_item(rules: pd.DataFrame, cfg: MiningConfig, out_path: str | None = None):
    """Network graph for single-item antecedent → single-item consequent rules."""
    if rules is None or rules.empty:
        return None

    G = nx.DiGraph()
    edges_to_plot = rules.head(cfg.network_max_rules)

    for _, r in edges_to_plot.iterrows():
        if len(r["antecedents"]) == 1 and len(r["consequents"]) == 1:
            a = next(iter(r["antecedents"]))
            c = next(iter(r["consequents"]))
            G.add_edge(a, c, weight=float(r["lift"]))

    if G.number_of_edges() == 0:
        return None

    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=900, font_size=7, arrows=True)
    plt.title("Top Association Rules Network (single-item rules)")
    plt.tight_layout()

    if out_path:
        plt.savefig(out_path, dpi=200)
    return plt.gcf()
