[![CircleCI](https://circleci.com/gh/woocart/tulips/tree/master.svg?style=svg&circle-token=631d7a818d7fade30fefe2a23c936d28aaa92ffa)](https://circleci.com/gh/woocart/tulips/tree/master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Type checker: mypy](https://img.shields.io/badge/type%20checker-mypy-1F5082.svg)](https://github.com/python/mypy)
[![Packaging: poetry](https://img.shields.io/badge/packaging-poetry-C2CAFD.svg)](https://poetry.eustace.io/)
[![Packaging: poetry](https://img.shields.io/badge/packaging-pypi-006dad.svg)](https://pypi.org/project/tulips/)
[![codecov](https://codecov.io/github/woocart/tulips/branch/master/graph/badge.svg)](https://codecov.io/github/woocart/tulips/)

# Tulips

A small wrapper around https://github.com/kubernetes-client/python which understands Kubernetes charts.

## Why

I needed something simple that would read Helm charts and push them to the Kubernetes cluster and
be extensible. So something like helm+kubectl with ability to write you own tools around them.

## Supported CRDS aka Kubernetes resources

- Deployment
- Service
- Ingress
- Secret
- Issuer (cert-manager)
- PersistentVolumeClaim

## Example use

```python

import yaml
from tulips.resources import ResourceRegistry
from kubernetes import client as k8s
from kubernetes import config


client = config.new_client_from_config('kube.conf')

spec = yaml.load('ingress.yaml')

ingress_cls = ResourceRegistry.get_cls(spec['kind'])
ingress = ingress_cls(config.client, namespace='default', spec)
ingress.create()  # Create Ingress resource
ingress.delete()  # Delete Ingress resource
```

## Adding new resource

In order to add support for new Kubernetes resource, one needs to create class
that inherits from `tulips.resources.Resource` class.

### Example resource

```python
import tulips.resources.Resource

class ClusterIssuer(Resource):
    """A `cert-manager` ClusterIssuer resource."""

    version = "v1alpha1"
    group = "certmanager.k8s.io"
    plural = "clusterissuers"

    def delete(self, body: k8s.V1DeleteOptions):
        return k8s.CustomObjectsApi(
            self.client
        ).delete_namespaced_custom_object(
            body=body,
            namespace=self.namespace,
            version=self.version,
            group=self.group,
            plural=self.plural,
            name=self.name,
        )

    def create(self):
        return k8s.CustomObjectsApi(
            self.client
        ).create_namespaced_custom_object(
            body=self.resource,
            namespace=self.namespace,
            version=self.version,
            group=self.group,
            plural=self.plural,
        )
```

It will be registered into the `ResourceRegistry` and can be fetched via `ResourceRegistry.get_cls` method.

## Tulip

Tulip is a sample client that emulates Helm but without `tiller`.

```shell
$ python tulips push --help                                    06/25/18 -  9:49
Usage: tulips push [OPTIONS] CHART

  You can pass chart variables via foo=bar, for example '$ tulip push
  app.yaml foo=bar'

Options:
  --namespace TEXT   Kubernetes namespace
  --release TEXT     Name of the release
  --kubeconfig PATH  Path to kubernetes config
  --help             Show this message and exit.

```

### Example client

Let's say that I want to deploy a Secret and Ingress

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ release }}-secrets
type: Opaque
data:
  password: {{ @pwd }}
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ release }}-web-ingress
  labels:
    app: woocart-{{ release }}
  annotations:
    nginx.ingress.kubernetes.io/limit-connections: "100"
    kubernetes.io/ingress.class: nginx
spec:
  defaultBackend:
    service:
      name: {{ release }}-web-ingress
      port:
        number: 80
  rules:
  - host: {{ domain }}
    http:
      paths:
        - path: /
          pathType: ImplementationSpecific
          backend:
            service:
              name: {{ release }}-web
            port:
              number: 80
```

If one runs `tulip --release test push --kubeconf kube.conf app.yaml domain=test.tld'

Spec file is inspected and all `{{ variables }}` are replaced with real values. Also
special `{{ @pwd }}` will generate strong password using `passlib` library.
