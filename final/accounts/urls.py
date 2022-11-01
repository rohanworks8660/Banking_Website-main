from django.conf.urls import url
from . import views
from django.urls import path,include

app_name = "accounts"

urlpatterns = [
    url(r"^register/$", views.register, name = "signup"),
    url(r"^register2/$", views.register2, name = "signup2"),
    url(r"^login/$", views.sign_in, name = "signin"),
    url(r"^logout/$", views.logout_view, name = "logout"),
    url(r"^services/$", views.services, name = "services"),
    url(r"^aboutus/$", views.aboutus, name = "aboutus"),
    url(r"^contactus/$", views.contactus, name = "contactus"),
    path('',views.homepage,name="homepage"),
]
