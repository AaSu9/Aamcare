def language_processor(request):
    """
    Add current language to template context
    """
    language = request.session.get('django_language', 'en')
    return {'language': language} 