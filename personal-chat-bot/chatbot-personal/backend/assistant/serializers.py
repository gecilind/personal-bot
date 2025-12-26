from rest_framework import serializers
from assistant.models import AssistantMemory


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(required=True, max_length=2000)


class ChatResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
    relevant_knowledge = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )


class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistantMemory
        fields = ['id', 'content', 'type', 'created_at']
        read_only_fields = ['id', 'created_at']

