from __future__ import annotations

from datetime import datetime
from typing import Optional

import mitzu.adapters.generic_adapter as GA
import pandas as pd
import json


def str_to_datetime(val: str | pd.Timestamp) -> Optional[datetime]:
    if val is None:
        return None
    if type(val) == str:
        return datetime.fromisoformat(val)
    elif type(val) == pd.Timestamp:
        return val.to_pydatetime()
    raise ValueError(f"invalid datetime type: {type(val)}")


def dataframe_str_to_datetime(pdf: pd.DataFrame, column: str) -> pd.DataFrame:
    pdf[column] = pdf[column].apply(str_to_datetime)
    return pdf


def pdf_string_json_array_to_array(pdf: pd.DataFrame):
    for col in pdf.columns:
        if col != GA.EVENT_NAME_ALIAS_COL:
            pdf[col] = pdf[col].apply(
                lambda val: json.loads(val) if type(val) == str else val
            )
    return pdf
