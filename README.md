# Market Basket Analysis (FP-Growth + Association Rules)

This project mines frequent itemsets using **FP-Growth** and generates **association rules** (**support / confidence / lift**) from transaction data, with visualizations and actionable insights
(e.g., bundling + cross-sell opportunities).

## Dataset
Designed for the **UCI Online Retail** dataset. Place the file in `data/` (gitignored) and point the script/notebook to it.

Expected columns:
- `InvoiceNo` (transaction ID)
- `Description` (item name)
- `Quantity` (positive values represent purchased items)

## What this project does
- Cleans transactions (drops cancellations/returns, normalizes product names)
- Builds a boolean basket matrix (transactions × items)
- Mines frequent itemsets via FP-Growth (`min_support`)
- Generates association rules and filters by confidence/lift
- Produces plots for rule exploration and reporting

## Quick start (recommended: virtual env)
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

## Run as a script
python run_pipeline.py --input "data/Online Retail.xlsx" --min_support 0.01 --min_conf 0.3 --min_lift 1.2 --top_k 300

## Outputs
- figures/support_confidence_bubble.png
- figures/top_rules_by_lift.png
- figures/rules_network.png (if single-item rules exist)

## Run as a notebook
Open: notebooks/Market_Basket_FP_Growth.ipynb

## Results (example insights)

Partyware bundle: Napkins + cups strongly predict plates (confidence ≈ 0.90, lift ≈ 30.56) → “Complete the set” bundling.

Toy line cross-sell: POPPY’S PLAYHOUSE items show strong two-way co-purchase (confidence ≈ 0.72–0.74, lift ≈ 30.53) → “Frequently bought together”.

Interpretation: Lift is very high (~29–31) while support is modest (~1–2%), indicating strong but segment-specific co-purchase patterns.

## Notes
- Tune min_support first (e.g., 0.02 → 0.01 → 0.005) depending on dataset size.
- For nicer results, restrict to a country/segment or keep only the top-K most frequent items.
- Association rules indicate co-occurrence, not causation.
