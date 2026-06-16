from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

import psycopg
from psycopg.rows import dict_row
from loguru import logger


DATABASE_URL = os.environ.get("DATABASE_URL", "")

_service_name = "narrato"


def _get_conn():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable is not set")
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


# ==================== Narration Projects ====================


def create_narration_project(
    name: str,
    workspace_id: str = "default",
    video_path: str | None = None,
    script: dict | None = None,
    status: str = "draft",
    settings: dict | None = None,
    output_path: str | None = None,
    language: str = "zh",
) -> dict:
    project_id = uuid4()
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO narration_projects (id, workspace_id, name, video_path, script, status, settings, output_path, language)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *
                """,
                (
                    str(project_id),
                    workspace_id,
                    name,
                    video_path,
                    json.dumps(script or {}),
                    status,
                    json.dumps(settings or {}),
                    output_path,
                    language,
                ),
            )
            return dict(cur.fetchone())


def get_narration_project(project_id: str) -> dict | None:
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM narration_projects WHERE id = %s", (project_id,))
            row = cur.fetchone()
            return dict(row) if row else None


def list_narration_projects(
    workspace_id: str = "default",
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[dict]:
    with _get_conn() as conn:
        with conn.cursor() as cur:
            if status:
                cur.execute(
                    "SELECT * FROM narration_projects WHERE workspace_id = %s AND status = %s ORDER BY created_at DESC LIMIT %s OFFSET %s",
                    (workspace_id, status, limit, offset),
                )
            else:
                cur.execute(
                    "SELECT * FROM narration_projects WHERE workspace_id = %s ORDER BY created_at DESC LIMIT %s OFFSET %s",
                    (workspace_id, limit, offset),
                )
            return [dict(r) for r in cur.fetchall()]


def update_narration_project(project_id: str, **fields) -> dict | None:
    allowed = {"name", "video_path", "script", "status", "settings", "output_path", "language"}
    updates = {k: v for k, v in fields.items() if k in allowed}
    if not updates:
        return get_narration_project(project_id)

    set_parts = []
    values = []
    for k, v in updates.items():
        set_parts.append(f"{k} = %s")
        values.append(json.dumps(v) if isinstance(v, (dict, list)) else v)
    values.append(project_id)

    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"UPDATE narration_projects SET {', '.join(set_parts)} WHERE id = %s RETURNING *",
                values,
            )
            row = cur.fetchone()
            return dict(row) if row else None


def delete_narration_project(project_id: str) -> bool:
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM narration_projects WHERE id = %s", (project_id,))
            return cur.rowcount > 0


# ==================== Narration Tasks ====================


def create_narration_task(
    project_id: str,
    task_type: str,
    status: str = "pending",
    input_data: dict | None = None,
) -> dict:
    task_id = uuid4()
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO narration_tasks (id, project_id, task_type, status, input)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *
                """,
                (str(task_id), project_id, task_type, status, json.dumps(input_data or {})),
            )
            return dict(cur.fetchone())


def get_narration_task(task_id: str) -> dict | None:
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM narration_tasks WHERE id = %s", (task_id,))
            row = cur.fetchone()
            return dict(row) if row else None


def list_narration_tasks(
    project_id: str,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[dict]:
    with _get_conn() as conn:
        with conn.cursor() as cur:
            if status:
                cur.execute(
                    "SELECT * FROM narration_tasks WHERE project_id = %s AND status = %s ORDER BY created_at DESC LIMIT %s OFFSET %s",
                    (project_id, status, limit, offset),
                )
            else:
                cur.execute(
                    "SELECT * FROM narration_tasks WHERE project_id = %s ORDER BY created_at DESC LIMIT %s OFFSET %s",
                    (project_id, limit, offset),
                )
            return [dict(r) for r in cur.fetchall()]


def update_narration_task(
    task_id: str,
    status: str | None = None,
    output_data: dict | None = None,
    error: str | None = None,
) -> dict | None:
    sets = []
    vals: list[Any] = []

    if status is not None:
        sets.append("status = %s")
        vals.append(status)
        if status == "running":
            sets.append("started_at = CURRENT_TIMESTAMP")
        elif status in ("completed", "failed"):
            sets.append("completed_at = CURRENT_TIMESTAMP")

    if output_data is not None:
        sets.append("output = %s")
        vals.append(json.dumps(output_data))

    if error is not None:
        sets.append("error = %s")
        vals.append(error)

    if not sets:
        return get_narration_task(task_id)

    vals.append(task_id)
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"UPDATE narration_tasks SET {', '.join(sets)} WHERE id = %s RETURNING *",
                vals,
            )
            row = cur.fetchone()
            return dict(row) if row else None


def delete_narration_tasks(project_id: str) -> int:
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM narration_tasks WHERE project_id = %s", (project_id,))
            return cur.rowcount


# ==================== File Registration ====================


def register_file(
    file_name: str,
    file_path: str,
    file_type: str,
    workspace_id: str = "default",
    file_size: int | None = None,
    mime_type: str | None = None,
    metadata: dict | None = None,
) -> dict:
    file_id = uuid4()
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO files (id, workspace_id, service, file_type, file_name, file_path, file_size, mime_type, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *
                """,
                (
                    str(file_id),
                    workspace_id,
                    _service_name,
                    file_type,
                    file_name,
                    file_path,
                    file_size,
                    mime_type,
                    json.dumps(metadata or {}),
                ),
            )
            return dict(cur.fetchone())


def get_file(file_id: str) -> dict | None:
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM files WHERE id = %s", (file_id,))
            row = cur.fetchone()
            return dict(row) if row else None


def list_files(
    workspace_id: str = "default",
    file_type: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    with _get_conn() as conn:
        with conn.cursor() as cur:
            if file_type:
                cur.execute(
                    "SELECT * FROM files WHERE workspace_id = %s AND service = %s AND file_type = %s ORDER BY created_at DESC LIMIT %s OFFSET %s",
                    (workspace_id, _service_name, file_type, limit, offset),
                )
            else:
                cur.execute(
                    "SELECT * FROM files WHERE workspace_id = %s AND service = %s ORDER BY created_at DESC LIMIT %s OFFSET %s",
                    (workspace_id, _service_name, limit, offset),
                )
            return [dict(r) for r in cur.fetchall()]


def delete_file(file_id: str) -> bool:
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM files WHERE id = %s", (file_id,))
            return cur.rowcount > 0


# ==================== Activity Logging ====================


def log_activity(
    action: str,
    workspace_id: str | None = None,
    user_id: str | None = None,
    resource_type: str | None = None,
    resource_id: str | None = None,
    details: dict | None = None,
    ip_address: str | None = None,
) -> dict:
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO activity_logs (workspace_id, user_id, service, action, resource_type, resource_id, details, ip_address)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s::inet)
                RETURNING *
                """,
                (
                    workspace_id,
                    user_id,
                    _service_name,
                    action,
                    resource_type,
                    resource_id,
                    json.dumps(details or {}),
                    ip_address,
                ),
            )
            return dict(cur.fetchone())


def list_activity_logs(
    workspace_id: str | None = None,
    resource_type: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    with _get_conn() as conn:
        with conn.cursor() as cur:
            clauses = ["service = %s"]
            params: list[Any] = [_service_name]

            if workspace_id:
                clauses.append("workspace_id = %s")
                params.append(workspace_id)
            if resource_type:
                clauses.append("resource_type = %s")
                params.append(resource_type)

            params.extend([limit, offset])
            cur.execute(
                f"SELECT * FROM activity_logs WHERE {' AND '.join(clauses)} ORDER BY created_at DESC LIMIT %s OFFSET %s",
                params,
            )
            return [dict(r) for r in cur.fetchall()]
