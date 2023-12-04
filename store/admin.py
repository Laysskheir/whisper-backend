from django.contrib import admin
from .models import *
from django.utils.html import format_html


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ["title", "slider_image", "is_active"]
    list_filter = ["is_active"]

    def slider_image(self, obj):
        return format_html('<img src="{}" width="100" height="50" />', obj.image.url)

    slider_image.short_description = "Slider"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "image_category"]
    prepopulated_fields = {"slug": ("name",)}

    def image_category(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.image.url)

    image_category.short_description = "Image"


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ["name", "color_preview"]

    def color_preview(self, obj):
        return format_html(
            '<div style="width: 30px; height: 30px; border-radius: 50%; background-color: {};"></div>',
            obj.name,
        )

    color_preview.short_description = "Color Preview"


class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1  # The number of empty image fields to display


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "show_colors",
        "show_sizes",
        "brand",
        "price",
        "feature",
        "display_image",
    ]
    list_filter = ["category", "brand"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImagesInline]

    def display_image(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.image.url)

    display_image.short_description = "Image"

    def show_colors(self, obj):
        colors = obj.colors.all()
        # Generate color  previews
        color_info = [
            f'<div style="display: inline-block; margin-right: 5px; width: 30px; height: 30px; border-radius: 50%; background-color: {color.name};"></div> '
            for color in colors
        ]
        return format_html(" ".join(color_info))
    show_colors.short_description = "Colors"

    def show_sizes(self, obj):
        sizes = obj.sizes.all()
        size_names = "/ ".join(str(size) for size in sizes)
        return size_names

    show_sizes.short_description = "Sizes"
