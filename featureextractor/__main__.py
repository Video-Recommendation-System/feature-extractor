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
    classifications = []
    descriptions = data["description"]
    titles = data["video_title"]
    for x in range(0, len(descriptions)):
        text = descriptions.iloc[x]
        print titles[x]

        document = types.Document(
            content = text,
            type = enums.Document.Type.PLAIN_TEXT)
        sentiments.append(get_sentiment(client, document))
        categories = []
        for category in get_classification(client, document).categories:
            categories.append((category.name.encode("utf-8"), category.confidence))
        classifications.append(categories)

    data["sentiment"] = sentiments
    data["classifications"] = classifications

    print data
    data.to_csv(output_file, index=False)


def get_sentiment(client, document):
    a = client.analyze_sentiment(document=document)

    return a.document_sentiment.magnitude

def get_classification(client, document):
    return client.classify_text(document)

if __name__ == "__main__":
    main()
