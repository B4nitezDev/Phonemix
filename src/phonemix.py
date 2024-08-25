from src.phonemize.analyzer import levenshtein_detailed, print_phonemes_with_indices


def provide_detailed_feedback(user_phonemes, correct_phonemes):
    """ Generate detailed feedback for phoneme corrections. """
    operations = levenshtein_detailed(user_phonemes, correct_phonemes)
    user_phonemes_indices = print_phonemes_with_indices(user_phonemes)
    correct_phonemes_indices = print_phonemes_with_indices(correct_phonemes)
    feedback_lines = [
        "Fonemas transcritos: " + user_phonemes_indices,
        "Fonemas correctos: " + correct_phonemes_indices,
        "\nOperaciones necesarias:\n" + "\n".join(operations) if operations else "No se requieren cambios, la pronunciación es correcta."
    ]
    return "\n".join(feedback_lines)