from kubernetes import client as k8s

from tulips.tulip import Tulip
from pathlib import Path


def test_create_namespace(mocker):
    api = mocker.patch("kubernetes.config.new_client_from_config")

    t = Tulip("conf", "my_namespace", {}, "fixtures")
    t.create_namespace()
    body = api.return_value.call_api.call_args[1]["body"]
    assert body.metadata.name == "my_namespace"
    assert api.return_value.call_api.call_args[0][0] == "/api/v1/namespaces"


def test_delete_namespace(mocker):
    api = mocker.patch("kubernetes.config.new_client_from_config")

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


def test_resources(mocker):
    mocker.patch("kubernetes.config.new_client_from_config")

    t = Tulip("conf", "my_namespace", {}, "fixtures")
    delme = k8s.V1DeleteOptions(
        propagation_policy="Foreground", grace_period_seconds=5
    )
    order = []
    for r in t.resources():
        order.append(r.name)
        r.create()
        r.delete(body=delme)
        r.status()
        r.patch()

    assert order == ['my-secrets', 'test-volume']


def test_parsing(mocker):
    mocker.patch("kubernetes.config.new_client_from_config")

    t = Tulip("conf", "my_namespace", {}, "fixtures")
    out = t.prepare(Path("./tests/fixtures/parse.yaml"), {".test.var": 1234})

    assert ".test.var" not in out
    assert '"1234"' in out
