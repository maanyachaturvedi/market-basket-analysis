import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules
from .config import MiningConfig

def mine_itemsets_fp_growth(basket: pd.DataFrame, cfg: MiningConfig) -> pd.DataFrame:
    """Mine frequent itemsets using FP-Growth."""
    itemsets = fpgrowth(basket, min_support=cfg.min_support, use_colnames=True)
    if itemsets.empty:
        return itemsets
    itemsets["length"] = itemsets["itemsets"].apply(len)
    itemsets = itemsets.sort_values(["support", "length"], ascending=[False, True]).reset_index(drop=True)
    return itemsets

def mine_rules(itemsets: pd.DataFrame, cfg: MiningConfig) -> pd.DataFrame:
    """Generate association rules and filter for interesting ones."""
    if itemsets is None or itemsets.empty:
        return pd.DataFrame()

    rules = association_rules(itemsets, metric="lift", min_threshold=cfg.min_lift)
    if rules.empty:
        return rules

    rules["antecedents_str"] = rules["antecedents"].apply(lambda s: ", ".join(sorted(list(s))))
    rules["consequents_str"] = rules["consequents"].apply(lambda s: ", ".join(sorted(list(s))))
    rules_f = rules[(rules["confidence"] >= cfg.min_confidence) & (rules["lift"] >= cfg.min_lift)].copy()
    rules_f = rules_f.sort_values(["lift", "confidence"], ascending=False).reset_index(drop=True)
    return rules_f
