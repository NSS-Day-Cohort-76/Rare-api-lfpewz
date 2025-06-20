from models.category import get_all_categories

def handle_get_all_categories():
    categories = get_all_categories()
    return (200, categories)