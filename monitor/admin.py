from django.contrib import admin

# Register your models here.
from .models import Camera
# Register your models here.

class cameraAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)



admin.site.register(Camera,cameraAdmin)
