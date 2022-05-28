from django.core.management.base import BaseCommand, CommandError
from off.fetcher import ApiConsulter


class Command(BaseCommand):
    help ="Fetch data from OpenFoodfacts and fill database"
    consulter = ApiConsulter()
    
    def handle(self, *args, **kwargs):
        try:
            self.stdout.write("Fetching data on OpenFoodfacts...")
            self.consulter.db_save()
        except:
            raise CommandError('Fetching data on OpenFoodfacts is not possible for now.')
        
        self.stdout.write(self.style.SUCCESS('Successfully fetched data'))
