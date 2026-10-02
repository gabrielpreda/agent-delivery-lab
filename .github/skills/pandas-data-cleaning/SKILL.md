---
name: pandas-data-cleaning
description: Enforce vectorized Pandas/Polars data cleaning, explicit missing value strategy, schema validation, and logging metrics.
---

# Pandas Data Cleaning Standards

When writing, updating, or refactoring data transformation and cleaning scripts using Pandas or Polars:

## 1. Vectorization Rules
- **Never use iterative loops:** Do NOT use `.iterrows()`, `.itertuples()`, or Python `for` loops to iterate over rows.
- **Prefer Vectorized Methods:** Use built-in vectorized operations, string accessor functions (`.str`), or `.apply()` only as an absolute last resort.
- For conditional column creation, use `np.select()` or `np.where()` instead of row-by-row functions.

## 2. Missing Value Handling
- Every imputation or deletion of null values MUST be explicit. Do NOT silently leave `NaN` values without comment or explicit strategy.
- Document missing data actions:
  - Numerical: Specify mean, median, forward-fill, or zero fill.
  - Categorical: Fill with explicit string category (e.g., `"UNKNOWN"` or `"UNSPECIFIED"`).
- Explicitly log missing value counts before and after cleaning:
  ```python
  import logging

  null_counts = df.isnull().sum()
  logging.info(f"Missing values before cleaning:\n{null_counts[null_counts > 0]}")
  ```

## 3. Schema & Data Type Enforcement
- Cast data types explicitly right after loading data (e.g., convert date strings to `datetime64[ns]`, categorical strings to `category` or `string` type).
- Always include a lightweight validation check or assertion on schema output using `pydantic` or `pandera` if available in the repository.

## 4. Code Structure Standard
Wrap cleaning workflows in modular functions that accept a `pd.DataFrame` and return a cleaned `pd.DataFrame`:

```python
import pandas as pd
import numpy as np
import logging

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans raw dataset by handling nulls, enforcing types, and vectorizing transformations."""
    df_clean = df.copy()

    # 1. Strip whitespaces from column names & string columns
    df_clean.columns = df_clean.columns.str.strip().str.lower().str.replace(' ', '_')

    # 2. Explicit categorical imputation
    if 'category' in df_clean.columns:
        df_clean['category'] = df_clean['category'].fillna('UNSPECIFIED').astype('string')

    # 3. Vectorized numerical clean
    if 'value' in df_clean.columns:
        df_clean['value'] = pd.to_numeric(df_clean['value'], errors='coerce')
        df_clean['value'] = df_clean['value'].fillna(df_clean['value'].median())

    return df_clean
```