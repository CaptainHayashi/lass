import urlparse
from django.template import Library
from django.templatetags.future import URLNode, url
from django.contrib.sites.models import Site

register = Library()


class AbsoluteURLNode(URLNode):
    def render(self, context):
        path = super(AbsoluteURLNode, self).render(context)
        domain = "://".join(
            "http",
            Site.objects.get_current().domain
        )
        return urlparse.urljoin(domain, path)


@register.tag()
def absolute_url(parser, token, node_cls=AbsoluteURLNode):
    """Just like {% url %} but adds the domain of the current site."""
    node_instance = url(parser, token)
    return node_cls(
        view_name=node_instance.view_name,
        args=node_instance.args,
        kwargs=node_instance.kwargs,
        asvar=node_instance.asvar
    )
