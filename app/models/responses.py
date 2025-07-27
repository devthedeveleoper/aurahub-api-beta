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
    extid: str | bool
    url: AnyHttpUrl | bool
