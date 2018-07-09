from kubernetes import client as k8s

from . import Resource


class Secret(Resource):
    def delete(self, body: k8s.V1DeleteOptions):
        return k8s.CoreV1Api(self.client).delete_namespaced_secret(
            body=body, namespace=self.namespace, name=self.name
        )

    def create(self):
        return k8s.CoreV1Api(self.client).create_namespaced_secret(
            body=self.resource, namespace=self.namespace
        )

    def status(self):
        return k8s.CoreV1Api(self.client).read_namespaced_secret(
            name=self.name, namespace=self.namespace
        )
