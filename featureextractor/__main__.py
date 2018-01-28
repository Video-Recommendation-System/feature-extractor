from __future__ import print_function
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
    unique_classifications = set()
    for x in range(0, len(descriptions)):
        text = descriptions.iloc[x]
        print(titles[x])

        document = types.Document(
            content = text,
            type = enums.Document.Type.PLAIN_TEXT)
        sentiments.append(get_sentiment(client, document))
        categories = []
        for category in get_classification(client, document).categories:
            categories.append((category.name.encode("utf-8"), category.confidence))
            unique_classifications.add(category.name.encode("utf-8"))

        classifications.append(categories)

    data["sentiment"] = sentiments
    data["classifications"] = classifications

    for classification in unique_classifications:
        column = []
        for categories_set in data["classifications"]:
            any_match = False
            for category_pair in categories_set:
                if category_pair[0] == classification:
                    column.append(category_pair[1])
                    any_match = True
            if not any_match:
                column.append(0.0)

        data[classification] = column

    print(data)
    data.to_csv(output_file, index=False)

def get_sentiment(client, document):
    return client.analyze_sentiment(document=document).document_sentiment.magnitude

def get_classification(client, document):
    return client.classify_text(document)

if __name__ == "__main__":
    main()
