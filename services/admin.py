from django.contrib import admin

# Register your models here.


from .models import Service, Variation, ServiceImage, Category, ServiceFeatured

class ServiceImageInline(admin.TabularInline):
	model = ServiceImage
	extra = 0
	max_num = 10

class VariationInline(admin.TabularInline):
	model = Variation
	extra = 0
	max_num = 10


class ServiceAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'price']
	inlines = [
		ServiceImageInline,
		VariationInline,
	]
	class Meta:
		model = Service

admin.site.register(Service, ServiceAdmin)



#admin.site.register(Variation)

admin.site.register(ServiceImage)

admin.site.register(Category)

admin.site.register(ServiceFeatured)