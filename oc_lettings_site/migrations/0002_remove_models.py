from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lettings', '0002_copy_data'),
        ('profiles', '0002_copy_data'),
        ('oc_lettings_site', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(name='Letting'),
                migrations.DeleteModel(name='Address'),
                migrations.DeleteModel(name='Profile'),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql="DROP TABLE IF EXISTS oc_lettings_site_letting;",
                    reverse_sql=migrations.RunSQL.noop,
                ),
                migrations.RunSQL(
                    sql="DROP TABLE IF EXISTS oc_lettings_site_address;",
                    reverse_sql=migrations.RunSQL.noop,
                ),
                migrations.RunSQL(
                    sql="DROP TABLE IF EXISTS oc_lettings_site_profile;",
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
        ),
    ]