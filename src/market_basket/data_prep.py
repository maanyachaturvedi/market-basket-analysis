import pandas as pd
from .config import PrepConfig

def load_dataset(path: str) -> pd.DataFrame:
    """Load an Excel or CSV dataset by file extension."""
    lower = path.lower()
    if lower.endswith((".xlsx", ".xls")):
        return pd.read_excel(path)
    if lower.endswith(".csv"):
        return pd.read_csv(path)
    raise ValueError(f"Unsupported file type for: {path}. Use .xlsx/.xls or .csv")

def clean_transactions(df: pd.DataFrame, cfg: PrepConfig) -> pd.DataFrame:
    """Clean and normalize transaction rows."""
    required = [cfg.invoice_col, cfg.item_col]
    if cfg.qty_col:
        required.append(cfg.qty_col)
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns: {missing}. Found: {list(df.columns)}")

    out = df.copy()

    # Basic NA cleanup
    out = out.dropna(subset=[cfg.invoice_col, cfg.item_col])

    # Quantity filter (remove returns/negatives)
    if cfg.qty_col in out.columns:
        out = out[out[cfg.qty_col] > 0]

    # Invoice normalization
    out[cfg.invoice_col] = out[cfg.invoice_col].astype(str)

    # Remove canceled invoices (common in Online Retail)
    if cfg.drop_canceled_invoices and cfg.canceled_prefix:
        out = out[~out[cfg.invoice_col].str.startswith(cfg.canceled_prefix)]

    # Country filter
    if cfg.country_filter and cfg.country_col and cfg.country_col in out.columns:
        out = out[out[cfg.country_col] == cfg.country_filter]

    # Normalize item names
    if cfg.strip_item_whitespace:
        out[cfg.item_col] = out[cfg.item_col].astype(str).str.strip()
    if cfg.normalize_items_upper:
        out[cfg.item_col] = out[cfg.item_col].astype(str).str.upper()

    # Top-K items filter for cleaner outputs
    if cfg.top_k_items is not None and cfg.top_k_items > 0:
        top_items = out[cfg.item_col].value_counts().head(cfg.top_k_items).index
        out = out[out[cfg.item_col].isin(top_items)]

    return out

def make_basket_matrix(df: pd.DataFrame, cfg: PrepConfig) -> pd.DataFrame:
    """Create a boolean basket matrix: rows=transactions, cols=items."""
    basket = (
        df.groupby([cfg.invoice_col, cfg.item_col])[cfg.qty_col]
          .sum()
          .unstack(fill_value=0)
    )
    return (basket > 0).astype(bool)
