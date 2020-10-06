from kubernetes import client as k8s

from . import Resource


class Issuer(Resource):
    """A `cert-manager` Issuer resource."""

    version = "v1"
    group = "cert-manager.io"
    plural = "issuers"

    def delete(self, body: k8s.V1DeleteOptions):
        return k8s.CustomObjectsApi(
            self.client
        ).delete_namespaced_custom_object(
            body=body,
            namespace=self.namespace,
            version=self.version,
            group=self.group,
            plural=self.plural,
            name=self.name,
        )

    def create(self):
        return k8s.CustomObjectsApi(
            self.client
        ).create_namespaced_custom_object(
            body=self.resource,
            namespace=self.namespace,
            version=self.version,
            group=self.group,
            plural=self.plural,
        )

    def read(self):
        return k8s.CustomObjectsApi(self.client).get_namespaced_custom_object(
            name=self.name,
            namespace=self.namespace,
            version=self.version,
            group=self.group,
            plural=self.plural,
        )

    def patch(self):
        return k8s.CustomObjectsApi(
            self.client
        ).patch_namespaced_custom_object(
            body=self.resource,
            name=self.name,
            namespace=self.namespace,
            version=self.version,
            group=self.group,
            plural=self.plural,
        )
