import abc

from kubernetes import client as k8s


class Resource(metaclass=abc.ABCMeta):
    """Resource is interface that describes Kubernetes Resource defintion."""

    resource: dict
    client: k8s.ApiClient
    namespace: str

    def __init__(
        self, client: k8s.ApiClient, namespace: str, resource: dict
    ) -> None:
        """Initializes resource or CRD.

        Args:
            client (k8s.ApiClient): Instance of the Kubernetes client.
            namespace (str): Namespace where Workload should be deployed.
            resource (dict): Kubernetes resource or CRD.
        """

        self.client = client
        self.namespace = namespace
        self.resource = resource

    @abc.abstractmethod
    def create(self):
        pass

    @abc.abstractmethod
    def delete(self, options: k8s.V1DeleteOptions):
        pass

    @property
    def name(self):
        return self.resource["metadata"]["name"]
