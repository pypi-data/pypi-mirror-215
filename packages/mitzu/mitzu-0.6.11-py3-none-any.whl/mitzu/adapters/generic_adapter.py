from __future__ import annotations

from abc import ABC
from typing import Any, Dict, List

import mitzu.model as M
import pandas as pd

# Final Select Columns
EVENT_NAME_ALIAS_COL = "_event_name"
DATETIME_COL = "_datetime"
RETENTION_INDEX = "_ret_index"
GROUP_COL = "_group"
AGG_VALUE_COL = "_agg_value"
USER_COUNT_COL = "_user_count"


# CTE Colmns
CTE_USER_ID_ALIAS_COL = "_cte_user_id"
CTE_DATETIME_COL = "_cte_datetime"
CTE_GROUP_COL = "_cte_group"


class CloseConnectionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class GenericDatasetAdapter(ABC):
    def __init__(self, project: M.Project):
        self.project = project

    def execute_query(self, query: Any) -> pd.DataFrame:
        raise NotImplementedError()

    def list_fields(self, event_data_table: M.EventDataTable) -> List[M.Field]:
        """Returns all fields including structs and map keys for an Event Data Table
        It requires running SQL query for Map type discovery
        """
        raise NotImplementedError()

    def list_all_table_columns(self, schema: str, table_name: str) -> List[M.Field]:
        """Returns physical columns including structs for a table"""
        raise NotImplementedError()

    def get_distinct_event_names(self, event_data_table: M.EventDataTable) -> List[str]:
        raise NotImplementedError()

    def get_field_enums(
        self,
        event_data_table: M.EventDataTable,
        fields: List[M.Field],
    ) -> Dict[str, M.EventDef]:
        raise NotImplementedError()

    def list_schemas(self) -> List[str]:
        raise NotImplementedError()

    def list_tables(self, schema: str) -> List[str]:
        raise NotImplementedError()

    def get_conversion_sql(self, metric: M.ConversionMetric) -> str:
        raise NotImplementedError()

    def get_conversion_df(self, metric: M.ConversionMetric) -> pd.DataFrame:
        raise NotImplementedError()

    def get_segmentation_sql(self, metric: M.SegmentationMetric) -> str:
        raise NotImplementedError()

    def get_segmentation_df(self, metric: M.SegmentationMetric) -> pd.DataFrame:
        raise NotImplementedError()

    def get_retention_sql(self, metric: M.RetentionMetric) -> str:
        raise NotImplementedError()

    def get_retention_df(self, metric: M.RetentionMetric) -> pd.DataFrame:
        raise NotImplementedError()

    def test_connection(self):
        raise NotImplementedError()

    def stop_current_execution(self):
        raise NotImplementedError()
