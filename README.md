[![Build Status](https://travis-ci.com/dz0ny/tulips.svg?branch=master)](https://travis-ci.com/dz0ny/tulips)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Type checker: mypy](https://img.shields.io/badge/type%20checker-mypy-1F5082.svg)](https://github.com/python/mypy)
[![Packaging: poetry](https://img.shields.io/badge/packaging-poetry-C2CAFD.svg)](https://poetry.eustace.io/)

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
from tulips import class_for_resource
from kubernetes import client as k8s
from kubernetes import config


client = config.new_client_from_config('kube.conf')

spec = yaml.load('ingress.yaml')

ingress_cls = class_for_resource(spec['kind'])
ingress = ingress_cls(config.client, namespace='default', spec)
ingress.create()  # Create Ingress resource
ingress.delete()  # Delete Ingress resource
```

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

### Example

Let's say that I want to deploy a Secret and Ingress

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: <%=release=%>-secrets
type: Opaque
data:
  password: <%=@pwd=%>
---
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: <%=release=%>-web-ingress
  labels:
    app: woocart-<%=release=%>
  annotations:
    nginx.ingress.kubernetes.io/limit-connections: "100"
    kubernetes.io/ingress.class: nginx
spec:
  rules:
  - host: <%=domain=%>
    http:
      paths:
        - path: /
          backend:
            serviceName: <%=release=%>-web
            servicePort: 80
```

If one runs `tulip --release test push --kubeconf kube.conf app.yaml domain=test.tld'

Spec file is inspected and all `<%=variables=%>` are replaced with real values. Also
special `<%=@pwd=%>` will generate strong password using `passlib` library.

## TODO

- [ ] Custom container for yaml(eliminates class_for_kind function)
