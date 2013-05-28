"""Views for the URY site searching engine."""

from haystack.views import SearchView, search_view_factory
from haystack.forms import HighlightedModelSearchForm


class SitewideSearchView(SearchView):
    pass


def sitewide_search_view_factory():
    return search_view_factory(
        view_class=SitewideSearchView,
        form_class=HighlightedModelSearchForm)
