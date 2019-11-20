from django.contrib import admin

from .models import Author, Genre, Book, BookInstance, Language

admin.site.register(Genre)
admin.site.register(Language)

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

#admin.site.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    #list_filter = ('title', 'author', 'display_genre')
    inlines=[BooksInstanceInline]

#admin.site.register(Author)
class BookInline(admin.TabularInline):
    model = Book
    extra = 0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines=[BookInline]

#admin.site.register(BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        ('General info', {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availabilty', {
            'fields': ('status', 'due_back')
        }),
    )