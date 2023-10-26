import kubernetes.client
import yaml
from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.rest import ApiException
from pprint import pprint
from tcp_route_model import TCPRoute, build_tcp_rule

def get_k8s_config_from_file(filepath: str) -> kubernetes.client.Configuration:
    """
    Create a kube client config from the configuration file.
    @param filepath: the path of the configuration file

    @return kube client configuration
    """
    kube_client_config = type.__call__(Configuration)
    config.load_kube_config(config_file=filepath, context=None, client_configuration=kube_client_config,
                            persist_config=False)
    kube_client_config.verify_ssl = False

    return kube_client_config

def update_tcp_route():
    file = "cluster.config"
    configuration = get_k8s_config_from_file(filepath=file)

    #tcp_rule = build_tcp_rule(tcp_rule_name="iperfroute", gateway_name="iperf-gateway", service_to_point="iperf-service-a",
    #                      port_of_serv=3212)


    # Enter a context with an instance of the API kubernetes.client
    with kubernetes.client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = kubernetes.client.CustomObjectsApi(api_client)
        group = 'gateway.networking.k8s.io'  # str | The custom resource's group name
        version = 'v1alpha2'  # str | The custom resource's version
        plural = 'tcproutes'  # str | The custom resource's plural name. For TPRs this would be lowercase plural kind.

    try:
        existing_rule = api_instance.get_namespaced_custom_object(group,version,'default',
                                                                  plural, "iperfroute")
        tcp_rule = TCPRoute.model_validate(existing_rule)

        # Inverting the zone
        if tcp_rule.spec.rules[0].backendRefs[0].name == "iperf-service-a":
            tcp_rule.spec.rules[0].backendRefs[0].name = "iperf-service-b"
        else:
            tcp_rule.spec.rules[0].backendRefs[0].name = "iperf-service-a"

        body: dict = tcp_rule.model_dump()

        api_response = api_instance.patch_namespaced_custom_object(group, version, 'default', plural,
                                                                   tcp_rule.metadata.name, body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CustomObjectsApi->create_cluster_custom_object: %s\n" % e)

