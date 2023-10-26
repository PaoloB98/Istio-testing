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


def build_tcp_rule(tcp_rule_name: str, gateway_name: str, service_to_point: str, port_of_serv: int) -> TCPRoute:
    """
    Build a TCP route
    """
    metadata = Metadata(name=tcp_rule_name)
    backend_ref = BackendRef(name=service_to_point, port=port_of_serv)
    rule = Rule(backendRefs=[backend_ref])
    parent_ref = ParentRef(name=gateway_name, sectionName="iperf-list")
    spec = Spec(parentRefs=[parent_ref], rules=[rule])
    tcp_route = TCPRoute(metadata=metadata, spec=spec, kind="TCPRoute", apiVersion="gateway.networking.k8s.io/v1alpha2")

    return tcp_route