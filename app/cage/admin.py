from cage.models import Detention, Imprisonment, Inmate, List, ListItem, Prison
from django.contrib import admin

admin.site.register(ListItem, admin.ModelAdmin)
admin.site.register(List, admin.ModelAdmin)
admin.site.register(Prison, admin.ModelAdmin)
admin.site.register(Detention, admin.ModelAdmin)
admin.site.register(Inmate, admin.ModelAdmin)
admin.site.register(Imprisonment, admin.ModelAdmin)
