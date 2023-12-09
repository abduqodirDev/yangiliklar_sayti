from modeltranslation.translator import register, TranslationOptions
from .models import News, Category

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields=('title', 'body')
    
@register(Category)
class NewsTranslationOptions(TranslationOptions):
    fields=('name',)