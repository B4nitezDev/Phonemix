from phonemizer import phonemize
from config.config import phonemize_config

def get_phonemes(text, language=phonemize_config['default_language'], backend=phonemize_config['backend']):
    """ Convert text to phonemes using the specified backend and language.
        language: 'es', 'en'
    """
    return phonemize(text, language=language, backend=backend)

def print_phonemes_with_indices(phonemes):
    """ Create a formatted string of phonemes with their corresponding indices. """
    return ' '.join(f"{index}: '{phoneme}'" for index, phoneme in enumerate(phonemes))

def levenshtein_detailed(s1, s2):
    """ Calculate detailed Levenshtein operations needed to convert s1 to s2. """
    dp = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
    for i in range(len(s1) + 1):
        dp[i][0] = i
    for j in range(len(s2) + 1):
        dp[0][j] = j

    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + 1)

    operations = []
    i, j = len(s1), len(s2)
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            i, j = i - 1, j - 1
        elif dp[i][j] == dp[i - 1][j - 1] + 1:
            operations.append(f"Sustituir '{s1[i - 1]}' por '{s2[j - 1]}' en la posición {i - 1}")
            i, j = i - 1, j - 1
        elif dp[i][j] == dp[i - 1][j] + 1:
            operations.append(f"Eliminar '{s1[i - 1]}' de la posición {i - 1}")
            i -= 1
        else:
            operations.append(f"Insertar '{s2[j - 1]}' en la posición {j - 1}")
            j -= 1

    while i > 0:
        operations.append(f"Eliminar '{s1[i - 1]}' de la posición {i - 1}")
        i -= 1
    while j > 0:
        operations.append(f"Insertar '{s2[j - 1]}' en la posición {j - 1}")
        j -= 1

    return operations[::-1]
