const languages = [
    {key: "en-us", value: "ingles americano"},
    {key: "en-gb", value:"ingles britanico"},
    {key: "fr-fr", value: "frances"},
    {key: "it", value: "italiano"},
    {key: "de", value: "aleman"},
    {key: "pt-pt", value: "portugues de portugal"},
    {key: "pt-br", value: "portugues de brasil"},
    {key: "es", value: "español de españa"},
    {key: "es-la", value: "español de latinoamerica"}
]

export function languageValidate(input, output) {
    const isValidLanguageInput = languages.some(language => language.key === input);
    const isValidLanguageOutput = languages.some(language => language.key === output);

    return isValidLanguageInput && isValidLanguageOutput;
}