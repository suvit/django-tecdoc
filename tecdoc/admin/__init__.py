
from django.contrib import admin

from tecdoc.models import (Manufacturer, Brand, Supplier,
                           CarModel, CarType, Engine,
                           Country,
                           Part,
                           Description, Text)

class TecdocAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    #def has_change_permission(self, request, obj=None):
    #    return not bool(obj)

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        return []

    #def get_readonly_fields(self, request, obj=None):
    #    return [f.name for f in self.model._meta.fields]

admin.site.register(Manufacturer, TecdocAdmin)
admin.site.register(Brand, TecdocAdmin)
admin.site.register(Supplier, TecdocAdmin)

admin.site.register(CarModel, TecdocAdmin)
admin.site.register(CarType, TecdocAdmin)
admin.site.register(Engine, TecdocAdmin)

admin.site.register(Part, TecdocAdmin)

admin.site.register(Country, TecdocAdmin)

admin.site.register(Description, TecdocAdmin)
admin.site.register(Text, TecdocAdmin)