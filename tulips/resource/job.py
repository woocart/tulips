from kubernetes import client as k8s
from kubernetes.client.models.v1_job import V1Job

from . import Resource


class Job(Resource):
    def delete(self, body: k8s.V1DeleteOptions):
        return k8s.BatchV1Api(self.client).delete_namespaced_job(
            body=body, namespace=self.namespace, name=self.name
        )

    def create(self) -> V1Job:
        return k8s.BatchV1Api(self.client).create_namespaced_job(
            body=self.resource, namespace=self.namespace
        )

    def status(self) -> V1Job:
        return k8s.BatchV1Api(self.client).read_namespaced_job_status(
            name=self.name, namespace=self.namespace
        )
