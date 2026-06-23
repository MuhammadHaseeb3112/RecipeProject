from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db.models import Avg
from django.utils import timezone   # ✅ ADD THIS IMPORT



# =========================
# CATEGORY MODEL
# =========================
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["parent__id", "name"]

    def __str__(self):
        full_path = [self.name]
        parent = self.parent
        while parent is not None:
            full_path.append(parent.name)
            parent = parent.parent
        return " → ".join(full_path[::-1])


# =========================
# RECIPE MODEL
# =========================
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=300)
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)

    prep_time = models.IntegerField(help_text="Preparation time in minutes")
    cook_time = models.IntegerField(
        null=True,
        blank=True,
        help_text="Cooking time in minutes"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    ingredients = models.TextField(
        help_text="Enter ingredients separated by commas or line breaks"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recipes'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recipes'
    )

    views = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['-views']),
        ]

    @property
    def total_time(self):
        prep = self.prep_time or 0
        cook = self.cook_time or 0
        return prep + cook

    def __str__(self):
        return f"{self.title} ({self.category})" if self.category else self.title

    # ⭐ OPTIMIZED RATING
    def average_rating(self):
        return self.ratings.aggregate(avg=Avg('rating'))['avg'] or 0

    def ratings_count(self):
        return self.ratings.count()

    # ❤️ FAVORITES
    def favorites_count(self):
        return self.favorited_by.count()

    def is_favorited_by(self, user):
        if user.is_authenticated:
            return self.favorited_by.filter(user=user).exists()
        return False

    # =========================
    # 🧠 AI SCORE SYSTEM
    # =========================
    def ai_score(self):
        avg_rating = self.average_rating() or 0
        favorites = self.favorites_count()
        views = self.views

        # 🔥 Recency boost (last 3 days)
        days_old = (timezone.now() - self.created_at).days
        recency_boost = max(0, 3 - days_old)

        score = (
            (views * 0.3) +
            (favorites * 2) +
            (avg_rating * 10) +
            (recency_boost * 5)
        )

        return round(score, 2)

# =========================
# RATING MODEL
# =========================
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ratings',
        db_index=True
    )

    rating = models.PositiveIntegerField(
        default=1,
        validators=[MaxValueValidator(5)]
    )

    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} rated {self.recipe.title}: {self.rating}"


# =========================
# FAVORITE MODEL
# =========================
class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'   # ✅ ADDED
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} ❤️ {self.recipe.title}"