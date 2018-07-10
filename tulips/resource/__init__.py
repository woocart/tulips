import abc

from kubernetes import client as k8s
import typing as t


class UndefinedResource(Exception):
    """Resource was not defined error."""

    def __init__(self, kind: str) -> None:
        self.str = kind
        Exception.__init__(
            self, f"{kind} is not yet defined[{ResourceRegistry.REGISTRY}]"
        )


class ResourceRegistry(type):

    REGISTRY: dict = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        cls.REGISTRY[new_cls.__name__] = new_cls
        return new_cls

    @classmethod
    def get_cls(cls, kind: str) -> t.Callable:
        """Get Class for provided kind.

        Args:
            kind (str): Name of the kind that implements Resource.

        Raises:
            UndefinedResource: Resource class for provided kind is not defined.

        Returns:
            t.Callable: [Resource] class that implements resource.
        """

        kind_cls = cls.REGISTRY.get(kind)
        if not kind_cls:
            raise UndefinedResource(kind)
        return kind_cls


class Resource(metaclass=ResourceRegistry):
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
        """Create Resource."""
        pass

    @abc.abstractmethod
    def delete(self, body: k8s.V1DeleteOptions):
        """Delete Resource."""
        pass

    @abc.abstractmethod
    def status(self):
        """Info about Resource."""
        pass

    @property
    def name(self):
        """Returns the class kind.

        Returns:
            [str]: Base name of the class and kind
        """

        return self.resource["metadata"]["name"]
