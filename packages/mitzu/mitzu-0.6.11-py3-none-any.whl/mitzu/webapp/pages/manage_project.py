import traceback
from typing import Any, Dict, List, Optional, cast

import dash.development.base_component as bc
import dash_bootstrap_components as dbc
from dash import (
    ALL,
    Input,
    Output,
    State,
    callback,
    ctx,
    html,
    register_page,
    no_update,
    dcc,
)
from mitzu.webapp.helper import MITZU_LOCATION

import mitzu.helper as H
import mitzu.model as M
import mitzu.webapp.dependencies as DEPS
import mitzu.webapp.helper as WH
import mitzu.webapp.navbar as NB
import mitzu.webapp.pages.paths as P
import mitzu.webapp.pages.projects.helper as MPH
import mitzu.webapp.pages.projects.manage_project_component as MPC
import mitzu.webapp.onboarding_flow as OF

from mitzu.webapp.auth.decorator import restricted, restricted_layout
from datetime import datetime

CREATE_PROJECT_DOCS_LINK = "https://github.com/mitzu-io/mitzu/blob/main/DOCS.md"
PROJECT_TITLE = "project_title"
PROJECT_LOCATION = "project_location"
SAVE_BUTTON = "project_save_button"
SAVE_AND_DISCOVER_BUTTON = "project_save_and_discover"
MANAGE_PROJECT_INFO = "manage_project_info"

DELETE_BUTTON = "project_delete_button"

CONFIRM_DIALOG_INDEX = "project_delete_confirm"
CONFIRM_DIALOG_CLOSE = "project_delete_confirm_dialog_close"
CONFIRM_DIALOG_ACCEPT = "project_delete_confirm_dialog_accept"


def create_delete_button(project: Optional[M.Project]) -> bc.Component:
    if project is not None:
        return dbc.Button(
            [html.B(className="bi bi-x-circle me-1"), "Delete Project"],
            id=DELETE_BUTTON,
            color="danger",
            class_name="d-inline-block me-3 mb-1",
            size="sm",
        )
    else:
        return html.Div()


def create_confirm_dialog(project: Optional[M.Project]):
    if project is None:
        return html.Div()
    return dbc.Modal(
        [
            dbc.ModalBody(
                f"Do you really want to delete the {project.project_name}?",
                class_name="lead",
            ),
            dbc.ModalFooter(
                [
                    dbc.Button(
                        "Close",
                        id=CONFIRM_DIALOG_CLOSE,
                        size="sm",
                        color="secondary",
                        class_name="me-1",
                    ),
                    dbc.Button(
                        "Delete",
                        id=CONFIRM_DIALOG_ACCEPT,
                        size="sm",
                        color="danger",
                        href=P.PROJECTS_PATH,
                        external_link=True,
                    ),
                ]
            ),
        ],
        id=CONFIRM_DIALOG_INDEX,
        is_open=False,
    )


def create_event_data_table(project: M.Project, tr: html.Tr):
    full_table_name = MPH.get_value_from_row(tr, 1)
    user_id_column = MPH.get_value_from_row(tr, 2)
    event_time_column = MPH.get_value_from_row(tr, 3)
    event_name_column = MPH.get_value_from_row(tr, 4)
    date_partition_col = MPH.get_value_from_row(tr, 5)
    ignore_cols = MPH.get_value_from_row(tr, 6)

    schema, table_name = tuple(full_table_name.split("."))
    adapter = project.get_adapter()

    fields = adapter.list_all_table_columns(schema, table_name)
    all_fields: Dict[str, M.Field] = {}
    for field in fields:
        if field._sub_fields:
            for sf in field.get_all_subfields():
                all_fields[sf._get_name()] = sf
        else:
            all_fields[field._get_name()] = field

    converted_ignored_fields: List[M.Field] = []
    if ignore_cols:
        for igf in ignore_cols.split(","):
            converted_ignored_fields.append(all_fields[igf])

    return M.EventDataTable.create(
        table_name=table_name,
        schema=schema,
        event_time_field=all_fields[event_time_column],
        event_name_field=all_fields[event_name_column] if event_name_column else None,
        ignored_fields=converted_ignored_fields,
        user_id_field=all_fields[user_id_column],
        event_specific_fields=fields,
        date_partition_field=(
            all_fields[date_partition_col] if date_partition_col else None
        ),
    )


@restricted_layout
def layout_create(**query_params) -> bc.Component:
    return layout(None, **query_params)


@restricted_layout
def layout(project_id: Optional[str] = None, **query_params) -> bc.Component:
    project: Optional[M.Project] = None
    dependencies = DEPS.Dependencies.get()
    if project_id is not None:
        project = dependencies.storage.get_project(project_id)

    title = (
        "Create new project"
        if project is None
        else f"{H.value_to_label(project.project_name)}"
    )

    return html.Div(
        [
            NB.create_mitzu_navbar("create-project-navbar"),
            dbc.Container(
                children=[
                    dcc.Location(id=PROJECT_LOCATION),
                    html.Div(title, id=PROJECT_TITLE, className="lead"),
                    MPC.create_project_settings(project, dependencies, **query_params),
                    dbc.Button(
                        [html.B(className="bi bi-check-circle"), " Save"],
                        color="success",
                        id=SAVE_BUTTON,
                        class_name="d-inline-block me-3 mb-1",
                        size="sm",
                    ),
                    dbc.Button(
                        [
                            html.B(className="bi bi-search me-1"),
                            "Save and manage events",
                        ],
                        size="sm",
                        color="primary",
                        id=SAVE_AND_DISCOVER_BUTTON,
                        class_name="d-inline-block me-3 mb-1",
                    ),
                    html.Div(
                        children="",
                        className="mb-3 lead",
                        id=MANAGE_PROJECT_INFO,
                    ),
                    create_delete_button(project),
                    create_confirm_dialog(project),
                ],
                class_name="mb-3",
            ),
        ]
    )


@callback(
    Output(CONFIRM_DIALOG_INDEX, "is_open"),
    Input(DELETE_BUTTON, "n_clicks"),
    Input(CONFIRM_DIALOG_CLOSE, "n_clicks"),
    prevent_initial_call=True,
)
@restricted
def delete_button_clicked(delete: int, close: int) -> bool:
    if delete is None:
        return no_update
    return ctx.triggered_id == DELETE_BUTTON


@callback(
    Output(CONFIRM_DIALOG_ACCEPT, "n_clicks"),
    Input(CONFIRM_DIALOG_ACCEPT, "n_clicks"),
    State(MITZU_LOCATION, "pathname"),
    prevent_initial_call=True,
)
@restricted
def delete_confirm_button_clicked(n_clicks: int, pathname: str) -> int:
    if n_clicks:
        project_id = P.get_path_value(
            P.PROJECTS_MANAGE_PATH, pathname, P.PROJECT_ID_PATH_PART
        )
        depenednecies = DEPS.Dependencies.get()
        try:
            depenednecies.storage.delete_project(project_id)
        except Exception:
            # TBD: Toaster
            traceback.print_exc()

    return no_update


@callback(
    Output(MANAGE_PROJECT_INFO, "children"),
    Output(PROJECT_LOCATION, "href"),
    Input(SAVE_BUTTON, "n_clicks"),
    Input(SAVE_AND_DISCOVER_BUTTON, "n_clicks"),
    State(MPH.EDT_TBL_BODY, "children"),
    State({"type": MPH.PROJECT_INDEX_TYPE, "index": ALL}, "value"),
    State(WH.MITZU_LOCATION, "pathname"),
    background=True,
    running=[
        (
            Output(MANAGE_PROJECT_INFO, "children"),
            [
                dbc.Spinner(
                    spinner_style={"width": "1rem", "height": "1rem"},
                    spinner_class_name="me-1",
                ),
                "Saving and validating project",
            ],
            "Project succesfully saved",
        )
    ],
    prevent_initial_call=True,
)
@restricted
def save_button_clicked(
    save_clicks: int,
    save_and_discover_clicks: int,
    edt_table_rows: List,
    prop_values: List,
    pathname: str,
):
    try:

        deps = DEPS.Dependencies.get()
        storage = deps.storage
        tracking_service = deps.tracking_service
        onboarding_service = deps.onboarding_service

        project_props: Dict[str, Any] = {}

        for prop in ctx.args_grouping[3]:
            id_val = prop["id"]
            if id_val.get("type") == MPH.PROJECT_INDEX_TYPE:
                project_props[id_val.get("index")] = prop["value"]

        project_id = cast(str, project_props.get(MPC.PROP_PROJECT_ID))
        project_name = cast(str, project_props.get(MPC.PROP_PROJECT_NAME))
        if not project_name:
            return (
                html.P("Please name your project!", className="text-danger"),
                no_update,
            )

        connection_id = cast(str, project_props.get(MPC.PROP_CONNECTION))
        if connection_id is None:
            return (
                html.P("Please select or add connection!", className="text-danger"),
                no_update,
            )

        description = cast(str, project_props.get(MPC.PROP_DESCRIPTION))
        disc_lookback_days = cast(int, project_props.get(MPC.PROP_DISC_LOOKBACK_DAYS))
        min_sample_size = cast(int, project_props.get(MPC.PROP_DISC_SAMPLE_SIZE))
        autorefresh_enabled = cast(
            bool, project_props.get(MPC.PROP_EXPLORE_AUTO_REFRESH)
        )
        end_date_config = M.WebappEndDateConfig[
            project_props.get(
                MPC.PROP_END_DATE_CONFIG, M.WebappEndDateConfig.NOW.name
            ).upper()
        ]
        custom_end_date_str = project_props.get(MPC.PROP_CUSTOM_END_DATE_CONFIG)
        if custom_end_date_str is not None:
            custom_end_date = datetime.strptime(custom_end_date_str[:10], "%Y-%m-%d")
        else:
            custom_end_date = None

        connection = storage.get_connection(connection_id)
        dummy_project = M.Project(
            connection=connection,
            event_data_tables=[],
            project_name="dummy_project",
        )

        event_data_tables = []
        for tr in edt_table_rows:
            event_data_tables.append(create_event_data_table(dummy_project, tr))

        project = M.Project(
            project_name=project_name,
            project_id=project_id,
            connection=connection,
            description=description,
            webapp_settings=M.WebappSettings(
                auto_refresh_enabled=autorefresh_enabled,
                end_date_config=end_date_config,
                custom_end_date=custom_end_date,
            ),
            discovery_settings=M.DiscoverySettings(
                min_property_sample_size=min_sample_size,
                lookback_days=disc_lookback_days,
            ),
            event_data_tables=event_data_tables,
        )

        storage.set_project(project_id, project)
        tracking_service.track_project_saved(project)
        onboarding_service.mark_state_complete(
            OF.ConfigureMitzuOnboardingFlow.flow_id(),
            OF.CONNECT_WAREHOUSE,
        )
        if ctx.triggered_id == SAVE_BUTTON:
            return ("Project succesfully saved", no_update)
        else:
            return (
                no_update,
                P.create_path(
                    P.EVENTS_CATALOG_PATH_PROJECT_PATH,
                    project_id=project_id,
                ),
            )
    except Exception as exc:

        traceback.print_exc()
        return (f"Something went wrong: {str(exc)}", no_update)


register_page(
    __name__ + "_create",
    path=P.PROJECTS_CREATE_PATH,
    title="Mitzu - Create Project",
    layout=layout_create,
)


register_page(
    __name__,
    path_template=P.PROJECTS_MANAGE_PATH,
    title="Mitzu - Manage Project",
    layout=layout,
)
