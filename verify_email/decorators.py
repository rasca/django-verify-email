from datetime import timedelta

from verify_email.models import Verification

def verify_email(expiration_period=timedelta(weeks=1), expires_on_usage=False,
                 view=None):
    """
    Decorator for resticting access based on email verification
    """
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            if 'hash' in request.GET:
                verification = Verification.objects.validate(
                    hash=request.GET['hash'],
                    expiration_period=expiration_period,
                    expires_on_usage=expires_on_usage)

                if verification:
                    return view_func(request, email=verification, *args, **kwargs)

            if view:
                return view(request, *args, **kwargs)
            else:
                return view_func(request, email=None, *args, **kwargs)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view
    return _dec
