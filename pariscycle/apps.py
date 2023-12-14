from django.apps import AppConfig

class ParisCycleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pariscycle'
    
class MapsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maps'
    
class ParisDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'parisdata'