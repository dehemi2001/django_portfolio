from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    UserProfile,
    Experience,
    Skill,
    Tool,
    Technology,
    Project,
    ProjectTechnology,
    Contact
)

# Register your models here.

# --- Inlines ---

# Inline for UserProfile to be attached to the main User admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# Inline for Project to manage its technologies
class ProjectTechnologyInline(admin.StackedInline):
    model = ProjectTechnology
    extra = 1
    ordering = ['order']
    autocomplete_fields = ['technology']

# --- ModelAdmins ---

# Custom User admin to include the UserProfile
class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__username',)

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'user_profile', 'order')
    list_editable = ('order',)
    list_filter = ('user_profile',)
    search_fields = ('name', 'company', 'user_profile__user__username')
    autocomplete_fields = ('user_profile',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'user_profile', 'order')
    list_editable = ('order',)
    list_filter = ('user_profile',)
    search_fields = ('name', 'user_profile__user__username')
    autocomplete_fields = ('user_profile',)

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_profile', 'order')
    list_editable = ('order',)
    list_filter = ('user_profile',)
    search_fields = ('name', 'user_profile__user__username')
    autocomplete_fields = ('user_profile',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_profile', 'order')
    list_editable = ('order',)
    inlines = [ProjectTechnologyInline]

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    readonly_fields = ('user_profile', 'name', 'email', 'subject', 'message', 'created_at')

# Re-register User model with our custom admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
