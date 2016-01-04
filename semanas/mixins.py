from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class AnonymousRequiredMixin(object):
    @method_decorator(
        user_passes_test(lambda user: not user.username, login_url=settings.HOME_URL, redirect_field_name=None))
    def dispatch(self, *args, **kwargs):
        return super(AnonymousRequiredMixin, self).dispatch(*args, **kwargs)
