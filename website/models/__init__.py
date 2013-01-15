"""
Models for the website-specific areas of LASS.

"""

from website.models.banner import Banner, BannerType
Banner = Banner
BannerType = BannerType

from website.models.banner import BannerCampaign, BannerLocation
BannerCampaign = BannerCampaign
BannerLocation = BannerLocation

from website.models.banner import BannerTimeslot
BannerTimeslot = BannerTimeslot

from website.models.blog import Blog
Blog = Blog

from website.models.website_class import Website
Website = Website

from website.models.website_class import WebsitePackageEntry
WebsitePackageEntry = WebsitePackageEntry

from website.models.website_class import WebsiteTextMetadata
WebsiteTextMetadata = WebsiteTextMetadata

from website.models.website_class import WebsiteImageMetadata
WebsiteImageMetadata = WebsiteImageMetadata

# v-- Temporary
from website.models.sis_comm import SISComm
SISComm = SISComm
