# The Translator

## Why this plugin

When you create a multi language website, it's very long to translate all your sentences.

With json_translator, you can translate a json file to many languages.

The plugin will create the json file in according to the language you want to translate.

google-cloud-translate==3.8.4
google-auth==1.35.0
google-api-core==2.8.0
protobuf==3.19.5

## Pre required

To use json_translator plugin you have to create a Google Cloud account.

See : https://cloud.google.com

Please verify in your apis dashboard that cloud translation API service is enable.

In the cloud translation service, go to your credentials.

Please create a service account.

You will have a googlekey.json file which is required to use the API.

## How use it

To use the plugin please write the command line 

    json_translator [options]

You have to use some options.

### Google file (Required)

    json_translator -c googlekey.json
    json_translator --credentials googlekey.json

Used to set the Google credentials.

### File to translate (Required)

    json_translator -i myFile.json
    json_translator --input myFile.json

Used to set the file to translate.

### Destination (Required)

    json_translator -o myFile.json
    json_translator --output myFile.json

Used to set the file to translate.

### Language Source (Optional)

    json_translator -f en
    json_translator --from en

Used to set the source language. By default, value is FR (French).

### Language(s) result (Optional)

    json_translator -l de,it,en
    json_translator --languages de,it,en

### List available languages

    json_translator -a

## Examples

    json_translator -c googlekey.json -i fr.json -o ./myPath/ -l en,de,ko,it,es