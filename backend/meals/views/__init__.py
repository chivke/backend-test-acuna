from .common import root_view

from .nora import (
    nora_view,
    menu_create_view,
    menu_update_view,
    menu_delete_view,
    plate_create_view,
    plate_update_view,
    plate_delete_view,
    send_reminder_view,
)

from .employee import menu_preference_view, menu_detail_view

__all__ = [
    'root_view',
    'nora_view',
    'menu_create_view',
    'menu_update_view',
    'menu_delete_view',
    'plate_create_view',
    'plate_update_view',
    'plate_delete_view',
    'menu_detail_view',
    'menu_preference_view',
    'send_reminder_view',
]
