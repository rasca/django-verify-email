from django.http import HttpResponse

from verify_email.decorators import verify_email

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

