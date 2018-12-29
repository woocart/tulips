import pytest


@pytest.fixture(scope="function")
def k8s_client(mocker):
    """Mock Kubernetes client."""
    mocker.patch(
        "kubernetes.config.kube_config._get_kube_config_loader_for_yaml_file"
    )
    yield mocker.patch("kubernetes.config.new_client_from_config")
