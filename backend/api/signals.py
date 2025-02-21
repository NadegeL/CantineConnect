from django.dispatch import receiver
from django.db.models.signals import post_save, post_migrate


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    from django.contrib.auth.models import Group
    groups = ['Administrateur du TDB de Django',
              'Administration du Site', 'Parents']
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)


@receiver(post_save, sender='api.User')
def add_user_to_group(sender, instance, created, **kwargs):
    from django.contrib.auth.models import Group
    if created:
        try:
            if instance.user_type == 'django_admin':
                group_name = 'Administrateur du TDB de Django'
                instance.is_superuser = True
                instance.is_staff = True
            elif instance.user_type == 'school_admin':
                group_name = 'Administration du Site'
                instance.is_staff = True
            else:
                group_name = 'Parents'

            group = Group.objects.get(name=group_name)
            instance.groups.add(group)
            instance.save()
        except Group.DoesNotExist:
            pass
