from django.http import HttpResponse

from verify_email.decorators import verify_email
from verify_email.views import VerifyEmailView

@verify_email()
def simple_view(request, email):
    if email:
        return HttpResponse(email)
    else:
        return HttpResponse('None')

def verify_view(request):
    return HttpResponse('VERIFY')

@verify_email(view=verify_view)
def other_view(request, email):
    return HttpResponse(email)

class VerifyEmailTemplateView(VerifyEmailView):
    verification_template = 'verification_email2.html'
    verification_subject = 'YOUR SUBJECT HERE2'

@verify_email(view=VerifyEmailTemplateView.as_view())
def other_view2(request, email):
    return HttpResponse(email)
