from dataclasses import dataclass
from typing import Optional

@dataclass
class PrepConfig:
    invoice_col: str = "InvoiceNo"
    item_col: str = "Description"
    qty_col: str = "Quantity"
    country_col: Optional[str] = "Country"

    drop_canceled_invoices: bool = True
    canceled_prefix: str = "C"  # UCI Online Retail uses 'C' prefix for cancellations
    drop_missing_items: bool = True # drop missing rows
    require_positive_qty: bool = True   # remove returns/neg qty

    normalize_items_upper: bool = True
    strip_item_whitespace: bool = True

    # Optional filters
    country_filter: Optional[str] = None
    top_k_items: Optional[int] = 300  # keep top-K most frequent items 

@dataclass
class MiningConfig:
    min_support: float = 0.01
    min_lift: float = 1.2
    min_confidence: float = 0.3
    network_max_rules: int = 25
    top_rules_bar_n: int = 10
