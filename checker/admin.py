from django.contrib import admin
from .models import Domain, Source

class DomainAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'expiration_date', 'display_sources']

    def display_sources(self, obj):
        return ', '.join(x.name for x in obj.sources.all())

admin.site.register(Domain, DomainAdmin)
admin.site.register(Source)
