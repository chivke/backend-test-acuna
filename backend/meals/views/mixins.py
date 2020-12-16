from django.contrib.auth.mixins import AccessMixin


class NoraRequiredMixin(AccessMixin):
    '''Verify that the current user is Nora.'''
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated \
           and request.user.profile.is_nora:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()
