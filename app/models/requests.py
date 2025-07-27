from pydantic import BaseModel, AnyHttpUrl

class AddRemoteUploadRequest(BaseModel):
    """Request body for adding a new remote upload task."""
    url: AnyHttpUrl
    folder_id: str | None = None
    headers: str | None = None
    name: str | None = None