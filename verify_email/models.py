import os, datetime

from django.conf import settings
from django.db import models
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class VerificationManager(models.Manager):
    def validate(self, hash, expiration_period=None,
                 expires_on_usage=None):
        # We first check for the hash
        try:
            verification = Verification.objects.get(hash=hash)

            # Now we check for the expiration_period
            if (expiration_period is not None and expiration_period <
                    datetime.datetime.today() - verification.created):
                return False

            # And finally we check if it's been used already
            if expires_on_usage and verification.used:
                return False

            # We marked it's been used
            verification.used = True
            verification.save()

            return verification.email

        except Verification.DoesNotExist:
            return False


class Verification(models.Model):
    """
    Records the hash for different emails
    """
    hash = models.CharField(primary_key=True, max_length=64)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    objects = VerificationManager()

    def create_hash(self):
        """
        Generates a random hash
        """
        return os.urandom(32).encode('hex') 

    def save(self, *args, **kwargs):
        # Let's create an unique hash
        if not self.pk:
            self.hash = self.create_hash()
        return super(Verification, self).save(*args, **kwargs)

    def send_verification_email(self, url, template, subject):
        context = {'verification': self, 'url': url, }

        # The subject can't contain newlines
        subject = ''.join(subject.splitlines())
        
        message = render_to_string(template, context)
        
        msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL,
                           [self.email, ])
        msg.content_subtype = 'html'

        try: 
            msg.send()
        except: #BadHeaderError:
            pass

