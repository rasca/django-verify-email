# Create your views here.
from django.views.generic.edit import FormView

from verify_email.forms import VerifyEmailForm


class VerifyEmailView(FormView):
    form_class = VerifyEmailForm
    template_name = 'verify_email/form.html'
    success_url = 'verify_email/thank_you.html'

    verification_template = 'verify_email/verification_email.html'
    verification_subject = 'YOUR SUBJECT HERE'

    def get_verification_template(self):
        if not self.verification_template:
            raise ImproperlyConfigured(
                "VerifyEmailForm requires either a definition of "
                "'verification_email_template' or an implementation of "
                "'get_verification_template()'")
        return self.verification_template

    def get_verification_subject(self):
        if not self.verification_subject:
            raise ImproperlyConfigured(
                "VerifyEmailForm requires either a definition of "
                "'verification_subject_template' or an implementation of "
                "'get_verification_subject()'")
        return self.verification_subject

    def form_valid(self, form):
        form.save(self.request, self.get_verification_template(),
                  self.get_verification_subject())
        return super(VerifyEmailView, self).form_valid(form)

