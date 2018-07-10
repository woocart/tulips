from kubernetes import client as k8s

from . import Resource


class Issuer(Resource):
    """A `cert-manager` Issuer resource."""

    version = "v1alpha1"
    group = "certmanager.k8s.io"
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

    def status(self):
        return k8s.CustomObjectsApi(self.client).get_namespaced_custom_object(
            name=self.name,
            namespace=self.namespace,
            version=self.version,
            group=self.group,
            plural=self.plural,
        )
