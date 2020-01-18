"""QAsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('',include('QAapp.urls')),
    path('admin/', admin.site.urls),
    path('welcome', views.index),
    path('question/<int:qid>/<slug:qslug>',  views.viewquestion),
    path('ask_question',  views.askquestion),
    path('ajax-answer-question',  views.ajaxanswerquestion),
    path('user_profile',  views.user_profile),
    path('contact_us',  views.contact),
    path('user_questions',  views.user_questions),
    path('user_answers',  views.user_answers),
    path('user_points',  views.user_points),
]

#urlpatterns = urlpatterns + staticfiles_urlpatterns()
