from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from api.models.user import User
from api.models.loan_application import LoanApplication
from api.models.admin_log import AdminLog

# Customize Admin Site
admin.site.site_header = "Nobus Cloud Administration"
admin.site.site_title = "Nobus Cloud Admin"
admin.site.index_title = "Welcome to Nobus Cloud Dashboard"

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'full_name', 'is_staff', 'is_active', 'created_at']
    search_fields = ['email', 'full_name']
    list_filter = ['is_staff', 'is_active']
    
    # Fieldsets for detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'created_at')}),
    )
    readonly_fields = ['created_at', 'last_login']

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_email', 'amount', 'tenure_months', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__email', 'user__full_name', 'purpose', 'id']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User'

@admin.register(AdminLog)
class AdminLogAdmin(admin.ModelAdmin):
    list_display = ['action', 'admin_email', 'target_model', 'target_id', 'created_at']
    list_filter = ['action', 'target_model', 'created_at']
    search_fields = ['admin__email', 'details', 'target_id']
    ordering = ['-created_at']
    readonly_fields = ['admin', 'action', 'target_id', 'target_model', 'details', 'created_at']
    
    def admin_email(self, obj):
        return obj.admin.email
    admin_email.short_description = 'Admin'
    
    # Disable adding/changing logs manually
    def has_add_permission(self, request):
        return False
        
    def has_change_permission(self, request, obj=None):
        return False
