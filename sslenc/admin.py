from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.utils.html import format_html

from .models import AcmeChallenge


class AcmeChallengeAdmin(admin.ModelAdmin):
    """Admin options for the ACME Challenge"""

    def format_acme_url(self, acme_object):
        """Format the ACME url from the ACME challenge object"""
        object_url = acme_object.get_acme_url()

        if object_url:
            return format_html(
                "<a href='{}'>ACME Challenge Link</a>",
                object_url,
            )

        return '-'
    format_acme_url.short_description = 'Link'

    fieldsets = [
        ('ACME Request', {
            'fields': [
                'challenge',
                'response',
            ],
        }),
        ('Metadata', {
            'fields': [
                'id',
                'format_acme_url',
            ],
        }),
    ]

    list_display = (
        'challenge',
        'format_acme_url',
    )

    ordering = [
        'challenge',
    ]

    readonly_fields = [
        'id',
        'format_acme_url',
    ]

    search_fields = [
        'challenge',
        'response',
    ]


admin.site.register(AcmeChallenge, AcmeChallengeAdmin)