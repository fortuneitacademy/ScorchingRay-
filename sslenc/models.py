from django.db import models

# Create your models here.

from django.db import models
from django.urls import (
    reverse,
    NoReverseMatch,
)


class AcmeChallenge(models.Model):
    """
    Simple model to handle Let's Encrypt .well-known/acme-challenge objects
    """

    challenge = models.CharField(
        help_text='The identifier for this challenge',
        unique=True,
        max_length=255,
    )

    response = models.CharField(
        help_text='The response expected for this challenge',
        max_length=255,
    )

    def __str__(self):
        return self.challenge

    def get_acme_url(self):
        """
        Get the URL to this ACME challenge
        :return: The URL as a string
        """
        try:
            return reverse(
                viewname='detail',
                current_app='sslenc',
                args=[self.challenge],
            )
        except NoReverseMatch:
            return ''

    class Meta:
        verbose_name = 'ACME Challenge'
        verbose_name_plural = 'ACME Challenges'
