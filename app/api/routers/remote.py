from fastapi import APIRouter, Query, status
from pydantic import AnyHttpUrl

from app.core.client import streamtape_client
from app.models.responses import RemoteUploadAdd, RemoteUploadStatus

router = APIRouter(
    prefix="/remote",
    tags=["Remote Upload"]
)

@router.get("/add", response_model=RemoteUploadAdd, status_code=status.HTTP_202_ACCEPTED)
async def add_remote_upload(
    url: AnyHttpUrl = Query(description="Remote URL of the file to upload."),
    folder_id: str | None = Query(default=None, alias="folder", description="Folder-ID to upload to."),
    headers: str | None = Query(default=None, description="Additional HTTP headers, separated by newline."),
    name: str | None = Query(default=None, description="Custom name for the new file.")
):
    """
    Queue a file from a remote URL to be uploaded. This is an async job.
    """
    params = {"url": str(url)}
    if folder_id:
        params["folder"] = folder_id
    if headers:
        params["headers"] = headers
    if name:
        params["name"] = name

    result = await streamtape_client._make_request(
        method="GET",
        endpoint="/remotedl/add",
        params=params
    )
    return result

@router.delete("/remove/{upload_id}", response_model=dict)
async def remove_remote_upload(upload_id: str):
    """
    Remove/cancel a remote upload. Use 'all' to remove all uploads.
    """
    result = await streamtape_client._make_request(
        method="GET",
        endpoint="/remotedl/remove",
        params={"id": upload_id}
    )
    return {"success": result}

@router.get("/status", response_model=dict[str, RemoteUploadStatus])
async def get_remote_upload_status(
    upload_id: str = Query(alias="id", description="A specific remote upload ID to check."),
    limit: int | None = Query(default=None, description="Limit the number of results (optional).")
):
    """
    Check the status of a specific remote upload.
    """
    params = {"id": upload_id}
    if limit is not None:
        params["limit"] = str(limit)

    result = await streamtape_client._make_request(
        method="GET",
        endpoint="/remotedl/status",
        params=params
    )
    return result