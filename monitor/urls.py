from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import HomePageView,CameraListView,CameraDetailView,CameraCreateView

camera_patterns = ([
    path('', CameraListView.as_view(), name='cameras'),
    path('camera/<int:pk>/<slug:slug>', CameraDetailView.as_view(), name='camera'),
    path('add-camera/', CameraCreateView.as_view(), name='add-camera'),

], 'camera')