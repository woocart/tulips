from kubernetes import client as k8s
from kubernetes.client.models.v1_resource_quota import V1ResourceQuota

from . import Resource


class ResourceQuota(Resource):
    def delete(self, body: k8s.V1DeleteOptions):
        return k8s.CoreV1Api(self.client).delete_namespaced_resource_quota(
            body=body, namespace=self.namespace, name=self.name
        )

    def create(self) -> V1ResourceQuota:
        return k8s.CoreV1Api(self.client).create_namespaced_resource_quota(
            body=self.resource, namespace=self.namespace
        )

    def read(self) -> V1ResourceQuota:
        return k8s.CoreV1Api(self.client).read_namespaced_resource_quota(
            name=self.name, namespace=self.namespace
        )

    def status(self) -> V1ResourceQuota:
        return k8s.CoreV1Api(
            self.client
        ).read_namespaced_resource_quota_status(
            name=self.name, namespace=self.namespace
        )

    def patch(self) -> V1ResourceQuota:
        return k8s.CoreV1Api(self.client).patch_namespaced_resource_quota(
            body=self.resource, name=self.name, namespace=self.namespace
        )
