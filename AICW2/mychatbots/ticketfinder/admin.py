from django.contrib import admin

# Register your models here.
from .models import TrainStation, TrainFare, UserQuery

admin.site.register(TrainStation)
admin.site.register(TrainFare)
admin.site.register(UserQuery)
class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('query_text', 'timestamp', 'processed')