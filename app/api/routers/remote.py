from fastapi import APIRouter, Query, status

from app.core.client import streamtape_client
from app.models.requests import AddRemoteUploadRequest
from app.models.responses import RemoteUploadAdd, RemoteUploadStatus

router = APIRouter(
    prefix="/remote",
    tags=["Remote Upload"]
)

@router.post("/add", response_model=RemoteUploadAdd, status_code=status.HTTP_202_ACCEPTED)
async def add_remote_upload(request: AddRemoteUploadRequest):
    """
    Queue a file from a remote URL to be uploaded. This is an async job.
    """
    params = {"url": str(request.url)}
    if request.folder_id:
        params["folder"] = request.folder_id
    if request.headers:
        params["headers"] = request.headers
    if request.name:
        params["name"] = request.name

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
    upload_id: str | None = Query(default=None, alias="id", description="A specific upload ID."),
    limit: int | None = Query(default=None, description="Limit the number of results.")
):
    """
    Check the status of one or more remote uploads.
    """
    params = {}
    if upload_id:
        params["id"] = upload_id
    if limit:
        params["limit"] = limit

    result = await streamtape_client._make_request(
        method="GET",
        endpoint="/remotedl/status",
        params=params
    )
    return result