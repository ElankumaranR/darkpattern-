import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import BernoulliNB
from sklearn import metrics
from joblib import dump


df1 = pd.read_csv('normie.csv')
df2 = pd.read_csv('dark_patterns.csv')

# Filter out NaN values and select only non-dark patterns from df1
df1 = df1[pd.notnull(df1["Pattern String"])]
df1 = df1[df1["classification"] == 0]
df1["classification"] = "Not Dark"
df1.drop_duplicates(subset="Pattern String", inplace=True)

# Filter out NaN values from df2
df2 = df2[pd.notnull(df2["Pattern String"])]

# Combine dfs and assign classifications
df1["classification"] = "Not Dark"
df2["classification"] = "Dark"
df = pd.concat([df1, df2])

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    df['Pattern String'], df["classification"], train_size=.75, random_state=42)

# Vectorize the text data
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

# Train the classifier
clf = BernoulliNB().fit(X_train_tfidf, y_train)

# Predictions
y_pred = clf.predict(count_vect.transform(X_test))

# Evaluate accuracy
print("Accuracy: ", metrics.accuracy_score(y_pred, y_test))

# Save the classifier and vectorizer
dump(clf, 'presence_classifier.joblib')
dump(count_vect, 'presence_vectorizer.joblib')