from django.urls import path

from backend.meals.views import (
    root_view, nora_view,
    menu_detail_view,
    menu_create_view,
    menu_update_view,
    menu_delete_view,
    plate_create_view,
    plate_update_view,
    plate_delete_view,
    menu_preference_view,
    send_reminder_view,
)

app_name = 'meals'

# Main entrypoint

urlpatterns = [
    path('', view=root_view, name='root-router'),
]

# Nora views

urlpatterns += [
    path('nora/', view=nora_view, name='nora-view'),
    path('nora/menu/create/',
         view=menu_create_view, name='menu-create'),
    path('nora/menu/<uuid:pk>/',
         view=menu_update_view, name='menu-update'),
    path('nora/menu/<uuid:pk>/delete/',
         view=menu_delete_view, name='menu-delete'),
    path('nora/plate/create/',
         view=plate_create_view, name='plate-create'),
    path('nora/plate/<uuid:pk>/',
         view=plate_update_view, name='plate-update'),
    path('nora/plate/<uuid:pk>/delete/',
         view=plate_delete_view, name='plate-delete'),
    path('nora/send-reminder/',
         view=send_reminder_view, name='send-reminder')
]

# Employee views

urlpatterns += [
    path('menu/<uuid:pk>/preference/',
         view=menu_preference_view, name='menu-preference')
]

# Public today's menu view

urlpatterns += [
    path('menu/<uuid:pk>/', view=menu_detail_view, name='menu-detail')
]
