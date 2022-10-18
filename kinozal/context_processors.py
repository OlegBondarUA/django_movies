from .selectors import categories_selector


def categories_menu(request):
    return {
        'search_categories': categories_selector()
    }
