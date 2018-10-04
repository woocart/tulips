import base64
import re
import typing as t
from pathlib import Path

import yaml
from kubernetes import client as k8s
from kubernetes import config
from passlib import pwd

from tulips.resource import Resource, ResourceRegistry


class Tulip:
    def __init__(
        self,
        conf: str,
        namespace: str,
        meta: t.Dict,
        spec_path: str,
        override: str = None,
    ) -> None:
        """Manages deployment.

        Args:
            conf (str): Path to Kubernetes config.
            namespace (str): Kubernetes namespace.
            meta (t.Dict): Spec variables.
            spec_path (str): Location of chart to deploy.
            override (str): Override specific resource file, defaults to
             `resource.override.yaml` where one has `resource.yaml`.
        """

        self.client: k8s.ApiClient = config.new_client_from_config(conf)

        # Disable threadding pool inside swagger client
        # because it causes problems with other multithreading workers
        # as we don't use any async calls we are safe to do so.
        self.client.pool.close()
        self.client.pool.join()

        self.meta = meta
        self.namespace = namespace
        self.override = override if override else "override"
        self.spec_path = spec_path

    def create_namespace(self) -> k8s.V1NamespaceStatus:
        """Create namespace.

        Returns:
            k8s.V1NamespaceStatus
        """

        body = k8s.V1Namespace(
            metadata=k8s.V1ObjectMeta(
                name=self.namespace, labels={"store_id": self.namespace}
            )
        )
        return k8s.CoreV1Api(self.client).create_namespace(body)

    def delete_namespace(self) -> k8s.V1NamespaceStatus:
        """Delete namespace.

        Returns:
            k8s.V1NamespaceStatus
        """
        body = k8s.V1DeleteOptions(
            propagation_policy="Foreground", grace_period_seconds=5
        )
        return k8s.CoreV1Api(self.client).delete_namespace(
            self.namespace, body
        )

    def resources(self) -> t.Iterator[Resource]:
        """Deployment specification.

        Returns:
            t.Iterator[Resource]: Iterator over specifications
        """

        pattern = re.compile(r"^(.*)<%=(?:\s+)?(\S*)(?:\s+)?=%>(.*)$")
        yaml.add_implicit_resolver("!meta", pattern)
        maps = {"@pwd": lambda: base64.b64encode(pwd.genword(length=24))}
        maps.update(self.meta)

        def meta_constructor(loader, node):
            value = loader.construct_scalar(node)
            start, name, end = pattern.match(value).groups()
            val = maps[name]
            if name.startswith("@"):
                val = val()
            return start + val + end

        yaml.add_constructor("!meta", meta_constructor)
        path = Path(self.spec_path).joinpath("templates")

        for res in path.glob("*.yaml"):
            base_name = str(res.name)[:-5]  # strip .yaml
            override = res.parent.joinpath(
                "overrides", f"{base_name}.{self.override}.yaml"
            )
            # use override if it is found else use original file
            source_file = override if override.is_file() else res

            text = self.prepare(source_file)
            for spec in yaml.load_all(text):
                yield ResourceRegistry.get_cls(spec["kind"])(
                    self.client, self.namespace, spec, source_file
                )

    def prepare(self, f: Path) -> str:
        """Yaml parser trips at {{}} so we replace it with custom constructor.

        Arguments:
            f {Path} -- Path instance.

        Returns:
            str -- Updated yaml string of the resource.
        """

        return f.read_text().replace("{{", "<%=").replace("}}", "=%>")
