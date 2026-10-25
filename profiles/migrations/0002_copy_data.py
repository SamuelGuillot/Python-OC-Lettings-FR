from django.db import migrations


BATCH_SIZE = 500


def copy_data(apps, schema_editor):
    OldProfile = apps.get_model('oc_lettings_site', 'Profile')
    NewProfile = apps.get_model('profiles', 'Profile')

    buffer = []
    for old in OldProfile.objects.iterator(chunk_size=BATCH_SIZE):
        buffer.append(NewProfile(
            id=old.id,
            user_id=old.user_id,
            favorite_city=old.favorite_city,
        ))
        if len(buffer) >= BATCH_SIZE:
            NewProfile.objects.bulk_create(
                buffer, batch_size=BATCH_SIZE, ignore_conflicts=True,
            )
            buffer.clear()
    if buffer:
        NewProfile.objects.bulk_create(
            buffer, batch_size=BATCH_SIZE, ignore_conflicts=True,
        )


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('profiles', '0001_initial'),
        ('oc_lettings_site', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_data, migrations.RunPython.noop),
    ]