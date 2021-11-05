from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        print(modulename)
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "quiz_center.Adminviews":
                    pass
                elif modulename == "quiz_center.views" or modulename == "django.views.static":
                    pass
                elif modulename == "django.contrib.auth.views" or modulename == "django.contrib.admin.sites":
                    pass
                else:
                    return HttpResponseRedirect(reverse("index"))
            elif user.user_type == "2":
                if modulename == "quiz_center.Participantviews":
                    pass
                elif modulename == "quiz_center.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("participant_page"))

            else:
                return HttpResponseRedirect(reverse("login_page"))

        else:
            if request.path == reverse("login_page") or request.path == reverse("dologin") or modulename == "django.contrib.auth.views":
                pass
            else:
                return HttpResponseRedirect(reverse("login_page"))