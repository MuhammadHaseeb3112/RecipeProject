from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Avg, Q, F, Count

from .models import Recipe, Rating, Category, Favorite
from .forms import RecipeForm, CustomSignupForm
from django.db.models import Avg, Count, F, FloatField, ExpressionWrapper
from django.utils import timezone
from datetime import timedelta



# ======================
# HOME & STATIC PAGES
# ======================


def home(request):

    # 🆕 Recent Recipes (unchanged)
    recent_recipes = Recipe.objects.order_by('-created_at')[:9]

    # 📊 Annotated data
    recipes = Recipe.objects.annotate(
        avg_rating=Avg('ratings__rating'),
        favorites_count=Count('favorited_by'),
        ratings_count=Count('ratings'),
    )

    # 🧠 SMART SCORE (improved balance)
    recipes = recipes.annotate(
        score=ExpressionWrapper(
            (F('views') * 0.3) +                 # popularity
            (F('favorites_count') * 2) +         # engagement
            (F('ratings_count') * 1.2) +         # activity
            (F('avg_rating') * 5),               # quality
            output_field=FloatField()
        )
    )

    # 🔥 Trending / Popular
    popular_recipes = recipes.order_by('-score')[:9]

    # 🏆 TOP 10 TODAY
    today = timezone.now() - timedelta(days=1)

    top_today = recipes.filter(
        created_at__gte=today
    ).order_by('-score')[:10]

    return render(request, 'index.html', {
        'recent_recipes': recent_recipes,
        'popular_recipes': popular_recipes,
        'top_today': top_today,   # ✅ NEW
    })


def about(request):
    return render(request, 'about.html')


# ======================
# RECIPE VIEWS
# ======================

def recipe_list(request):
    filter_type = request.GET.get("filter")
    query = request.GET.get("q")
    category_id = request.GET.get("category")

    recipes = Recipe.objects.all().select_related("category")

    # Search
    if query:
        recipes = recipes.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query)
        )

    # Category filter
    if category_id:
        recipes = recipes.filter(
            Q(category_id=category_id) |
            Q(category__parent_id=category_id)
        )

    # Filters
    if filter_type == "popular":
        recipes = recipes.annotate(
            avg_rating=Avg("ratings__rating")
        ).filter(avg_rating__gte=4)

    elif filter_type == "recent":
        recipes = recipes.order_by("-created_at")[:20]

    else:
        recipes = recipes.order_by("-created_at")

    categories = Category.objects.filter(
        parent__isnull=True
    ).prefetch_related("children")

    return render(request, "recipes.html", {
        "recipes": recipes,
        "categories": categories,
        "active_category": category_id,
        "active_filter": filter_type,
        "search_query": query,
    })




def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    # 👁 views
    session_key = f"viewed_recipe_{id}"
    if not request.session.get(session_key):
        Recipe.objects.filter(id=id).update(views=F('views') + 1)
        request.session[session_key] = True

    recipe.refresh_from_db()

    # ⭐ rating
    user_rating = None
    is_favorited = False

    if request.user.is_authenticated:
        user_rating = recipe.ratings.filter(user=request.user).first()
        is_favorited = Favorite.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists()

    return render(request, 'recipe_detail.html', {
        'recipe': recipe,
        'user_rating': user_rating,
        'is_favorited': is_favorited   # 🔥 ADD THIS
    })

# ======================
# RATING SYSTEM
# ======================

@login_required
def submit_rating(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    if request.method == "POST":
        score = request.POST.get('score')
        comment = request.POST.get('comment', '').strip()

        # ✅ FIX 1: Handle empty rating
        if not score:
            messages.error(request, "Please select a rating ⭐")
            return redirect('recipe_detail', id=recipe.id)

        try:
            score = int(score)
        except ValueError:
            messages.error(request, "Invalid rating value")
            return redirect('recipe_detail', id=recipe.id)

        # ✅ FIX 2: Validate range
        if not (1 <= score <= 5):
            messages.error(request, "Rating must be between 1 and 5")
            return redirect('recipe_detail', id=recipe.id)

        # ✅ FIX 3: Update or create
        Rating.objects.update_or_create(
            user=request.user,
            recipe=recipe,
            defaults={
                'rating': score,
                'comment': comment
            }
        )

        messages.success(request, "Rating submitted successfully!")

    return redirect('recipe_detail', id=recipe.id)


# ======================
# RECIPE CRUD
# ======================

@login_required
def submit_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            form.save_m2m()

            messages.success(request, "Recipe submitted successfully!")
            return redirect('recipe_detail', id=recipe.id)
    else:
        form = RecipeForm()

    return render(request, 'submit_recipe.html', {'form': form})


@login_required
def edit_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, user=request.user)

    form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("my_recipes")

    return render(request, "edit_recipe.html", {"form": form, "recipe": recipe})


@login_required
def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, user=request.user)

    if request.method == "POST":
        recipe.delete()
        return redirect("my_recipes")

    return render(request, "delete_recipe.html", {"recipe": recipe})


# ======================
# AUTHENTICATION
# ======================

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = CustomSignupForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect('home')

    return render(request, 'accounts/signup.html', {'form': form})


# ======================
# USER PAGES
# ======================

@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(user=request.user)
    return render(request, "my_recipes.html", {"recipes": recipes})



@login_required
def profile(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('recipe')

    return render(request, "profile.html", {
        "favorites": favorites
    })


@login_required
def toggle_favorite(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    fav, created = Favorite.objects.get_or_create(
        user=request.user,
        recipe=recipe
    )

    if not created:
        fav.delete()
        messages.info(request, "Removed from favorites")
    else:
        messages.success(request, "Added to favorites ❤️")

    return redirect('recipe_detail', id=id)