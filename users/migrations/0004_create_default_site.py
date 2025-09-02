from django.db import migrations
from django.conf import settings

def create_default_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    db_alias = schema_editor.connection.alias
    
    # Get the site ID from settings, default to 1
    site_id = getattr(settings, 'SITE_ID', 1)
    
    # Check if a site with this ID already exists
    if Site.objects.using(db_alias).filter(pk=site_id).exists():
        return

    # Create the default site
    Site.objects.using(db_alias).create(
        pk=site_id,
        domain='example.com',
        name='example.com'
    )

def remove_default_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    db_alias = schema_editor.connection.alias
    site_id = getattr(settings, 'SITE_ID', 1)
    
    # Remove the site if it exists
    Site.objects.using(db_alias).filter(pk=site_id).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_contactform'),
        # Add a dependency on the sites app's initial migration
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_site, remove_default_site),
    ]