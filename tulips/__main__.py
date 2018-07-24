import click
import structlog
import yaml
from kubernetes import client as k8s
from kubernetes.client.rest import ApiException

from .tulip import Tulip

log = structlog.get_logger("tulip")

__version__ = "0.0.3"


@click.group()
def cli():
    pass


@click.command(
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True),
    help=(
        "You can pass chart variables via foo=bar, "
        "for example '$ tulip push app.yaml foo=bar'"
    ),
)
@click.argument("chart", type=click.Path(exists=True))
@click.option("--namespace", default="default", help="Kubernetes namespace")
@click.option("--release", help="Name of the release")
@click.option(
    "--kubeconfig",
    help="Path to kubernetes config",
    default="/home/dz0ny/.kube/config",
    type=click.Path(exists=True),
)
@click.pass_context
def push(ctx, chart, namespace, release, kubeconfig):
    options = {
        ".Release.Name": release,
        "namespace": namespace,
        "chart": chart,
    }
    for item in ctx.args:
        options.update([item.split("=")])
    click.echo(options)
    client = Tulip(kubeconfig, namespace, options, chart)
    for resource in client.resources():
        try:
            resource.create()
            log.info(
                "Created",
                name=resource.name,
                Resource=resource.__class__.__name__,
            )
        except ApiException as e:
            log.error(
                "Failed creating",
                name=resource.name,
                Resource=chart.__class__.__name__,
                reason=e.reason,
            )


@click.command(
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True),
    help=(
        "You can pass chart variables via foo=bar, "
        "for example '$ tulip push app.yaml foo=bar'"
    ),
)
@click.argument("chart", type=click.Path(exists=True))
@click.option("--namespace", default="default", help="Kubernetes namespace")
@click.option("--release", help="Name of the release")
@click.option(
    "--kubeconfig",
    help="Path to kubernetes config",
    default="/home/dz0ny/.kube/config",
    type=click.Path(exists=True),
)
@click.pass_context
def status(ctx, chart, namespace, release, kubeconfig):
    options = {
        ".Release.Name": release,
        "namespace": namespace,
        "chart": chart,
    }
    for item in ctx.args:
        options.update([item.split("=")])
    client = Tulip(kubeconfig, namespace, options, chart)
    for resource in client.resources():
        try:
            click.echo(resource.status().status)
        except ApiException as e:
            log.error(
                "Failed getting info",
                name=resource.name,
                Resource=chart.__class__.__name__,
                reason=e.reason,
            )


@click.command(
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True),
    help=(
        "You can pass chart variables via foo=bar, "
        "for example '$ tulip push app.yaml foo=bar'"
    ),
)
@click.argument("chart", type=click.Path(exists=True))
@click.option("--namespace", default="default", help="Kubernetes namespace")
@click.option("--release", help="Name of the release")
@click.option(
    "--kubeconfig",
    help="Path to kubernetes config",
    default="/home/dz0ny/.kube/config",
    type=click.Path(exists=True),
)
@click.pass_context
def echo(ctx, chart, namespace, release, kubeconfig):
    options = {
        ".Release.Name": release,
        "namespace": namespace,
        "chart": chart,
    }
    for item in ctx.args:
        options.update([item.split("=")])
    click.echo(options)
    client = Tulip(kubeconfig, namespace, options, chart)
    for resource in client.resources():
        click.echo(yaml.dump(resource.resource))


@click.command(
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True),
    help=(
        "You can pass chart variables via foo=bar, "
        "for example '$ tulip rm app.yaml foo=bar'"
    ),
)
@click.argument("chart", type=click.Path(exists=True))
@click.option("--namespace", default="default", help="Kubernetes namespace")
@click.option("--release", help="Name of the release")
@click.option(
    "--kubeconfig",
    help="Path to kubernetes config",
    type=click.Path(exists=True),
)
@click.pass_context
def rm(ctx, chart, namespace, release, kubeconfig):
    options = {"release": release, "namespace": namespace, "chart": chart}
    for item in ctx.args:
        options.update([item.split("=")])
    click.echo(options)
    client = Tulip(kubeconfig, namespace, options, chart)
    delete = k8s.V1DeleteOptions(
        propagation_policy="Foreground", grace_period_seconds=5
    )
    for chart in client.resources():
        try:
            chart.delete(body=delete)
            log.info(
                "Deleted", name=chart.name, Resource=chart.__class__.__name__
            )
        except ApiException as e:
            log.error(
                "Failed deleting",
                name=chart.name,
                Resource=chart.__class__.__name__,
                reason=e.reason,
            )


if __name__ == "__main__":
    cli.add_command(rm)
    cli.add_command(push)
    cli.add_command(echo)
    cli.add_command(status)
    cli()
