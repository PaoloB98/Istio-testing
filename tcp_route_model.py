from typing import List
from pydantic import BaseModel


class Metadata(BaseModel):
    name: str


class BackendRef(BaseModel):
    name: str
    port: int


class ParentRef(BaseModel):
    name: str
    sectionName: str


class Rule(BaseModel):
    backendRefs: List[BackendRef]


class Spec(BaseModel):
    parentRefs: List[ParentRef]
    rules: List[Rule]


class TCPRoute(BaseModel):
    apiVersion: str
    kind: str
    metadata: Metadata
    spec: Spec