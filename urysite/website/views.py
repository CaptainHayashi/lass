from website.models import Banner
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from random import choice


def index(request):
    banner = choice(Banner.objects.all())
    return render(request, 'website/index.html')
