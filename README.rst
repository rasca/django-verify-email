===================
django-verify-email
===================

Ever wanted to allow access to a certain page only to verified users, but
without the hassle of registration?

This apps lets you verify an email, and then grant access to a certain view.

Sample usage:

    @verify_email
    def restricted_view(request, email):
        pass


The `email` parameter will be added to the kwargs by the decorator. It will
hold the verified email address or `None` if no email has been verified yet.

The first time someone tries to access restricted_view it should display
`VerifyEmailForm` which on POST will send the user an email with a link to
access the page.

A granted permission can have an expiration period and be available only once.
You can achieve this by passing arguments to the decorator:

* `expiration_period`: the period for which a mailed link is valid. It should
  be a `timedelta` or `None` for no expiration. Default: `timedelta(weeks=1)`

* `expires_on_usage`: defines if the maild link expires on first usage.
  Default: `False`

You can also delegate the responsability of displaying the `VerifyEmailForm`
and a thank you message to another view. For example:

    from django.views.generic.edit import FormView
    from verify_email.forms import VerifyEmailForm

    class VerifyEmailView(FormView):
       form_class = VerifyEmailForm 
       template_name = 'verify_email/form.html'
       success_url = 'verify_email/thank_you.html'

    @verify_email(view=VerifyEmailView.as_view())
    def restricted_view(request, email):
        pass

You can find VerifyEmailView in verify_email.views. You also should override
the default template and subject for the email. You can achieve this by setting
`verification_template` and `verification_subject`, or by overriding
`get_verification_template()` and `get_verification_subject()`.

I'm planning on adding support for sessions, so we can keep track of the
verifications. I'll implement this for the next release:

* `session_store`: the email get's stored in the session for later use on the
  same or other restricted views. Default `False`
