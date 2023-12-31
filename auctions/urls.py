from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("additem", views.additem, name="additem"),
    path("item/<uuid:item_id>", views.item_detail, name="item"),
    path("bid/<uuid:item_id>", views.bid, name="bid")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
