from kubernetes import client as k8s

from . import Resource


class StatefulSet(Resource):
    def delete(self, body: k8s.V1DeleteOptions):
        return k8s.AppsV1Api(self.client).delete_namespaced_stateful_set(
            body=body, namespace=self.namespace, name=self.name
        )

    def create(self):
        return k8s.AppsV1Api(self.client).create_namespaced_stateful_set(
            body=self.resource, namespace=self.namespace
        )

    def status(self):
        return k8s.AppsV1Api(self.client).read_namespaced_stateful_set_status(
            name=self.name, namespace=self.namespace
        )
