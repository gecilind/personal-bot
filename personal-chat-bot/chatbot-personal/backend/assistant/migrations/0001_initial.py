# Generated migration - TEMPORARY VERSION WITHOUT pgvector
# This allows the app to work without pgvector installed
# Later, we'll add a migration to convert to vector field when pgvector is ready
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssistantMemory',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('content', models.TextField()),
                ('embedding', models.TextField(blank=True, null=True)),  # Temporary: store as JSON text
                ('type', models.CharField(choices=[('knowledge', 'Knowledge'), ('memory', 'Memory')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'assistant_memory',
                'ordering': ['-created_at'],
            },
        ),
    ]

