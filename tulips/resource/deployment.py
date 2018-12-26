from kubernetes import client as k8s

from . import Resource


class Deployment(Resource):
    def delete(self, body: k8s.V1DeleteOptions):
        return k8s.AppsV1Api(self.client).delete_namespaced_deployment(
            body=body, namespace=self.namespace, name=self.name
        )

    def create(self):
        return k8s.AppsV1Api(self.client).create_namespaced_deployment(
            body=self.resource, namespace=self.namespace
        )

    def read(self):
        return k8s.AppsV1Api(self.client).read_namespaced_stateful_set_status(
            name=self.name, namespace=self.namespace
        )

    def patch(self):
        return k8s.AppsV1Api(self.client).patch_namespaced_deployment(
            name=self.name, body=self.resource, namespace=self.namespace
        )
