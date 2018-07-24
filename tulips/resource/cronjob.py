from kubernetes import client as k8s
from kubernetes.client.models.v1beta1_cron_job import V1beta1CronJob

from . import Resource


class CronJob(Resource):
    def delete(self, body: k8s.V1DeleteOptions):
        return k8s.BatchV1beta1Api(self.client).delete_namespaced_cron_job(
            body=body, namespace=self.namespace, name=self.name
        )

    def create(self) -> V1beta1CronJob:
        return k8s.BatchV1beta1Api(self.client).create_namespaced_cron_job(
            body=self.resource, namespace=self.namespace
        )

    def status(self) -> V1beta1CronJob:
        return k8s.BatchV1beta1Api(
            self.client
        ).read_namespaced_cron_job_status(
            name=self.name, namespace=self.namespace
        )
