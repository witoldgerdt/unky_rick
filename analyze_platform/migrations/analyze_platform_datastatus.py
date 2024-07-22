from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        # Define any dependencies here if applicable
    ]

    operations = [
        migrations.CreateModel(
            name='DataStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'analyze_platform_datastatus',
            },
        ),
    ]
