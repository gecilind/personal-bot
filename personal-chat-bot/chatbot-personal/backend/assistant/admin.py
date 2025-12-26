from django.contrib import admin
from .models import AssistantMemory


@admin.register(AssistantMemory)
class AssistantMemoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'content_preview', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('content',)
    readonly_fields = ('created_at',)
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'

