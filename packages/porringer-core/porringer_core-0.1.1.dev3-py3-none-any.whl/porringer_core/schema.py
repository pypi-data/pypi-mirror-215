"""Schema for Porringer"""

from pydantic import BaseModel


class Package(BaseModel):
    """Package definition"""

    name: str
    version: str
