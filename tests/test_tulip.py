import unittest.mock as mock

from kubernetes import client as k8s

from tulips.tulip import Tulip


class TestTulip:
    """Unit tests for the `Tulip` class."""

    @mock.patch("kubernetes.config.new_client_from_config")
    def test_create_namespace(self, api):
        t = Tulip("conf", "my_namespace", {}, "fixtures")
        t.create_namespace()
        body = api.return_value.call_api.call_args[1]["body"]
        assert body.metadata.name == "my_namespace"
        assert (
            api.return_value.call_api.call_args[0][0] == "/api/v1/namespaces"
        )

    @mock.patch("kubernetes.config.new_client_from_config")
    def test_delete_namespace(self, api):
        t = Tulip("conf", "my_namespace", {}, "fixtures")
        t.delete_namespace()
        body = api.return_value.call_api.call_args[1]["body"]
        assert body.propagation_policy == "Foreground"
        assert (
            api.return_value.call_api.call_args[0][0]
            == "/api/v1/namespaces/{name}"
        )
        assert api.return_value.call_api.call_args[0][1] == "DELETE"
        assert api.return_value.call_api.call_args[0][2] == {
            "name": "my_namespace"
        }

    @mock.patch("kubernetes.config.new_client_from_config")
    def test_resources(self, api):
        t = Tulip("conf", "my_namespace", {}, "fixtures")
        delme = k8s.V1DeleteOptions(
            propagation_policy="Foreground", grace_period_seconds=5
        )
        for r in t.resources():
            r.create()
            r.delete(body=delme)
            r.status()
