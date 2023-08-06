from __future__ import annotations

from dataclasses import dataclass
import mitzu.webapp.storage as S
from typing import Callable, Dict, Optional
import mitzu.model as M
import mitzu.webapp.model as WM
from mitzu.helper import value_to_label


class EventServiceException(Exception):
    pass


@dataclass
class EventsService:

    storage: S.MitzuStorage

    def populate_discovered_project(self, discovered_project: M.DiscoveredProject):
        self.storage.populate_discovered_project(discovered_project)

    def get_project_definition(
        self, project_id: str
    ) -> Dict[M.EventDataTable, Dict[str, M.Reference[M.EventDef]]]:
        project = self.storage.get_project(project_id)
        dp = project._discovered_project.get_value()
        if dp is None:
            return {}
        self.storage.populate_discovered_project(dp)
        return dp.definitions

    def discover_project(
        self,
        project_id: str,
        callback: Callable[
            [
                M.EventDataTable,
                Dict[str, M.Reference[M.EventDef]],
                Optional[Exception],
                int,
                int,
            ],
            None,
        ],
    ) -> M.DiscoveredProject:
        project = self.storage.get_project(project_id)
        edt_count = len(project.event_data_tables)
        edts = []

        def edt_callback(
            edt: M.EventDataTable,
            defs: Dict[str, M.Reference[M.EventDef]],
            exc: Optional[Exception],
        ):
            if exc is None:
                self.storage.set_event_data_table_definition(
                    event_data_table=edt, definitions=defs
                )
            edts.append(edt)
            callback(edt, defs, exc, len(edts), edt_count)

        discovered_project = project.discover_project(False, edt_callback)
        self.storage.set_project(
            project_id=discovered_project.project.id,
            project=discovered_project.project,
        )

        for edt, defs in discovered_project.definitions.items():
            for event_def_ref in defs.values():
                event_def = event_def_ref.get_value_if_exists()
                event_name = event_def._event_name
                display_name = value_to_label(event_name)

                stored_event_meta = (
                    self.storage.get_event_meta_by_event_name_and_source_table(
                        project_id, event_name, edt.table_name
                    )
                )
                if stored_event_meta is not None:
                    continue

                event_meta_with_same_display_name = (
                    self.storage.get_event_meta_by_display_name(
                        project_id, display_name
                    )
                )
                i = 2
                while event_meta_with_same_display_name is not None:
                    display_name = f"{value_to_label(event_name)} ({i})"
                    event_meta_with_same_display_name = (
                        self.storage.get_event_meta_by_display_name(
                            project_id, display_name
                        )
                    )
                    i += 1

                self.storage.set_event_meta(
                    discovered_project.project.id,
                    WM.EventMeta(
                        source_table=edt.table_name,
                        event_name=event_name,
                        display_name=display_name,
                        description=None,
                    ),
                )

        return discovered_project
