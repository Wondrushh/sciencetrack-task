from django.urls import path, include
from rest_framework.routers import DefaultRouter 

from library import views

router = DefaultRouter()
router.register("authors", views.AuthorViewSet)
router.register("books", views.BookViewSet)

urlpatterns = [
    # path("", views.index, name="index"),
    path('', include(router.urls)),
]
