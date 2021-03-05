from kubernetes import client as k8s
from kubernetes.client.models.v1_horizontal_pod_autoscaler import (
    V1HorizontalPodAutoscaler,
)

from . import Resource


class HorizontalPodAutoscaler(Resource):
    def delete(self, body: k8s.V1DeleteOptions):
        return k8s.AutoscalingV1Api(
            self.client
        ).delete_namespaced_horizontal_pod_autoscaler(
            body=body, namespace=self.namespace, name=self.name
        )

    def create(self) -> V1HorizontalPodAutoscaler:
        return k8s.AutoscalingV1Api(
            self.client
        ).create_namespaced_horizontal_pod_autoscaler(
            body=self.resource, namespace=self.namespace
        )

    def read(self) -> V1HorizontalPodAutoscaler:
        return k8s.AutoscalingV1Api(
            self.client
        ).read_namespaced_horizontal_pod_autoscaler(
            name=self.name, namespace=self.namespace
        )

    def patch(self):
        return k8s.AutoscalingV1Api(
            self.client
        ).patch_namespaced_horizontal_pod_autoscaler(
            name=self.name, body=self.resource, namespace=self.namespace
        )
