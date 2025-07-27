from fastapi import APIRouter, Query, status
from pydantic import AnyHttpUrl

from app.core.client import streamtape_client
from app.models.responses import FolderContent, CreateFolderResponse

router = APIRouter(
    prefix="/fs",  # fs for "filesystem"
    tags=["File & Folder Management"]
)

# --- Folder Management ---

@router.get("/list", response_model=FolderContent)
async def list_folder_contents(
    folder_id: str | None = Query(default=None, alias="folder", description="ID of the folder to list. Defaults to root.")
):
    """Shows the content (files and subfolders) of a given folder."""
    params = {}
    if folder_id:
        params["folder"] = folder_id
    
    result = await streamtape_client._make_request("GET", "/file/listfolder", params)
    return result

@router.post("/folders/create", response_model=CreateFolderResponse)
async def create_folder(
    name: str = Query(description="Name for the new folder."),
    parent_id: str | None = Query(default=None, alias="pid", description="Parent Folder ID. Defaults to root.")
):
    """Creates a new folder."""
    params = {"name": name}
    if parent_id:
        params["pid"] = parent_id

    result = await streamtape_client._make_request("GET", "/file/createfolder", params)
    return result

@router.patch("/folders/rename/{folder_id}", response_model=dict)
async def rename_folder(
    folder_id: str,
    name: str = Query(description="The new name for the folder.")
):
    """Renames a folder."""
    params = {"folder": folder_id, "name": name}
    result = await streamtape_client._make_request("GET", "/file/renamefolder", params)
    return {"success": result}

@router.delete("/folders/delete/{folder_id}", status_code=status.HTTP_200_OK, response_model=dict)
async def delete_folder(folder_id: str):
    """Deletes a folder and all of its contents. Be careful!"""
    result = await streamtape_client._make_request("GET", "/file/deletefolder", {"folder": folder_id})
    return {"success": result}

# --- File Management ---

@router.patch("/files/rename/{file_id}", response_model=dict)
async def rename_file(
    file_id: str,
    name: str = Query(description="The new name for the file.")
):
    """Renames a file."""
    params = {"file": file_id, "name": name}
    result = await streamtape_client._make_request("GET", "/file/rename", params)
    return {"success": result}

@router.patch("/files/move/{file_id}", response_model=dict)
async def move_file(
    file_id: str,
    destination_folder_id: str = Query(alias="folder", description="The ID of the folder to move the file into.")
):
    """Moves a file to a different folder."""
    params = {"file": file_id, "folder": destination_folder_id}
    result = await streamtape_client._make_request("GET", "/file/move", params)
    return {"success": result}

@router.delete("/files/delete/{file_id}", status_code=status.HTTP_200_OK, response_model=dict)
async def delete_file(file_id: str):
    """Deletes a file."""
    result = await streamtape_client._make_request("GET", "/file/delete", {"file": file_id})
    return {"success": result}

# ----- To Get Thumnails -----
@router.get("/files/thumbnail/{file_id}", response_model=dict[str, AnyHttpUrl])
async def get_file_thumbnail(file_id: str):
    """Gets the thumbnail URL for a specific file."""
    thumbnail_url = await streamtape_client._make_request(
        "GET",
        "/file/getsplash",
        {"file": file_id}
    )
    return {"thumbnail_url": thumbnail_url}