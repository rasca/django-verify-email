# Create your views here.
from django.views.generic.edit import FormView

from verify_email.forms import VerifyEmailForm


class VerifyEmailView(FormView):
    form_class = VerifyEmailForm
    template_name = 'verify_email/form.html'
    success_url = 'verify_email/thank_you.html'

    def form_valid(self, form):
        form.save(self.request)
        return super(VerifyEmailView, self).form_valid(form)

