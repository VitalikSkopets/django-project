from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import *


class VehicleAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Vehicle
        fields = '__all__'


class VehicleAdmin(admin.ModelAdmin):
    form = VehicleAdminForm
    list_display = ('id', 'make', 'model', 'price', 'available', 'in_storage', 'time_create')
    list_display_links = ('id', 'model')
    search_fields = ('make', 'model', 'description')
    list_editable = ('available', 'in_storage')
    list_filter = ('available', 'time_create')
    prepopulated_fields = {"slug": ("make", "model")}


class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Type, TypeAdmin)
admin.site.register(Vehicle, VehicleAdmin)
