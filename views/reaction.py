from models.reaction import get_all_reactions

def handle_get_all_reactions():
    reactions = get_all_reactions()
    return (200, reactions)