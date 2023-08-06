from __future__ import annotations

import traceback
from typing import Any, Dict, Optional
import dash.development.base_component as bc
import dash_bootstrap_components as dbc
import mitzu.model as M
import mitzu.webapp.pages.explore.toolbar_handler as TH
import mitzu.webapp.pages.explore.explore_page as EXP
import mitzu.webapp.configs as configs
import mitzu.webapp.dependencies as DEPS
import mitzu.webapp.storage as S
import mitzu.webapp.cache as C
import mitzu.visualization.common as CO
import mitzu.webapp.pages.paths as P
import mitzu.webapp.model as WM
import mitzu.serialization as SE
from mitzu.webapp.helper import MITZU_LOCATION
import mitzu.webapp.onboarding_flow as OF

import pandas as pd
from dash import Input, Output, State, ctx, dcc, html, callback, no_update, dash_table
from mitzu.webapp.helper import get_final_all_inputs
from mitzu.webapp.auth.decorator import restricted
import mitzu.visualization.plot as PLT
import mitzu.visualization.charts as CHRT
import json
import hashlib
from urllib.parse import urlparse
from datetime import datetime
import mitzu.webapp.service.tracking_service as TS

GRAPH = "graph"
MESSAGE = "lead fw-normal text-center h-100 w-100"
TABLE = "explore_results_table"
SQL_AREA = "sql_area"


CONTENT_STYLE = {
    "min-height": "200px",
    "max-height": "700px",
    "overflow": "auto",
}

DF_CACHE: Dict[int, pd.DataFrame] = {}
MARKDOWN = """```sql
{sql}
```"""

GRAPH_CONTAINER = (
    "graph_container d-flex justify-content-stretch align-items-center pt-3"
)
GRAPH_REFRESHER_INTERVAL = "graph_refresher_interval"


def create_graph_container() -> bc.Component:
    return html.Div(
        id=GRAPH_CONTAINER,
        children=[],
        className=GRAPH_CONTAINER,
    )


def create_metric_hash_key(metric: M.Metric) -> str:
    metric_dict = SE.to_dict(metric)

    #  We need to remove these keys from the metric dict as changes in these shouldn't trigger reexecution
    metric_dict["co"]["mn"] = None
    metric_dict["co"]["mgc"] = None
    metric_dict["co"]["ct"] = None
    metric_dict["co"]["cat"] = None
    metric_dict["id"] = None
    # The project_id is not part of the query param, but the path.
    # However we need to use the ID as well for caching, some project may contain the same events.
    metric_dict["prj"] = metric.get_project().get_id()

    return hashlib.md5(json.dumps(metric_dict).encode("ascii")).hexdigest()


def get_metric_result_df(
    hash_key: str,
    metric: M.Metric,
    mitzu_cache: C.MitzuCache,
    tracking_service: TS.TrackingService,
) -> pd.DataFrame:
    start_time = datetime.now().timestamp()
    result_df = mitzu_cache.get(hash_key)
    from_cache = True
    if result_df is None:
        from_cache = False
        result_df = metric.get_df()
        mitzu_cache.put(hash_key, result_df, expire=configs.CACHE_EXPIRATION)
    duration = datetime.now().timestamp() - start_time
    tracking_service.track_explore_finished(
        metric, duration_seconds=duration, from_cache=from_cache
    )
    return result_df


def create_graph(
    metric: Optional[M.Metric],
    simple_chart: CO.SimpleChart,
) -> Optional[dcc.Graph]:
    if metric is None:
        return html.Div("Select the first event...", id=GRAPH, className=MESSAGE)

    if (
        (isinstance(metric, M.SegmentationMetric) and metric._segment is None)
        or (
            isinstance(metric, M.ConversionMetric)
            and len(metric._conversion._segments) == 0
        )
        or (isinstance(metric, M.RetentionMetric) and metric._initial_segment is None)
    ):
        return html.Div("Select the first event...", id=GRAPH, className=MESSAGE)

    fig = PLT.plot_chart(simple_chart, metric)
    return dcc.Graph(
        id=GRAPH, className="w-100", figure=fig, config={"displayModeBar": False}
    )


def create_table(
    metric: Optional[M.Metric],
    hash_key: str,
    mitzu_cache: C.MitzuCache,
    tracking_service: TS.TrackingService,
) -> Optional[dbc.Table]:
    if metric is None:
        return None

    result_df = get_metric_result_df(hash_key, metric, mitzu_cache, tracking_service)
    result_df = result_df.sort_values(by=[result_df.columns[0], result_df.columns[1]])
    result_df.columns = [col[1:].replace("_", " ").title() for col in result_df.columns]
    table = dash_table.DataTable(
        id=TABLE,
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False}
            for i in result_df.columns
        ],
        data=result_df.to_dict("records"),
        editable=False,
        sort_action="native",
        sort_mode="single",
        filter_action="native",
        export_columns="all",
        export_headers="names",
        export_format="csv",
        page_size=20,
        style_cell={"padding": "10px", "fontFamily": "var(--mdb-font-sans-serif)"},
        style_header={
            "backgroundColor": "var(--mdb-gray-100)",
            "fontWeight": "bold",
        },
    )

    return table


def create_sql_area(metric: Optional[M.Metric]) -> dbc.Table:
    if metric is not None:
        return dcc.Markdown(
            children=MARKDOWN.format(sql=metric.get_sql()),
            id=SQL_AREA,
        )
    else:
        return html.Div(id=SQL_AREA)


def store_rendered_saved_metric(
    metric_name: str,
    metric: M.Metric,
    simple_chart: CO.SimpleChart,
    project: M.Project,
    storage: S.MitzuStorage,
    metric_id: Optional[str] = None,
):
    fig = PLT.plot_chart(simple_chart, metric)
    small_image_b64 = PLT.figure_to_base64_image(
        fig, 0.5, kaleid_configs=configs.get_kaleido_configs()
    )
    saved_metric = WM.SavedMetric(
        metric=metric,
        chart=simple_chart,
        project=project,
        image_base64=small_image_b64,
        small_base64=small_image_b64,
        name=metric_name,
        id=metric_id,
    )

    storage.set_saved_metric(metric_id=saved_metric.id, saved_metric=saved_metric)


def create_callbacks():
    @callback(
        output=Output(GRAPH_CONTAINER, "children"),
        inputs=EXP.ALL_INPUT_COMPS,
        state=dict(
            graph_content_type=State(TH.GRAPH_CONTENT_TYPE, "value"),
            href=State(MITZU_LOCATION, "href"),
            metric_name=State(EXP.METRIC_NAME_INPUT, "value"),
            metric_id=State(EXP.METRIC_ID_VALUE, "children"),
        ),
        interval=configs.GRAPH_POLL_INTERVAL_MS,
        background=True,
        running=[
            (
                Output(TH.GRAPH_REFRESH_BUTTON, "disabled"),
                True,
                False,
            ),
            (
                Output(TH.CANCEL_BUTTON, "style"),
                TH.VISIBLE,
                TH.HIDDEN,
            ),
        ],
        cancel=[Input(TH.CANCEL_BUTTON, "n_clicks")],
    )
    @restricted
    def handle_changes_for_graph(
        all_inputs: Dict[str, Any],
        graph_content_type: str,
        href: str,
        metric_name: Optional[str],
        metric_id: str,
    ) -> bc.Component:
        try:
            parse_result = urlparse(href)
            project_id = P.get_path_value(
                P.PROJECTS_EXPLORE_PATH, parse_result.path, P.PROJECT_ID_PATH_PART
            )
            deps = DEPS.Dependencies.get()
            storage = deps.storage
            mitzu_cache = deps.cache
            tracking_service = deps.tracking_service
            onboarding_service = deps.onboarding_service

            project = storage.get_project(project_id)
            if project is None:
                return no_update
            all_inputs = get_final_all_inputs(all_inputs, ctx.inputs_list)
            all_inputs[EXP.METRIC_ID_VALUE] = metric_id
            all_inputs[EXP.METRIC_NAME_INPUT] = metric_name
            all_inputs[EXP.MITZU_LOCATION] = parse_result.query
            dp = project._discovered_project.get_value()
            if dp is None:
                return html.Div(
                    [
                        "It seems your event catalog is empty ",
                        html.Br(),
                        dcc.Link(
                            f"Manage event catalog for {project.project_name}",
                            href=P.create_path(
                                P.EVENTS_CATALOG_PATH_PROJECT_PATH,
                                project_id=project.id,
                            ),
                        ),
                    ],
                    id=GRAPH,
                    className=MESSAGE,
                )

            metric, _, _ = EXP.create_metric_from_all_inputs(all_inputs, dp)

            if metric is None:
                return html.Div("Select an event", id=GRAPH, className=MESSAGE)

            simple_chart: CO.SimpleChart

            hash_key = create_metric_hash_key(metric)
            if ctx.triggered_id in (TH.GRAPH_REFRESH_BUTTON, TH.GRAPH_RUN_QUERY_BUTTON):
                mitzu_cache.clear(hash_key)

            if (
                not project.webapp_settings.auto_refresh_enabled
                and ctx.triggered_id != TH.GRAPH_RUN_QUERY_BUTTON
                and mitzu_cache.get(hash_key) is None
            ):
                return html.Div(
                    "Click run to execute the query", id=GRAPH, className=MESSAGE
                )

            if graph_content_type == TH.CHART_VAL:
                result_df = get_metric_result_df(
                    hash_key, metric, mitzu_cache, tracking_service
                )
                simple_chart = CHRT.get_simple_chart(metric, result_df)
                res = create_graph(metric, simple_chart)  # noqa
            elif graph_content_type == TH.TABLE_VAL:
                res = create_table(metric, hash_key, mitzu_cache, tracking_service)
            elif graph_content_type == TH.SQL_VAL:
                res = create_sql_area(metric)

            onboarding_service.mark_state_complete(
                OF.ConfigureMitzuOnboardingFlow.flow_id(),
                OF.EXPLORE_DATA,
            )

            return res
        except Exception as exc:
            traceback.print_exc()
            return html.Div(
                [
                    html.B("Something has gone wrong. Details:"),
                    html.Pre(children=str(exc)),
                ],
                id=GRAPH,
                className="text-danger small",
            )
