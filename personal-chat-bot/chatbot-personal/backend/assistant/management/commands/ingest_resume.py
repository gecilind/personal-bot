from django.core.management.base import BaseCommand
from assistant.services.ingest_resume import ingest_resume


class Command(BaseCommand):
    help = 'Ingest resume data from resume.txt into the knowledge base'

    def handle(self, *args, **options):
        try:
            ingest_resume()
            self.stdout.write(
                self.style.SUCCESS('Successfully ingested resume data!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error ingesting resume: {str(e)}')
            )

