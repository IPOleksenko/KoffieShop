from django.contrib import admin
from django.contrib import messages
from django.db.models import Case, When, IntegerField
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    # Add a filter by status
    list_filter = ('status',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Annotate orders with an additional field for sorting:
        # if status is 'completed' - value 1, for all others - 0.
        qs = qs.annotate(
            status_order=Case(
                When(status='completed', then=1),
                default=0,
                output_field=IntegerField(),
            )
        )
        # Sort first by the annotation, then by status (if annotation values are equal)
        return qs.order_by('status_order', 'status')

    def has_add_permission(self, request):
        # Disable adding new orders through the admin interface
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:  # When editing an existing order
            # Make all fields, except 'status', read-only
            return [field.name for field in self.model._meta.fields if field.name != 'status']
        return []

    def save_model(self, request, obj, form, change):
        if change:
            changed_fields = form.changed_data
            non_status_changes = [f for f in changed_fields if f != 'status']
            if non_status_changes:
                self.message_user(
                    request,
                    "Warning: Changing fields other than 'status' is not allowed.",
                    level=messages.WARNING
                )
        super().save_model(request, obj, form, change)

admin.site.register(Order, OrderAdmin)
