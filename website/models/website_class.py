"""
The singleton class that allows metadata and other attachables to be
attached to the entire website.

As the website at this level is one item of data rather than an entire
model, we have to use a singleton class to attach metadata to it.

"""

from django.conf import settings
from django.contrib.sites.models import Site

from metadata.models import PackageEntry, ImageMetadata, TextMetadata
from metadata.mixins import MetadataSubjectMixin


class Website(MetadataSubjectMixin):
    """
    Class representing the website itself.

    This does not hold any data on its own, so in order to acquire a
    website object for running metadata queries, just run Website().

    """

    def __init__(self, request):
        """
        Initialises a Website object.

        :param request: The HttpRequest object of the current page.
        :type request: HttpRequest
        :rtype: Website

        """
        self.request = request
        self.pk = 1  # Needed for the metadata system

    def metadata_strands(self):
        return {
            "text": WebsiteTextMetadata.objects,
            "image": WebsiteImageMetadata.objects,
        }

    def packages(self):
        return WebsitePackageEntry.objects

    ## Template-exposed API ##
    def root(self):
        """
        Returns the URI of the root of the website, for concatenating
        things like STATIC_URL onto it.

        Please please PLEASE try using decoupling-friendly features
        such as 'get_absolute_uri' and whatnot before this.

        """
        return self.request.build_absolute_uri('/').rstrip('/')

    def site(self):
        """
        Returns the current Django Sites Framework site.

        """
        try:
            site = Site.objects.get_current()
        except Site.DoesNotExist:
            site = None
        return site


WebsiteTextMetadata = TextMetadata.make_model(
    Website,
    'website',
    table=getattr(
        settings,
        'WEBSITE_TEXT_METADATA_DB_TABLE',
        None
    ),
    id_column=getattr(
        settings,
        'WEBSITE_TEXT_METADATA_DB_ID_COLUMN',
        None
    ),
    fkey=None,
)


WebsiteImageMetadata = ImageMetadata.make_model(
    Website,
    'website',
    table=getattr(
        settings,
        'WEBSITE_IMAGE_METADATA_DB_TABLE',
        None
    ),
    id_column=getattr(
        settings,
        'WEBSITE_IMAGE_METADATA_DB_ID_COLUMN',
        None
    ),
    fkey=None,
)


WebsitePackageEntry = PackageEntry.make_model(
    Website,
    'website',
    table=getattr(
        settings,
        'WEBSITE_PACKAGE_ENTRY_DB_TABLE',
        None
    ),
    id_column=getattr(
        settings,
        'WEBSITE_PACKAGE_ENTRY_DB_ID_COLUMN',
        None
    ),
    fkey=None,
)
