"""
The singleton class that allows metadata and other attachables to be
attached to the entire website.

As the website at this level is one item of data rather than an entire
model, we have to use a singleton class to attach metadata to it.

"""

from django.conf import settings

from metadata.models import PackageEntry, ImageMetadata, TextMetadata
from metadata.mixins import MetadataSubjectMixin


class Website(MetadataSubjectMixin):
    """
    Singleton class representing the website itself.

    This does not hold any data on its own, so in order to acquire a
    website object for running metadata queries, just run Website().

    """

    def metadata_strands(self):
        return {
            "text": self.websitetextmetadata_set,
            "image": self.websiteimagemetadata_set,
        }

    def packages(self):
        return self.websitepackageentry_set


WebsiteTextMetadata = TextMetadata.make_model(
    Website,
    'website',
    table=getattr(settings, 'WEBSITE_TEXT_METADATA_DB_TABLE', None),
    id_column=getattr(settings, 'WEBSITE_TEXT_METADATA_DB_ID_COLUMN', None),
    fkey=None,
)


WebsiteImageMetadata = ImageMetadata.make_model(
    Website,
    'website',
    table=getattr(settings, 'WEBSITE_IMAGE_METADATA_DB_TABLE', None),
    id_column=getattr(settings, 'WEBSITE_IMAGE_METADATA_DB_ID_COLUMN', None),
    fkey=None,
)


WebsitePackageEntry = PackageEntry.make_model(
    Website,
    'website',
    table=getattr(settings, 'WEBSITE_PACKAGE_ENTRY_DB_TABLE', None),
    id_column=getattr(settings, 'WEBSITE_PACKAGE_ENTRY_DB_ID_COLUMN', None),
    fkey=None,
)
