from django.contrib import admin
from .models import Paragraph, TypingResult

# Register your models here.

@admin.register(Paragraph)
class ParagraphAdmin(admin.ModelAdmin): # Custom admin interface for the Paragraph model 
    list_display = ('id', 'difficulty') # Display the id and difficulty in the admin panel instead of name
    list_filter = ('difficulty',) # Add a filter for difficulty in the admin panel to easily find paragraphs by their difficulty level 

@admin.register(TypingResult)
class TypingResultAdmin(admin.ModelAdmin): # Custom admin interface for the TypingResult model
    list_display = ('user', 'wpm')
    list_filter = ('difficulty',)