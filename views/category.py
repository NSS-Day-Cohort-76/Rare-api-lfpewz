from models.category import get_all_categories, create_category, delete_category, update_category

def handle_get_all_categories():
    categories = get_all_categories()
    return (200, categories)

def handle_create_category(new_category):
    status, created_category = create_category(new_category)
    return status, created_category

def handle_delete_category(category_id):
    delete_category(category_id)
    return (204, "")

def handle_update_category(category_id, data):
    if "label" not in data or not data["label"]:
        return (400, {"error": "Category label is required"})
    label = data["label"]
    success = update_category(label, category_id)

    if success:
        return (204, {})  # No Content
    else:
        return (404, {"error": "Category not found"})

