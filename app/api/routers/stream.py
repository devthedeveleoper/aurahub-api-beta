from fastapi import APIRouter, Query, HTTPException, status
from typing import Annotated

from app.core.client import streamtape_client
from app.models.responses import DownloadTicket, DownloadLink, FileInfo

router = APIRouter(
    prefix="/stream",
    tags=["Stream & Download"]
)

@router.get("/ticket/{file_id}", response_model=DownloadTicket)
async def prepare_download(file_id: str):
    """
    Prepares a download and gets a ticket required for the final download link.
    """
    result = await streamtape_client._make_request(
        method="GET",
        endpoint="/file/dlticket",
        params={"file": file_id}
    )
    return result

@router.get("/link", response_model=DownloadLink)
async def get_download_link(
    file_id: str,
    ticket: str,
    captcha_response: str | None = None
):
    """
    Gets the direct download link for a file using a previously generated ticket.
    """
    params = {"file": file_id, "ticket": ticket}
    if captcha_response:
        params["captcha_response"] = captcha_response

    result = await streamtape_client._make_request(
        method="GET",
        endpoint="/file/dl",
        params=params
    )
    return result

@router.get("/info", response_model=dict[str, FileInfo])
async def get_files_info(
    file_ids: Annotated[str, Query(description="A single file ID or multiple IDs separated by a comma.")]
):
    """
    Checks the status and details of one or more files.
    
    (Max. 100 file IDs per request)
    """
    if len(file_ids.split(',')) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only request info for a maximum of 100 files at a time."
        )
    
    result = await streamtape_client._make_request(
        method="GET",
        endpoint="/file/info",
        params={"file": file_ids}
    )
    return result