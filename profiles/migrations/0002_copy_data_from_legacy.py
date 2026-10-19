from django.db import migrations


def copy_data(apps, schema_editor):
    OldProfile = apps.get_model('oc_lettings_site', 'Profile')
    NewProfile = apps.get_model('profiles', 'Profile')

    for old in OldProfile.objects.all():
        NewProfile.objects.create(
            id=old.id,
            user_id=old.user_id,
            favorite_city=old.favorite_city,
        )


def reverse_copy(apps, schema_editor):
    apps.get_model('profiles', 'Profile').objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('oc_lettings_site', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_data, reverse_copy),
    ]