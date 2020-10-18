from django.contrib import admin

from cage.models import Detention, Inmate, Imprisonment, List, ListItem, Prison


admin.site.register(ListItem, admin.ModelAdmin)
admin.site.register(List, admin.ModelAdmin)
admin.site.register(Prison, admin.ModelAdmin)
admin.site.register(Detention, admin.ModelAdmin)
admin.site.register(Inmate, admin.ModelAdmin)
admin.site.register(Imprisonment, admin.ModelAdmin)
