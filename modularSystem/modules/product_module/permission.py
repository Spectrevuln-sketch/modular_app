from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Product

def setup_permissions():
    try:
        content_type = ContentType.objects.get_for_model(Product)
        manager_group, _ = Group.objects.get_or_create(name='manager')
        user_group, _ = Group.objects.get_or_create(name='user')
        public_group, _ = Group.objects.get_or_create(name='public')
    except Exeption as e:
        print(f"Error setting permission in product module: \n {e}")
    manager_perms = [
        Permission.objects.get_or_create(
            codename=f'{action}_product',
            content_type=content_type,
            defaults={'name': f'Can {action} product'}
        )[0]
        for action in ['add', 'change', 'delete', 'view']
    ]

    user_perms = [
        Permission.objects.get_or_create(
            codename=f'{action}_product',
            content_type=content_type,
            defaults={'name': f'Can {action} product'}
        )[0]
        for action in ['add', 'change', 'view']
    ]

    public_perms = [
        Permission.objects.get_or_create(
            codename='view_product',
            content_type=content_type,
            defaults={'name': 'Can view product'}
        )[0]
    ]

    manager_group.permissions.set(manager_perms)
    user_group.permissions.set(user_perms)
    public_group.permissions.set(public_perms)

setup_permissions()