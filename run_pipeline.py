import argparse
import os

from market_basket.config import PrepConfig, MiningConfig
from market_basket.data_prep import load_dataset, clean_transactions, make_basket_matrix
from market_basket.mining import mine_itemsets_fp_growth, mine_rules
from market_basket.viz import (
    plot_support_confidence_bubble,
    plot_top_rules_by_lift,
    plot_rules_network_single_item,
)

def main():
    parser = argparse.ArgumentParser(description="Market Basket Analysis (FP-Growth + Association Rules)")
    parser.add_argument("--input", required=True, help="Path to dataset (.xlsx/.xls/.csv)")
    parser.add_argument("--country", default=None, help="Optional country filter (if column exists)")
    parser.add_argument("--top_k", type=int, default=300, help="Keep only top-K items by frequency (0/None = keep all)")
    parser.add_argument("--min_support", type=float, default=0.01)
    parser.add_argument("--min_conf", type=float, default=0.3)
    parser.add_argument("--min_lift", type=float, default=1.2)
    args = parser.parse_args()

    prep_cfg = PrepConfig(country_filter=args.country, top_k_items=(args.top_k if args.top_k and args.top_k > 0 else None))
    mining_cfg = MiningConfig(min_support=args.min_support, min_confidence=args.min_conf, min_lift=args.min_lift)

    df = load_dataset(args.input)
    df = clean_transactions(df, prep_cfg)
    basket = make_basket_matrix(df, prep_cfg)

    print("Basket shape:", basket.shape)

    itemsets = mine_itemsets_fp_growth(basket, mining_cfg)
    print("Frequent itemsets:", len(itemsets))
    if not itemsets.empty:
        print(itemsets.head(10))

    rules = mine_rules(itemsets, mining_cfg)
    print("Filtered rules:", len(rules))
    if not rules.empty:
        print(rules[["antecedents_str","consequents_str","support","confidence","lift"]].head(10))

    os.makedirs("figures", exist_ok=True)
    plot_support_confidence_bubble(rules, "figures/support_confidence_bubble.png")
    plot_top_rules_by_lift(rules, mining_cfg, "figures/top_rules_by_lift.png")
    fig = plot_rules_network_single_item(rules, mining_cfg, "figures/rules_network.png")
    if fig is None:
        print("No single-item rules available for the network plot under current thresholds.")

if __name__ == "__main__":
    main()
