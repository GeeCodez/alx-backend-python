import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # Filter messages by sender ID
    sender = django_filters.NumberFilter(field_name="sender__id")

    # Filter messages by conversation ID
    conversation = django_filters.NumberFilter(field_name="conversation__id")

    # Filter messages within a date/time range
    start_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'start_date', 'end_date']
