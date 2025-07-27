from fastapi import APIRouter, Query

from app.core.client import streamtape_client
from app.models.responses import UploadURL

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

@router.get("/url", response_model=UploadURL)
async def get_upload_url(
    folder_id: str | None = Query(default=None, alias="folder", description="Folder-ID to upload to."),
    sha256: str | None = Query(default=None, description="Expected sha256 hash of the file."),
    http_only: bool | None = Query(default=None, alias="httponly", description="If true, use only HTTP upload links.")
):
    """
    Get a dedicated URL to upload a file to.

    Note: This endpoint provides a URL. The actual file upload must be a
    multipart/form-data POST request to that URL.
    """
    params = {}
    if folder_id:
        params["folder"] = folder_id
    if sha256:
        params["sha256"] = sha256
    if http_only is not None:
        params["httponly"] = str(http_only).lower()

    result = await streamtape_client._make_request(
        method="GET",
        endpoint="/file/ul",
        params=params
    )
    return result