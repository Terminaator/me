from django.conf.urls import url
from django.urls import path, include
from django.views.generic import TemplateView
import views.client.clientQuestionView


urlpatterns = [
    path('api/question', views.client.clientQuestionView.ClientQuestionView.as_view()),
    url(r'^$', TemplateView.as_view(template_name="main.html")),
]
