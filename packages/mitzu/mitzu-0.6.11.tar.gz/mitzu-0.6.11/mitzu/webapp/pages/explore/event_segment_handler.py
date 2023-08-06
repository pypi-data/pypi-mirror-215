from __future__ import annotations

from typing import Any, Dict, List, Optional

import dash.development.base_component as bc
import mitzu.model as M
import mitzu.webapp.pages.explore.simple_segment_handler as SS
from dash import html, dcc
from mitzu.webapp.helper import CHILDREN, get_event_names, WITH_VALUE_CLS
from mitzu.helper import value_to_label
import dash_mantine_components as dmc
import mitzu.webapp.model as WM

EVENT_SEGMENT = "event_segment"
EVENT_NAME_DROPDOWN = "event_name_dropdown"
SIMPLE_SEGMENT_CONTAINER = "simple_segment_container"


def create_event_name_dropdown(
    index,
    discovered_project: M.DiscoveredProject,
    step: int,
    event_segment_index: int,
    segment: Optional[M.Segment],
    event_catalog: List[WM.EventMeta],
) -> dmc.Select:
    options: List[Dict] = []

    segment_event_names = get_event_names(segment)
    if len(set(segment_event_names)) > 1:
        raise Exception("Multiple event complex segment for EventSegmentHandler")
    value = None if len(segment_event_names) == 0 else segment_event_names[0]

    for v in discovered_project.get_all_event_names():
        event_metas = [em for em in event_catalog if em.event_name == v]
        # TODO: fix representation when there are more events with the same event name
        if len(event_metas) != 0:
            event_meta = event_metas[0]
            label = (
                html.Div(
                    children=[
                        html.Div(children=event_meta.display_name),
                        html.Div(
                            children=event_meta.description,
                            className="fst-italic text-secondary text-nowrap",
                        )
                        if event_meta.description
                        else None,
                    ],
                    title=event_meta.description,
                ),
            )
            options.append(
                {
                    "label": label,
                    "search": f"{v} {event_meta.display_name} {event_meta.description if event_meta.description else ''}",
                    "value": v,
                }
            )
        else:
            label = html.Div(value_to_label(v))
            options.append(
                {
                    "label": value_to_label(v),
                    "value": v,
                    "search": f"{v} {value_to_label(v)}",
                }
            )

    options.sort(key=lambda v: v["value"])

    if step == 0 and event_segment_index == 0:
        placeholder = "+ Select Event"
    elif step > 0 and event_segment_index == 0:
        placeholder = "+ Then"
    else:
        placeholder = "+ Select Another Event"

    return html.Div(
        [
            dcc.Dropdown(
                options=options,
                value=value,
                searchable=True,
                clearable=True,
                className=(
                    EVENT_NAME_DROPDOWN
                    + " "
                    + ("" if value is None else WITH_VALUE_CLS)
                    + " border border-0 rounded-2"
                ),
                placeholder=placeholder,
                id={
                    "type": EVENT_NAME_DROPDOWN,
                    "index": index,
                },
            ),
        ]
    )


def get_event_simple_segments(segment: M.Segment) -> List[M.SimpleSegment]:
    if isinstance(segment, M.SimpleSegment):
        return [segment]
    elif isinstance(segment, M.ComplexSegment):
        if segment._operator != M.BinaryOperator.AND:
            raise Exception(
                f"Invalid event level complex segment operator: {segment._operator}"
            )
        return get_event_simple_segments(segment._left) + get_event_simple_segments(
            segment._right
        )
    else:
        raise Exception(f"Unsupported Segment Type: {type(segment)}")


def create_simple_segments_container(
    type_index: str,
    segment: Optional[M.Segment],
    discovered_project: M.DiscoveredProject,
) -> Optional[html.Div]:
    children = []
    if segment is None:
        return None
    event_simple_segments = get_event_simple_segments(segment)
    if isinstance(segment, M.ComplexSegment):
        for seg_index, ess in enumerate(event_simple_segments):
            children.append(
                SS.from_simple_segment(ess, discovered_project, type_index, seg_index)
            )
    elif isinstance(segment, M.SimpleSegment) and isinstance(
        segment._left, M.EventFieldDef
    ):
        children.append(
            SS.from_simple_segment(segment, discovered_project, type_index, 0)
        )

    event_name = event_simple_segments[0]._left._event_name
    event_def = discovered_project.get_event_def(event_name)
    if event_def is None:
        raise Exception(
            f"Invalid state, {event_name} is not possible to find in discovered datasource."
        )
    children.append(
        SS.from_simple_segment(
            M.SimpleSegment(event_def),
            discovered_project,
            type_index,
            len(children),
        )
    )

    return html.Div(
        id={"type": SIMPLE_SEGMENT_CONTAINER, "index": type_index}, children=children
    )


def from_segment(
    segment: Optional[M.Segment],
    discovered_project: M.DiscoveredProject,
    funnel_step: int,
    event_segment_index: int,
    event_catalog: List[WM.EventMeta],
) -> bc.Component:
    type_index = f"{funnel_step}-{event_segment_index}"

    event_dd = create_event_name_dropdown(
        type_index,
        discovered_project,
        funnel_step,
        event_segment_index,
        segment,
        event_catalog,
    )
    children = [event_dd]
    simples_segs_container = create_simple_segments_container(
        type_index, segment, discovered_project
    )
    if simples_segs_container is not None:
        children.append(simples_segs_container)

    component = html.Div(
        id={"type": EVENT_SEGMENT, "index": type_index},
        children=children,
        className=EVENT_SEGMENT,
    )
    return component


def from_all_inputs(
    discovered_project: Optional[M.DiscoveredProject],
    event_segment: Dict[str, Any],
    complex_segment_index: int,
    event_segment_index: int,
) -> Optional[M.Segment]:
    if discovered_project is None:
        return None
    event_name_dd_value = event_segment.get(EVENT_NAME_DROPDOWN)
    simple_segments = event_segment.get(CHILDREN, {})

    if event_name_dd_value is None:
        return None

    res_segment: Optional[M.Segment] = None
    ss_index = 0
    for _, simple_segment in simple_segments.items():
        simple_seg = SS.from_all_inputs(
            discovered_project,
            simple_segment,
            complex_segment_index,
            event_segment_index,
            ss_index,
        )
        ss_index += 1

        if simple_seg is None:
            continue
        if simple_seg._left._event_name != event_name_dd_value:
            continue

        if res_segment is None:
            res_segment = simple_seg
        else:
            res_segment = res_segment & simple_seg

    if res_segment is None and event_name_dd_value is not None:
        return M.SimpleSegment(
            _left=discovered_project.get_event_def(event_name_dd_value)
        )
    return res_segment
