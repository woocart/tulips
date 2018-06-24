from tulips import class_for_resource
from tulips.resource.deployment import Deployment
from tulips.resource.ingress import Ingress
from tulips.resource.issuer import Issuer
from tulips.resource.persistentvolumeclaim import PersistentVolumeClaim
from tulips.resource.secret import Secret
from tulips.resource.service import Service


class TestResource:
    """Unit tests for the `class_for_resource` function."""

    def test_instance_methods_can_be_called(self):
        cls = class_for_resource("Ingress")
        assert cls is Ingress
        cls = class_for_resource("Deployment")
        assert cls is Deployment
        cls = class_for_resource("Service")
        assert cls is Service
        cls = class_for_resource("Secret")
        assert cls is Secret
        cls = class_for_resource("Issuer")
        assert cls is Issuer
        cls = class_for_resource("PersistentVolumeClaim")
        assert cls is PersistentVolumeClaim
