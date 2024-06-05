from string import Template

TITLE_PROMPT = Template(
    """
    Create a title for a puzzle game related to '$topic'.
    Only mention the title (without quotations) in your reponse.
    """
)
SOLUTION_PROMPT = Template(
    """
    Create a word of between 8 and 10 characters related to '$topic' for a puzzle game.
    Only mention the word in your reponse.
    """
)
WORDS_PROMPT = Template(
    """
    For each subsequent character in the word '$solution' generate 10 single words related
    to '$topic' that contains that character.
    Return your response as a JSON string array containing all the words in a single list.
    """
)
CLUES_PROMPT = Template(
    """Generate a clue for each word in the list $words, for a puzzle game.
    Return your response as a JSON string array containing all the clues in a single, ordered list.
    Each clue should only be the actual clue text.
    """
)
