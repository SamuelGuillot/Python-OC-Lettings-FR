from django.db import migrations



BATCH_SIZE = 500


def copy_data(apps, schema_editor):
    OldAddress = apps.get_model('oc_lettings_site', 'Address')
    OldLetting = apps.get_model('oc_lettings_site', 'Letting')
    NewAddress = apps.get_model('lettings', 'Address')
    NewLetting = apps.get_model('lettings', 'Letting')

    buffer = []
    for old in OldAddress.objects.iterator(chunk_size=BATCH_SIZE):
        buffer.append(NewAddress(
            id=old.id,
            number=old.number,
            street=old.street,
            city=old.city,
            state=old.state,
            zip_code=old.zip_code,
            country_iso_code=old.country_iso_code,
        ))
        if len(buffer) >= BATCH_SIZE:
            NewAddress.objects.bulk_create(
                buffer, batch_size=BATCH_SIZE, ignore_conflicts=True,
            )
            buffer.clear()
    if buffer:
        NewAddress.objects.bulk_create(
            buffer, batch_size=BATCH_SIZE, ignore_conflicts=True,
        )
        buffer.clear()

    for old in OldLetting.objects.iterator(chunk_size=BATCH_SIZE):
        buffer.append(NewLetting(
            id=old.id,
            title=old.title,
            address_id=old.address_id,
        ))
        if len(buffer) >= BATCH_SIZE:
            NewLetting.objects.bulk_create(
                buffer, batch_size=BATCH_SIZE, ignore_conflicts=True,
            )
            buffer.clear()
    if buffer:
        NewLetting.objects.bulk_create(
            buffer, batch_size=BATCH_SIZE, ignore_conflicts=True,
        )


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('lettings', '0001_initial'),
        ('oc_lettings_site', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_data, migrations.RunPython.noop),
    ]