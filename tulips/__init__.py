import importlib
import typing as t
from .resource import Resource

from kubernetes import client as k8s


def class_for_resource(
    kind: str
) -> t.Callable[[k8s.ApiClient, str, dict], Resource]:
    """Return Kubernetes ResourceDefintion class.

    Args:
        kind (str): Resource name.

    Raises:
        ImportError: Resource is not defined.
            Example: Missing persistentvolumeclaim.py
        AttributeError: Resource has no Resource class.
            Example: Missing persistentvolumeclaim.PersistentVolumeClaim

    Returns:
        t.Callable[Resource]: Resource operator.
    """

    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(
        f".resource.{kind.lower()}", package=__package__
    )
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, kind)
    return c
