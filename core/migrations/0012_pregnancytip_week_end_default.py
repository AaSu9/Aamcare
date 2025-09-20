from django.db import migrations, models

def set_week_end_default(apps, schema_editor):
    PregnancyTip = apps.get_model('core', 'PregnancyTip')
    for tip in PregnancyTip.objects.filter(week_end__isnull=True):
        tip.week_end = 1
        tip.save()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0011_pregnancytip_updated_at_default'),
    ]

    operations = [
        migrations.RunPython(set_week_end_default, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='pregnancytip',
            name='week_end',
            field=models.IntegerField(help_text='Ending week of pregnancy', default=1),
        ),
    ] 