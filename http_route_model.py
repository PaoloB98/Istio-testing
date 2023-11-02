from typing import List, Optional
from pydantic import BaseModel, Field


class Metadata(BaseModel):
    name: str


class BackendRef(BaseModel):
    name: str
    port: int


class ParentRef(BaseModel):
    name: str
    sectionName: str | None = Field(default=None)
    group: str

class Path(BaseModel):
    type: str
    value: str

class Match(BaseModel):
    path: Path


class Rule(BaseModel):
    backendRefs: List[BackendRef]
    matches: List[Match]


class Spec(BaseModel):
    parentRefs: List[ParentRef]
    rules: List[Rule]


class HTTPRoute(BaseModel):
    apiVersion: str
    kind: str
    metadata: Metadata
    spec: Spec