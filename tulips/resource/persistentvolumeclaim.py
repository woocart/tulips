from kubernetes import client as k8s

from . import Resource


class PersistentVolumeClaim(Resource):
    def delete(self, body: k8s.V1DeleteOptions):
        return k8s.CoreV1Api(
            self.client
        ).delete_namespaced_persistent_volume_claim(
            body=body, namespace=self.namespace, name=self.name
        )

    def create(self):
        return k8s.CoreV1Api(
            self.client
        ).create_namespaced_persistent_volume_claim(
            body=self.resource, namespace=self.namespace
        )

    def status(self):
        return k8s.CoreV1Api(
            self.client
        ).read_namespaced_persistent_volume_claim_status(
            name=self.name, namespace=self.namespace
        )
