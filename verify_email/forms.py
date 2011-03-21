from django import forms

from verify_email.models import Verification

class VerifyEmailForm(forms.Form):
    email = forms.EmailField()

    def save(self, request):
        """
        Creates a new Verification and sends an email with the link
        """
        verification = Verification.objects.create(
            email=self.cleaned_data['email'])
        verification.send_verification_email(request.build_absolute_uri())

