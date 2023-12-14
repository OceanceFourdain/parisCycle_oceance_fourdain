from django.contrib import admin

from .models import Article



class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Id", {"fields": ["id"]}),
        ("Nom de l'article", {"fields": ["titlesArticle"]}),
        ("Contenue de l'article", {"fields": ["descriptionArticle"]}),
        ("Lien pointant vers l'image", {"fields": ["urlImageArticle"]})
    ]
    list_display = ["id", "titlesArticle", "createArticle"]
    
    

admin.site.register(Article, ArticleAdmin)


# Register your models here.
