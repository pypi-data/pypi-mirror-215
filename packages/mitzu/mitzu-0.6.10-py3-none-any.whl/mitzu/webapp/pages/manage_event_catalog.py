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
)
import dash.development.base_component as bc
import mitzu.webapp.navbar as NB
import mitzu.webapp.pages.paths as P
from typing import List, Optional, Tuple
from mitzu.webapp.auth.decorator import restricted, restricted_layout
import mitzu.webapp.dependencies as DEPS
import mitzu.webapp.helper as H
import dash_mantine_components as dmc
import mitzu.webapp.model as WM
import mitzu.model as M

INDEX_TYPE = "event_catalog"

TABLE_INDEX_TYPE = "event_catalog_table"
PROP_DISPLAY_NAME = "prop_display_name"
PROP_DESCRIPTION = "prop_description"
SAVING_CHANGES_ERROR_CONTAINER = "saving_changes_error_container"

SELECT_PROJECT_DD = "event_catalog_select_project"

MANAGE_PROJECT_BUTTON = "event_catalog_manage_project_button"
EVENT_CATALOG_SPINNER = "event_catalog_spinner"
EVENT_CATALOG_CONTAINER = "event_catalog_container"

TBL_CLS = "small text mh-0 align-top"


def create_event_catalog_table(
    event_catalog: List[WM.EventMeta], discoverd_project: Optional[M.DiscoveredProject]
) -> bc.Component:
    rows = []
    if discoverd_project:
        discovered_events = discoverd_project.get_all_event_names()
    else:
        discovered_events = []

    ordered_event_meta = sorted(
        event_catalog,
        key=lambda x: "__" + x.event_name
        if x.event_name in discovered_events
        else x.event_name,  # sorting down not present evnets
    )

    for event_meta in ordered_event_meta:
        present = event_meta.event_name in discovered_events
        present_cls = " text-secondary" if not present else ""
        cells = [
            html.Td(event_meta.source_table, className=TBL_CLS + present_cls),
            html.Td(event_meta.event_name, className=TBL_CLS + present_cls),
            html.Td(
                dmc.TextInput(
                    id={
                        "type": PROP_DISPLAY_NAME,
                        "index": TABLE_INDEX_TYPE,
                        "source_table": event_meta.source_table,
                        "event_name": event_meta.event_name,
                    },
                    size="xs",
                    value=event_meta.display_name,
                    debounce=300,
                    required=True,
                    className=PROP_DISPLAY_NAME,
                    disabled=not present,
                ),
                className=TBL_CLS,
            ),
            html.Td(
                dmc.Textarea(
                    id={
                        "type": PROP_DESCRIPTION,
                        "index": TABLE_INDEX_TYPE,
                        "source_table": event_meta.source_table,
                        "event_name": event_meta.event_name,
                    },
                    value=event_meta.description,
                    size="xs",
                    className=PROP_DESCRIPTION,
                    debounce=300,
                    maxRows=0,
                    placeholder="Describe the event",
                    disabled=not present,
                ),
                className=TBL_CLS + " w-50",
            ),
        ]

        rows.append(html.Tr(cells))

    return dbc.Table(
        children=[
            html.Thead(
                html.Tr(
                    [
                        html.Th("Source table", className=H.TBL_HEADER_CLS),
                        html.Th("Event name", className=H.TBL_HEADER_CLS),
                        html.Th("Display name", className=H.TBL_HEADER_CLS),
                        html.Th("Description", className=H.TBL_HEADER_CLS),
                        html.Th("", className=H.TBL_HEADER_CLS),
                    ],
                )
            ),
            html.Tbody(rows),
        ],
        hover=False,
        responsive=True,
        striped=True,
        size="sm",
    )


def no_project_layout():
    return layout(None)


@restricted_layout
def layout(project_id: Optional[str], **query_params) -> bc.Component:
    storage = DEPS.Dependencies.get().storage

    projects = storage.list_projects()
    event_catalog: Optional[List[WM.EventMeta]] = None
    discovered_project: Optional[M.DiscoveredProject] = None
    for p in projects:
        if p.id == project_id:
            discovered_project = storage.get_project(
                project_id
            )._discovered_project.get_value_if_exsits()
            event_catalog = storage.get_event_catalog_for_project(project_id)
            break

    options = [{"label": p.name, "value": p.id} for p in projects]

    return html.Div(
        [
            NB.create_mitzu_navbar("event-catalog-navbar"),
            dbc.Container(
                [
                    html.H4("Manage event catalog"),
                    html.Hr(),
                    dbc.Row(
                        [
                            dbc.Col("Select project:", className="lead", width="auto"),
                            dbc.Col(
                                dmc.Select(
                                    id=SELECT_PROJECT_DD,
                                    data=options,
                                    value=project_id,
                                    searchable=True,
                                    placeholder="Select project",
                                ),
                                width="2",
                            ),
                            dbc.Col(
                                dbc.Button(
                                    children=[
                                        html.B(className="bi bi-gear me-1"),
                                        "Manage project",
                                    ],
                                    id=MANAGE_PROJECT_BUTTON,
                                    color="light",
                                    disabled=project_id is None,
                                ),
                                width="auto me-auto",
                            ),
                        ],
                    ),
                    html.Hr(),
                    html.Div(
                        [
                            dbc.Spinner(
                                spinner_class_name="d-none",
                                spinner_style={"width": "1rem", "height": "1rem"},
                                id=EVENT_CATALOG_SPINNER,
                            ),
                            dmc.Alert(
                                children=[],
                                title="Failed to save changes",
                                id=SAVING_CHANGES_ERROR_CONTAINER,
                                hide=True,
                                color="red",
                                className="mb-3",
                            ),
                            html.Div(
                                children=create_event_catalog_table(
                                    event_catalog, discovered_project
                                )
                                if event_catalog is not None
                                else "No project selected",
                                id=EVENT_CATALOG_CONTAINER,
                                className="mb-3 lead",
                            ),
                        ]
                    ),
                ],
            ),
        ],
    )


@callback(
    Output(MANAGE_PROJECT_BUTTON, "disabled"),
    Output(MANAGE_PROJECT_BUTTON, "href"),
    Input(SELECT_PROJECT_DD, "value"),
)
@restricted
def manage_project_disabled(project_id: str) -> Tuple[bool, str]:
    return (
        project_id is None,
        P.create_path(P.PROJECTS_MANAGE_PATH, project_id=project_id)
        if project_id is not None
        else "",
    )


@callback(
    Output(EVENT_CATALOG_CONTAINER, "children"),
    Input(SELECT_PROJECT_DD, "value"),
    prevent_initial_call=True,
)
@restricted
def handle_project_change(
    project_id: str,
):
    storage = DEPS.Dependencies.get().storage
    event_catalog = storage.get_event_catalog_for_project(project_id)
    dp = storage.get_project(project_id)._discovered_project.get_value_if_exsits()
    return create_event_catalog_table(event_catalog, dp)


@callback(
    Output(SAVING_CHANGES_ERROR_CONTAINER, "children"),
    Output(SAVING_CHANGES_ERROR_CONTAINER, "hide"),
    Input(
        {
            "type": ALL,
            "index": TABLE_INDEX_TYPE,
            "source_table": ALL,
            "event_name": ALL,
        },
        "value",
    ),
    State(SELECT_PROJECT_DD, "value"),
    prevent_initial_call=True,
)
@restricted
def handle_event_meta_change(
    table_inputs: List,
    project_id: str,
):
    # empty project selected
    if len(table_inputs) == 0:
        return "", True

    event_name = ctx.triggered_id["event_name"]
    source_table = ctx.triggered_id["source_table"]
    event_meta = WM.EventMeta(
        source_table=source_table,
        event_name=event_name,
        display_name=event_name,
        description=None,
    )

    try:
        for input in ctx.args_grouping[0]:
            if (
                input["id"]["event_name"] != event_name
                or input["id"]["source_table"] != source_table
            ):
                continue

            if input["id"]["type"] == PROP_DISPLAY_NAME:
                display_name = sanitize_string_value(input["value"])
                if display_name is None:
                    raise ValueError(
                        f"Display name of {event_name} in {source_table} cannot be empty"
                    )
                event_meta = WM.EventMeta(
                    source_table=source_table,
                    event_name=event_name,
                    display_name=input["value"],
                    description=event_meta.description,
                )
            elif input["id"]["type"] == PROP_DESCRIPTION:
                event_meta = WM.EventMeta(
                    source_table=source_table,
                    event_name=event_name,
                    display_name=event_meta.display_name,
                    description=sanitize_string_value(input["value"]),
                )

        storage = DEPS.Dependencies.get().storage

        stored_with_display_name = storage.get_event_meta_by_display_name(
            project_id, event_meta.display_name
        )

        if stored_with_display_name is not None and not (
            stored_with_display_name.source_table == event_meta.source_table
            and stored_with_display_name.event_name == event_meta.event_name
        ):
            return (
                f"""
                {event_meta.source_table}.{event_meta.event_name} and
                {stored_with_display_name.source_table}.{stored_with_display_name.event_name}
                can't have the same display name '{event_meta.display_name}'""",
                False,
            )

        storage.set_event_meta(project_id, event_meta)
        return "", True
    except Exception as e:
        return str(e), False


def sanitize_string_value(value: Optional[str]) -> Optional[str]:
    if value:
        sanitized_value = value.strip()
        if sanitized_value != "":
            return sanitized_value
    return None


register_page(
    __name__ + "_event_catalog",
    path=P.EVENTS_CATALOG_PATH,
    title="Mitzu - Event Catalog",
    layout=no_project_layout,
)

register_page(
    __name__,
    path_template=P.EVENTS_CATALOG_PATH_PROJECT_PATH,
    title="Mitzu - Event Catalog",
    layout=layout,
)
