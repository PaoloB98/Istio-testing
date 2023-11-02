import kubernetes.client
from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.rest import ApiException
from pprint import pprint

from http_route_model import HTTPRoute
from tcp_route_model import TCPRoute, build_tcp_rule

def get_k8s_config_from_file(filepath: str) -> kubernetes.client.Configuration:
    """
    Create a kube client config from the configuration file.
    @param filepath: the path of the configuration file

    @return kube client configuration
    """
    kube_client_config = type.__call__(Configuration)
    # Carico la conf da file
    config.load_kube_config(config_file=filepath, context=None, client_configuration=kube_client_config,
                            persist_config=False)
    kube_client_config.verify_ssl = False

    return kube_client_config

def update_tcp_route():
    file = "cluster.config"
    configuration = get_k8s_config_from_file(filepath=file)

    # Enter a context with an instance of the API kubernetes.client
    with kubernetes.client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = kubernetes.client.CustomObjectsApi(api_client)
        group = 'gateway.networking.k8s.io'  # str | The custom resource's group name
        version = 'v1alpha2'  # str | The custom resource's version
        plural = 'tcproutes'  # str | The custom resource's plural name. For TPRs this would be lowercase plural kind.

    try:
        # Otteniamo l'oggetto che vogliamo aggiornare (c'è già sul server)
        existing_rule = api_instance.get_namespaced_custom_object(group, version, 'default',
                                                                  plural, "iperfroute")
        # Lo rendo un modello per semplificarmi la vita
        tcp_rule = TCPRoute.model_validate(existing_rule)

        # Inverting the zone, (changing the service to address)
        if tcp_rule.spec.rules[0].backendRefs[0].name == "iperf-service-a":
            tcp_rule.spec.rules[0].backendRefs[0].name = "iperf-service-b"
        else:
            tcp_rule.spec.rules[0].backendRefs[0].name = "iperf-service-a"

        # Da modello lo passo in dizionario
        body: dict = tcp_rule.model_dump()

        #Aggiorna l'oggetto chiamando l'API di K8S
        api_response = api_instance.patch_namespaced_custom_object(group, version, 'default', plural,
                                                                   tcp_rule.metadata.name, body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CustomObjectsApi->create_cluster_custom_object: %s\n" % e)

def update_http_route():
    file = "cluster.config"
    configuration = get_k8s_config_from_file(filepath=file)

    # Enter a context with an instance of the API kubernetes.client
    with kubernetes.client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = kubernetes.client.CustomObjectsApi(api_client)
        group = 'gateway.networking.k8s.io'  # str | The custom resource's group name
        version = 'v1beta1'  # str | The custom resource's version
        plural = 'httproutes'  # str | The custom resource's plural name. For TPRs this would be lowercase plural kind.

    try:
        # Otteniamo l'oggetto che vogliamo aggiornare (c'è già sul server)
        existing_rule = api_instance.get_namespaced_custom_object(group, version, 'default',
                                                                  plural, "bookinfo")
        # Lo rendo un modello per semplificarmi la vita
        http_route = HTTPRoute.model_validate(existing_rule)

        # Change the service to address
        # ?
        # ?
        # ?
        # ?

        # Da modello lo passo in dizionario
        body: dict = http_route.model_dump(exclude_none=True)

        # Aggiorna l'oggetto chiamando l'API di K8S
        api_response = api_instance.patch_namespaced_custom_object(group, version, 'default', plural,
                                                                   http_route.metadata.name, body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CustomObjectsApi->create_cluster_custom_object: %s\n" % e)