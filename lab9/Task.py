

import nltk
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')


sia = SentimentIntensityAnalyzer()


def analyze_text(text):
    score = sia.polarity_scores(text)

    if score['compound'] >= 0.05:
        sentiment = "Positive "
    elif score['compound'] <= -0.05:
        sentiment = "Negative "
    else:
        sentiment = "Neutral "

    return score, sentiment


    try:
        df = pd.read_csv(file_path)

        if 'text' not in df.columns:
            print(" CSV must have a column named 'text'")
            return

        df['Sentiment'] = df['text'].apply(lambda x: analyze_text(str(x))[1])

        output_file = "output_sentiment.csv"
        df.to_csv(output_file, index=False)

        print("\n CSV Analysis Complete!")
        print(df.head())

    except Exception as e:
        print("Error:", e)




def analyze_dataset():
    # Sample dataset
    data = {
        "text": [
            "I love this product, it's amazing!",
            "Worst experience ever",
            "It is okay, not great",
            "Absolutely fantastic service",
            "I hate this so much",
            "Not bad, could be better",
            "Very happy with the results",
            "This is terrible",
            "I am satisfied",
            "Awful quality"
        ]
    }

    df = pd.DataFrame(data)

    # Apply sentiment analysis
    df['Sentiment'] = df['text'].apply(lambda x: analyze_text(x)[1])

  
    counts = df['Sentiment'].value_counts()

    print("\n Dataset Analysis Result:")
    print(df)

    print("\n Summary:")
    print(counts)

   
    df.to_csv("dataset_output.csv", index=False)
    print("\n Saved as dataset_output.csv")

def main():
    while True:
        print("\n===== Sentiment Analysis (VADER) =====")
        print("1. Analyze Single Text")
        print("2. Analyze CSV File")
        print("3. Analyze Built-in Dataset ")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            text = input("\nEnter your text: ")
            score, sentiment = analyze_text(text)

            print("\n Result:")
            print("Scores:", score)
            print("Sentiment:", sentiment)

        elif choice == '2':
            path = input("\nEnter CSV file path: ")
            analyze_csv(path)

        elif choice == '3':
            analyze_dataset()

        elif choice == '4':
            print("Exiting program...")
            break

        else:
            print(" Invalid choice. Try again.")


# Run Program

if __name__ == "__main__":
    main()