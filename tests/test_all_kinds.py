from tulips.resource import ResourceRegistry, UndefinedResource
from tulips.resource.configmap import ConfigMap
from tulips.resource.cronjob import CronJob
from tulips.resource.deployment import Deployment
from tulips.resource.ingress import Ingress
from tulips.resource.issuer import Issuer
from tulips.resource.persistentvolumeclaim import PersistentVolumeClaim
from tulips.resource.secret import Secret
from tulips.resource.service import Service
from tulips.resource.statefullset import StatefulSet


def test_instance_methods_can_be_called(k8s_client):
    cls = ResourceRegistry.get_cls("Ingress")
    assert cls is Ingress
    cls = ResourceRegistry.get_cls("Deployment")
    assert cls is Deployment
    cls = ResourceRegistry.get_cls("Service")
    assert cls is Service
    cls = ResourceRegistry.get_cls("Secret")
    assert cls is Secret
    cls = ResourceRegistry.get_cls("Issuer")
    assert cls is Issuer
    cls = ResourceRegistry.get_cls("PersistentVolumeClaim")
    assert cls is PersistentVolumeClaim
    cls = ResourceRegistry.get_cls("StatefulSet")
    assert cls is StatefulSet
    cls = ResourceRegistry.get_cls("CronJob")
    assert cls is CronJob
    cls = ResourceRegistry.get_cls("ConfigMap")
    assert cls is ConfigMap

    try:
        ResourceRegistry.get_cls("Foo")
    except UndefinedResource:
        pass


def test_all_calls(k8s_client):
    for cls in ResourceRegistry.REGISTRY.values():
        res = cls(k8s_client, "foo", {"metadata": {"name": "foo"}}, "file")
        res.read()
        res.patch()
        res.delete("")
        res.create()
