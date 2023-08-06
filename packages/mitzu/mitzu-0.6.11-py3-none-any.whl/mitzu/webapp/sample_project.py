from __future__ import annotations

import mitzu.model as M
import mitzu.webapp.storage as S
import mitzu.webapp.service.events_service as ES
from mitzu.samples.data_ingestion import create_and_ingest_sample_project


SAMPLE_PROJECT_NAME = "sample_project"
SAMPLE_PROJECT_ID = "sample_project_id"
SAMPLE_CONNECTION_ID = "sample_connection_id"


def setup_sample_project(storage: S.MitzuStorage):
    if storage.project_exists(SAMPLE_PROJECT_ID):
        return
    connection = M.Connection(
        id=SAMPLE_CONNECTION_ID,
        connection_name="Sample connection",
        connection_type=M.ConnectionType.SQLITE,
        host="sample_project",
    )
    project = create_and_ingest_sample_project(
        connection,
        event_count=200000,
        number_of_users=300,
        schema="main",
        overwrite_records=False,
        project_id=SAMPLE_PROJECT_ID,
    )
    storage.set_connection(project.connection.id, project.connection)
    storage.set_project(project_id=project.id, project=project)

    event_service = ES.EventsService(storage)
    event_service.discover_project(project.id, lambda *args: None)
