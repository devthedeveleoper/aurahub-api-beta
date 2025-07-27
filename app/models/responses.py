from pydantic import BaseModel, AnyHttpUrl

class DownloadTicket(BaseModel):
    """Response model for a download ticket request."""
    ticket: str
    wait_time: int
    valid_until: str

class DownloadLink(BaseModel):
    """Response model for a direct download link."""
    name: str
    size: int
    url: AnyHttpUrl

class FileInfo(BaseModel):
    """Response model for a single file's information."""
    id: str
    name: str
    size: int
    mime_type: str | None = None
    converted: bool
    status: int

class UploadURL(BaseModel):
    """Response model for getting an upload URL."""
    url: AnyHttpUrl
    valid_until: str

class RemoteUploadAdd(BaseModel):
    """Response model for a newly added remote upload."""
    id: str
    folderid: str

class RemoteUploadStatus(BaseModel):
    """Response model for the status of a single remote upload."""
    id: str
    remoteurl: AnyHttpUrl
    status: str
    bytes_loaded: int | None = None
    bytes_total: int | None = None
    folderid: str
    added: str
    last_update: str
    extid: str | bool | None = None
    linkid: str | None = None
    url: AnyHttpUrl | bool | None = None

class ListedFolder(BaseModel):
    """Response model for a folder within a folder list."""
    id: str
    name: str

class ListedFile(BaseModel):
    """Response model for a file within a folder list."""
    name: str
    size: int
    link: AnyHttpUrl
    created_at: int
    downloads: int
    linkid: str
    status: str | None = None

class FolderContent(BaseModel):
    """Response model for the full content of a folder."""
    folders: list[ListedFolder]
    files: list[ListedFile]

class CreateFolderResponse(BaseModel):
    """Response model for a newly created folder's ID."""
    folderid: str