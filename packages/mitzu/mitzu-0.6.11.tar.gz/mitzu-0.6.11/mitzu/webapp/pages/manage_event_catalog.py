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
from typing import Dict, List, Optional, Tuple
from mitzu.webapp.auth.decorator import restricted, restricted_layout
import mitzu.webapp.dependencies as DEPS
import mitzu.webapp.helper as H
import dash_mantine_components as dmc
import mitzu.webapp.model as WM
import mitzu.model as M
import traceback
from mitzu.helper import LOGGER

INDEX_TYPE = "event_catalog"

TABLE_INDEX_TYPE = "event_catalog_table"
PROP_DISPLAY_NAME = "prop_display_name"
PROP_DESCRIPTION = "prop_description"
SAVING_CHANGES_ERROR_CONTAINER = "saving_changes_error_container"

SELECT_PROJECT_DD = "event_catalog_select_project"

MANAGE_PROJECT_BUTTON = "event_catalog_manage_project_button"
EVENT_CATALOG_CONTAINER = "event_catalog_container"
EVENT_CATALOG_CONTAINER_2 = "event_catalog_container_2"

TBL_CLS = "small text mh-0 align-top"

NO_EVENTS_ALERT = "no_events_alert"
DISCOVER_EDT_BUTTON_TYPE = "edt_discover_button"
DISCOVER_PROJECT_BUTTON = "events_discover_button"
DISCOVER_CANCEL_BUTTON = "cancel_discovery_button"
DISCOVER_PROGRESS = "discover_progress"
DISCOVER_PROGRESS_CONTAINER = "discover_progress_container"
DISCOVER_ERROR_CONTAINER = "discover_error_container"


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

    return [
        dmc.Alert(
            id=NO_EVENTS_ALERT,
            children=[
                "It seems that you don't have any events in your catalog. ",
                "Try fetching events for your project.",
            ],
            title="No events in your catalog",
            color="gray",
            hide=len(rows) != 0,
        ),
        dbc.Table(
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
            size="sm",
        ),
    ]


def no_project_layout():
    return layout(None)


@restricted_layout
def layout(project_id: Optional[str], **query_params) -> bc.Component:
    storage = DEPS.Dependencies.get().storage

    projects = storage.list_projects()
    event_catalog: Optional[List[WM.EventMeta]] = None
    discovered_project: Optional[M.DiscoveredProject] = None

    if project_id is None:
        project_id = projects[0].id if len(projects) > 0 else None

    for p in projects:
        if p.id == project_id:
            discovered_project = storage.get_project(
                project_id
            )._discovered_project.get_value()
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
                                    href=P.create_path(
                                        P.PROJECTS_MANAGE_PATH, project_id=project_id
                                    ),
                                ),
                                width="auto me-auto",
                            ),
                            dbc.Col(
                                dbc.Button(
                                    [
                                        html.B(className="bi bi-x-circle me-1"),
                                        "Cancel",
                                    ],
                                    id=DISCOVER_CANCEL_BUTTON,
                                    color="light",
                                    class_name="d-inline-block mb-3",
                                    size="sm",
                                ),
                                width="auto",
                                class_name="invisible",
                            ),
                            dbc.Col(
                                dbc.Button(
                                    [
                                        html.B(className="bi bi-arrow-clockwise"),
                                        "Fetch events",
                                    ],
                                    id=DISCOVER_PROJECT_BUTTON,
                                    disabled=project_id is None,
                                    class_name="d-inline-block mb-3 me-3",
                                    size="sm",
                                    color="secondary",
                                ),
                                width="auto",
                            ),
                        ],
                    ),
                    html.Hr(),
                    html.Div(
                        id=DISCOVER_PROGRESS_CONTAINER,
                        children=[
                            html.Div(
                                children=[
                                    "Refreshing all events",
                                    dbc.Progress(
                                        id=DISCOVER_PROGRESS,
                                        animated=True,
                                        label="0%",
                                        value=2,
                                        min=0,
                                        max=100,
                                        style={
                                            "height": "14px",
                                            "border-radius": "8px",
                                        },
                                        className="mb-3 mt-3",
                                    ),
                                ],
                                className="lead shadow p-3 rounded mb-3",
                            ),
                        ],
                        className="d-none",
                    ),
                    html.Div(
                        [
                            dmc.Alert(
                                children=[],
                                title="Failed to save changes",
                                id=SAVING_CHANGES_ERROR_CONTAINER,
                                hide=True,
                                color="red",
                                className="mb-3",
                            ),
                            dmc.Alert(
                                children=[],
                                title="Events refresh failed",
                                id=DISCOVER_ERROR_CONTAINER,
                                color="red",
                                hide=True,
                                className="mb-3",
                            ),
                            html.Div(
                                html.Div(
                                    children=create_event_catalog_table(
                                        event_catalog, discovered_project
                                    )
                                    if event_catalog is not None
                                    else "Select project",
                                    id=EVENT_CATALOG_CONTAINER,
                                    className="mb-3 lead",
                                ),
                                id=EVENT_CATALOG_CONTAINER_2,
                            ),
                        ]
                    ),
                ],
            ),
        ],
    )


def create_discovery_error_message(errors: Dict[str, str]):
    if errors is None or len(errors) == 0:
        return []
    msgs = []
    for tbl, error in errors.items():
        msgs.append(
            [
                html.B(f"Failed to refresh: {tbl}", className="d-block"),
                html.Div(f"Message: {error[:400]}..."),
            ]
        )

    return [html.Div(children=msg) for msg in msgs]


@callback(
    Output(MANAGE_PROJECT_BUTTON, "disabled"),
    Output(MANAGE_PROJECT_BUTTON, "href"),
    Input(SELECT_PROJECT_DD, "value"),
    prevent_initial_call=True,
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
    Output(DISCOVER_PROJECT_BUTTON, "disabled"),
    Input(SELECT_PROJECT_DD, "value"),
    prevent_initial_call=True,
)
@restricted
def handle_project_change(
    project_id: str,
):
    storage = DEPS.Dependencies.get().storage
    event_catalog = storage.get_event_catalog_for_project(project_id)
    dp = storage.get_project(project_id)._discovered_project.get_value()
    return create_event_catalog_table(event_catalog, dp), False


@callback(
    Output(EVENT_CATALOG_CONTAINER_2, "children"),
    Output(DISCOVER_ERROR_CONTAINER, "children"),
    Output(DISCOVER_ERROR_CONTAINER, "hide"),
    Input(DISCOVER_PROJECT_BUTTON, "n_clicks"),
    State(SELECT_PROJECT_DD, "value"),
    background=True,
    running=[
        (Output(DISCOVER_PROJECT_BUTTON, "disabled"), True, False),
        (Output(SELECT_PROJECT_DD, "disabled"), True, False),
        (Output(DISCOVER_CANCEL_BUTTON, "class_name"), "visible", "invisible"),
        (Output(DISCOVER_PROGRESS_CONTAINER, "className"), "d-block", "d-none"),
        (Output(DISCOVER_PROGRESS, "value"), 1, 1),
        (Output(NO_EVENTS_ALERT, "className"), "d-none", "d-none"),
    ],
    progress=[
        Output(DISCOVER_PROGRESS, "value"),
        Output(DISCOVER_PROGRESS, "label"),
        Output(DISCOVER_PROGRESS, "color"),
    ],
    prevent_initial_call=True,
    cancel=Input(DISCOVER_CANCEL_BUTTON, "n_clicks"),
)
@restricted
def handle_project_discovery(set_progress, discovery_clicks: int, project_id: str):
    try:
        deps = DEPS.Dependencies.get()
        events_service = deps.events_service
        tracking_service = deps.tracking_service
        set_progress((2, "0%", "primary"))

        errors: Dict[str, str] = {}

        def edt_callback(
            edt: M.EventDataTable,
            defs: Dict[str, M.Reference[M.EventDef]],
            exc: Optional[Exception],
            processed_count: int,
            total_count: int,
        ):
            if exc is not None:
                errors[edt.get_full_name()] = str(exc)

            set_progress(
                (
                    processed_count * 100 / total_count,
                    f"{(processed_count * 100 / total_count):.0f}%",
                    "primary" if len(errors) == 0 else "danger",
                )
            )
            LOGGER.debug(f"Discovering tables {processed_count*100/total_count:.0f}%")

        dp = events_service.discover_project(project_id, callback=edt_callback)
        tracking_service.track_project_discovered(dp)
        event_catalog = deps.storage.get_event_catalog_for_project(project_id)
        catalog = create_event_catalog_table(event_catalog, dp)

        return (
            html.Div(html.Div(catalog, id=EVENT_CATALOG_CONTAINER)),
            create_discovery_error_message(errors),
            len(errors) == 0,
        )
    except Exception as exc:
        traceback.print_exc()
        return ([], f"Something went wrong: {str(exc)[:300]}", True)


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
