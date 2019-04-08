from django.contrib import admin

from professor.models import Ementa, QuestaoStatus, AlgoritmoStatus

class EmentaAdmin(admin.ModelAdmin):
    list_display=('conhecimento','texto',)
admin.site.register(Ementa,EmentaAdmin)

class QuestaoStatusAdmin(admin.ModelAdmin):
    list_display=('aplicada','iniciou','tempo','tentativa','ativo')
admin.site.register(QuestaoStatus,QuestaoStatusAdmin)

class AlgoritmoStatusAdmin(admin.ModelAdmin):
    list_display=('aplicado','iniciou','tempo','ativo')
admin.site.register(AlgoritmoStatus,AlgoritmoStatusAdmin)
