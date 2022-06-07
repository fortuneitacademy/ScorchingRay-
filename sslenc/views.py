from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import AcmeChallenge


def detail(request, acme_data):
    acme_challenge = get_object_or_404(
        AcmeChallenge,
        challenge=acme_data,
    )

    return HttpResponse(acme_challenge.response, content_type="text/plain")
