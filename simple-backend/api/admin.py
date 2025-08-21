from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from django.utils.html import format_html, format_html_join
from guardian.shortcuts import get_users_with_perms, get_groups_with_perms

from resolwe.flow.models import Collection, Data, Process, DescriptorSchema

# --- Extra display helpers ---
def current_user_perms(obj):
    users = get_users_with_perms(obj, attach_perms=True, with_superusers=False)
    rows = [(f"{u.username}", ", ".join(sorted(perms))) for u, perms in users.items()]
    if not rows:
        return "(none)"
    return format_html("<ul>{}</ul>", format_html_join("", "<li><b>{}</b>: {}</li>", rows))
current_user_perms.short_description = "Current user permissions"

def current_group_perms(obj):
    groups = get_groups_with_perms(obj, attach_perms=True)
    rows = [(g.name, ", ".join(sorted(perms))) for g, perms in groups.items()]
    if not rows:
        return "(none)"
    return format_html("<ul>{}</ul>", format_html_join("", "<li><b>{}</b>: {}</li>", rows))
current_group_perms.short_description = "Current group permissions"

# --- Base admin with permissions ---
class BasePermAdmin(GuardedModelAdmin):
    readonly_fields = ("created", "modified", current_user_perms, current_group_perms)
    search_fields = ("name",)
    list_per_page = 25

@admin.register(Collection)
class CollectionAdmin(BasePermAdmin):
    list_display = ("id", "name", "contributor", "created", "modified")

@admin.register(Data)
class DataAdmin(BasePermAdmin):
    list_display = ("id", "name", "status", "contributor", "created")

@admin.register(Process)
class ProcessAdmin(BasePermAdmin):
    list_display = ("id", "slug", "name", "version", "type")

@admin.register(DescriptorSchema)
class DescriptorSchemaAdmin(BasePermAdmin):
    list_display = ("id", "slug", "name", "version")
