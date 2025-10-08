from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Count, Q
from .models import ASMTask
from zonemanager.models import ZoneManager
from django.contrib.auth.models import User

@admin.register(ASMTask)
class ASMTaskAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'zone_manager', 'asm', 'category', 'status', 
        'start_date', 'end_date', 'action_buttons'
    )
    list_filter = ('status', 'category', 'zone_manager')
    search_fields = ('title', 'asm__user__username', 'zone_manager__user__username', 'category__name')
    ordering = ('-start_date',)
    
    # Use custom change list template to add Task Board button
    change_list_template = "admin/tasks/asmtask_change_list.html"

    # Edit / Delete buttons per row
    def action_buttons(self, obj):
        return format_html(
            '<a class="button" style="background-color:#28a745;color:white;padding:2px 6px;border-radius:4px;text-decoration:none;" href="{}">Edit</a>&nbsp;'
            '<a class="button" style="background-color:#dc3545;color:white;padding:2px 6px;border-radius:4px;text-decoration:none;" href="{}" onclick="return confirm(\'Are you sure?\')">Delete</a>',
            f'/admin/tasks/asmtask/{obj.id}/change/',
            f'/admin/tasks/asmtask/{obj.id}/delete/',
        )
    action_buttons.short_description = 'Actions'

    # Custom URL for Task Board
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.task_dashboard_view), name='task-dashboard'),
        ]
        return custom_urls + urls

    # Task Board view
     # Dashboard view
    def task_dashboard_view(self, request):
        """Task Board with filters and glossy design"""
        # Date range filter
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        try:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else timezone.now().date()
        except:
            start_date = timezone.now().date()
        try:
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else start_date
        except:
            end_date = start_date

        # ASM & ZM filters
        asm_id = request.GET.get('asm')
        zm_id = request.GET.get('zone_manager')

        tasks = ASMTask.objects.filter(is_deleted=False, start_date__gte=start_date, start_date__lte=end_date)
        if asm_id:
            tasks = tasks.filter(asm__id=asm_id)
        if zm_id:
            tasks = tasks.filter(zone_manager__id=zm_id)

        status_columns = ['pending','in_progress','completed','cancelled','hold']

        # For dropdowns
        asms = User.objects.filter(groups__name='Area Sales Manager')
        zms = ZoneManager.objects.all()

        context = dict(
            self.admin_site.each_context(request),
            tasks=tasks,
            status_columns=status_columns,
            start_date=start_date,
            end_date=end_date,
            selected_asm=int(asm_id) if asm_id else '',
            selected_zm=int(zm_id) if zm_id else '',
            asms=asms,
            zms=zms,
        )
        return render(request, "admin/tasks/task_board.html", context)