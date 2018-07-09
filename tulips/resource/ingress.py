from kubernetes import client as k8s

from . import Resource


class Ingress(Resource):
    def delete(self, body: k8s.V1DeleteOptions):
        return k8s.ExtensionsV1beta1Api(self.client).delete_namespaced_ingress(
            body=body, namespace=self.namespace, name=self.name
        )

    def create(self):
        return k8s.ExtensionsV1beta1Api(self.client).create_namespaced_ingress(
            body=self.resource, namespace=self.namespace
        )

    def status(self):
        return k8s.ExtensionsV1beta1Api(
            self.client
        ).read_namespaced_ingress_status(
            name=self.name, namespace=self.namespace
        )
