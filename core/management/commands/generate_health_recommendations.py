from django.core.management.base import BaseCommand
from core.models import CheckupProgress
from core.views import generate_health_recommendations

class Command(BaseCommand):
    help = 'Generate health recommendations for all existing checkups'

    def add_arguments(self, parser):
        parser.add_argument(
            '--checkup-id',
            type=int,
            help='Generate recommendations for a specific checkup ID only',
        )

    def handle(self, *args, **options):
        if options['checkup_id']:
            try:
                checkup = CheckupProgress.objects.get(id=options['checkup_id'])
                recommendations = generate_health_recommendations(checkup)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully generated {len(recommendations)} recommendations for checkup ID {checkup.id}'
                    )
                )
            except CheckupProgress.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Checkup with ID {options["checkup_id"]} does not exist')
                )
        else:
            checkups = CheckupProgress.objects.all()
            total_checkups = checkups.count()
            
            self.stdout.write(f'Generating recommendations for {total_checkups} checkups...')
            
            generated_count = 0
            for checkup in checkups:
                try:
                    recommendations = generate_health_recommendations(checkup)
                    generated_count += len(recommendations)
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error generating recommendations for checkup ID {checkup.id}: {str(e)}')
                    )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully generated {generated_count} recommendations for {total_checkups} checkups'
                )
            )