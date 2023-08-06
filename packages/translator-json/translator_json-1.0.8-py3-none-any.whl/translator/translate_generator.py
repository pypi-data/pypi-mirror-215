import json
import os
import re
import sys

import click
from google.cloud import translate
from google.oauth2 import service_account

source = 'fr'
DEFAULT_LANGUAGES = ['en', 'de', 'ko']
location = "global"
parent = f"projects/clickandco-301800/locations/{location}"

"""
    Translate text to a target language
    exclude params
    :arg text - text to translate
    :arg target - target language
    :return translated text
"""


def translate_text(text, target, translate_client, glossary):
    # Find translate params
    params = re.findall(r"{{\w+}}", text)
    for param in params:
        parsedParam = param.replace(
            '{{', '<span translate="no">').replace('}}', '</span>')
        # no translate params
        text = text.replace(param, parsedParam)

    if glossary is not None:
        glossary_config = translate.TranslateTextGlossaryConfig(
            glossary=glossary
        )

        return translate_client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",  # mime types: text/plain, text/html
                "source_language_code": "fr",
                "target_language_code": target,
                "glossary_config": glossary_config,
            }
        )

    return translate_client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": "fr",
            "target_language_code": target,
        }
    )


"""
    Translate all values from dictionary data to language dest
    :argument
        data: dictionary
        language: language dest
    :return
        translated dictionary
"""


def translate_language(data, language, translate_client, glossary):
    for key in data.keys():
        if isinstance(data[key], str):
            value = data[key]
            translation = translate_text(
                value,
                language,
                translate_client,
                glossary
            )
            data[key] = translation.translations[0].translated_text.replace(
                '<span translate="no">', '{{').replace('</span>', '}}')
        else:
            translate_language(data[key], language, translate_client, glossary)


def silent_remove(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print("The file does not exist")


def write_translate_file(data, language, output):
    # delete old version file
    silent_remove(output + '/' + language + '.json')
    with open(output + '/' + language + '.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def read_json_file(file):
    f = open(file)
    data = json.load(f)
    f.close()
    return data


@click.command(help=f"""
Translate all the value of a json file in a language given in
argument using the google translate
API. The supported language are English, Deutsch, Korean and French.
""")
@click.option('--credentials', '-c', type=str,
              help='google key credentials file')
@click.option('--input', '-i', type=str,
              help='path to the json file to translate')
@click.option('--output', '-o', type=str,
              help='path to the json file translated')
@click.option('--languages', '-l', default=None,
              help="""the language to translate
              must be 'en', 'de' or 'ko'""")
@click.option('--available', '-a',
              is_flag=True, default=False,
              help="List available languages")
@click.option('--glossary', '-g', default=None,
              help='Id of the glossary to be used for the traduction')
def json_translator(
        credentials,
        input,
        output,
        languages=None,
        available=False,
        glossary=None
):
    credentials = read_json_file(credentials)

    credentials_dist = service_account.Credentials.from_service_account_info(
        credentials
    )
    translate_client = translate.TranslationServiceClient(
        credentials=credentials_dist
    )
    if glossary is not None:
        glossary = translate_client.glossary_path(
            project=credentials['project_id'],
            location='west-1',
            glossary=glossary
        )

    if available:
        response = translate_client.get_supported_languages(parent=parent)

        for language in response.languages:
            print("Language Code: {}".format(language.language_code))

        return

    if languages is None:
        languages = DEFAULT_LANGUAGES

    for language in languages:
        f = open(input)
        data = json.load(f)
        f.close()
        translate_language(data, language, translate_client, glossary)
        write_translate_file(data, language, output)
