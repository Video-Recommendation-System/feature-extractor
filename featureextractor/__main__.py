from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import pandas as pd
import sys

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    data = pd.read_csv(input_file)

    client = language.LanguageServiceClient()

    sentiments = []
    for text in data["description"]:
        sentiments.append(get_data(client, text))

    data["sentiment"] = sentiments

    print data
    data.to_csv(output_file, index=False)


def get_data(client, text):
    document = types.Document(
        content = text,
        type = enums.Document.Type.PLAIN_TEXT)

    return client.analyze_sentiment(document=document).document_sentiment.magnitude

if __name__ == "__main__":
    main()
