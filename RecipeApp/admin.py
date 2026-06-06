from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Recipe, Rating

# -----------------------------
# Category Admin
# -----------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# -----------------------------
# Rating Inline (for Recipe)
# -----------------------------
class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0
    readonly_fields = ('user', 'rating', 'comment', 'created_at')
    can_delete = False


# -----------------------------
# Recipe Admin
# -----------------------------
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'image_tag',          # Thumbnail
        'title',
        'category',
        'user',
        'prep_time',
        'cook_time',
        'total_time',
        'average_rating',
        'ratings_count',
        'created_at',
    )
    list_filter = ('category', 'user', 'created_at')
    search_fields = ('title', 'ingredients', 'instructions')
    readonly_fields = ('average_rating', 'ratings_count', 'total_time', 'created_at', 'image_tag')
    inlines = [RatingInline]
    ordering = ('-created_at',)

    # Thumbnail for recipe image
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover; border-radius:4px;" />', obj.image.url)
        return '-'
    image_tag.short_description = 'Image'

    # Optional: average rating
    def average_rating(self, obj):
        return obj.average_rating()
    average_rating.short_description = 'Avg. Rating'
    average_rating.admin_order_field = 'id'  # workaround for calculated field

    # Ratings count
    def ratings_count(self, obj):
        return obj.ratings_count()
    ratings_count.short_description = 'Ratings Count'


# -----------------------------
# Rating Admin
# -----------------------------
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'rating', 'comment', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('recipe__title', 'user__username', 'comment')
    readonly_fields = ('created_at',)
