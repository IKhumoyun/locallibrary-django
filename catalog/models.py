from django.db import models

class Genre(models.Model):
    """Modeal representing a book genre"""

    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representating the Model object."""
        return self.name

class Language(models.Model):
    """Model representing a book language"""
    name = models.CharField(max_length=100, help_text='Enter a book language')

    def __str__(self):
        """String for reprsentating the Model object."""
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')

    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, help_text='Select a language for this book')

    def display_genre(self):
        """Create a string for Genre. This is required to display genre in admin"""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'

    def __str__(self):
        """String for representating the Model object."""
        return self.title

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('book-detail', args=[str(self.id)])

import uuid #required for unique book instances

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')

    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.DateField(null=True, blank=True)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book Availabilty'
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String representating the Model object."""
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    """Model representating the author."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death=models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('author_detail', args=[str(self.id)])

    def __str__(self):
        """String for representatingthe Model object."""
        return f'{self.last_name}, {self.first_name}'

