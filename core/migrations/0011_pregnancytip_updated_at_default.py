from django.db import migrations, models
import django.utils.timezone

def set_updated_at_default(apps, schema_editor):
    PregnancyTip = apps.get_model('core', 'PregnancyTip')
    for tip in PregnancyTip.objects.filter(updated_at__isnull=True):
        tip.updated_at = django.utils.timezone.now()
        tip.save()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0010_fix_pregnancytip_schema'),
    ]

    operations = [
        migrations.RunPython(set_updated_at_default, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='pregnancytip',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ] 