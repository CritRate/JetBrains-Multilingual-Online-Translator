import requests
import sys
from bs4 import BeautifulSoup, NavigableString

languages = [
    'All',
    'Arabic',
    'German',
    'English',
    'Spanish',
    'French',
    'Hebrew',
    'Japanese',
    'Dutch',
    'Polish',
    'Portuguese',
    'Romanian',
    'Russian',
    'Turkish'
]


def get_translations_data(from_language, to_language, word_to_translate, number_of_translations):
    link = f'https://context.reverso.net/' \
           f'translation/{from_language.lower()}-' \
           f'{to_language.lower()}/{word_to_translate}'

    try:
        request = requests.get(link, headers={'user-agent': 'Mozilla/5.0'})
    except ConnectionError:
        print('Something wrong with your internet connection')
    else:
        if request:
            soup = BeautifulSoup(request.content, 'html.parser')

            container_one = soup.find('div', {'id': 'translations-content'})
            translations = []

            for c in container_one:
                if not isinstance(c, NavigableString):
                    translations.append(c.text.strip())

            container_two = soup.find_all('div', {'class': 'example'})
            sentences = []

            for c in container_two:
                if not isinstance(c, NavigableString):
                    for val in c.text.split('\n'):
                        if val:
                            val = val.strip()
                            sentences.append(''.join(val))

            return translations[:number_of_translations], [(sentences[i], sentences[i + 1]) for i in
                                                           range(number_of_translations * 2) if i % 2 == 0]
        else:
            print(f'Sorry, unable to find {word}')
            sys.exit()


def write_all_translations_to_file(from_language, word_to_translate):
    with open(f'{word_to_translate}.txt', mode='w', encoding='utf-8') as file:
        for lang in languages:
            if lang != from_language and lang != 'All':
                one_translation, one_example = get_translations_data(from_language=from_language,
                                                                     to_language=lang,
                                                                     word_to_translate=word_to_translate,
                                                                     number_of_translations=1)

                output = formatted_translations(lang=lang,
                                                translations=one_translation,
                                                examples=one_example) + '\n'
                file.write(output)
                print(output)


def formatted_translations(lang, translations, examples):
    output = ''

    output += f'{lang} Translations:\n'

    for s in translations:
        output += f'{s}\n'

    output += '\n'
    output += f'{lang} Examples:\n'

    for s in examples:
        output += f'{s[0]}\n{s[1]}\n\n'

    return output


if __name__ == '__main__':
    from_lang, to_lang, word = sys.argv[1].capitalize(), sys.argv[2].capitalize(), sys.argv[3]
    if from_lang not in languages:
        print(f"Sorry, the program doesn't support {from_lang}")
        sys.exit()
    if to_lang not in languages:
        print(f"Sorry, the program doesn't support {to_lang}")
        sys.exit()

    if to_lang == 'All':
        write_all_translations_to_file(from_language=from_lang,
                                       word_to_translate=word)
    else:
        five_translations, five_examples = get_translations_data(from_language=from_lang,
                                                                 to_language=to_lang,
                                                                 word_to_translate=word,
                                                                 number_of_translations=5)
        if five_translations and five_examples:
            print(formatted_translations(to_lang, five_translations, five_examples))
