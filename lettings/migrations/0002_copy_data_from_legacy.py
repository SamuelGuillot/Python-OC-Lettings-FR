from django.db import migrations


def copy_data(apps, schema_editor):
    OldAddress = apps.get_model('oc_lettings_site', 'Address')
    OldLetting = apps.get_model('oc_lettings_site', 'Letting')
    NewAddress = apps.get_model('lettings', 'Address')
    NewLetting = apps.get_model('lettings', 'Letting')

    for old in OldAddress.objects.all():
        NewAddress.objects.create(
            id=old.id,
            number=old.number,
            street=old.street,
            city=old.city,
            state=old.state,
            zip_code=old.zip_code,
            country_iso_code=old.country_iso_code,
        )

    for old in OldLetting.objects.all():
        NewLetting.objects.create(
            id=old.id,
            title=old.title,
            address_id=old.address_id,
        )


def reverse_copy(apps, schema_editor):
    apps.get_model('lettings', 'Letting').objects.all().delete()
    apps.get_model('lettings', 'Address').objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('lettings', '0001_initial'),
        ('oc_lettings_site', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_data, reverse_copy),
    ]