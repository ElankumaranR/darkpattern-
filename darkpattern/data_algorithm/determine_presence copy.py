import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.externals import joblib

dark_pattern_data = pd.read_csv('darkpattern.csv')
normie_data = pd.read_csv('normie.csv')

normie_data = normie_data[normie_data['classification'] == 0]

dark_pattern_data['classification'] = dark_pattern_data["Pattern Type"]
normie_data['classification'] = 'Not Dark'

df = pd.concat([dark_pattern_data, normie_data])

X_train, X_test, y_train, y_test = train_test_split(
    df['Pattern String'], df["Pattern Type"], train_size=0.75, random_state=42)

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

clf = MultinomialNB().fit(X_train_tfidf, y_train)

X_test_counts = count_vect.transform(X_test)
X_test_tfidf = tfidf_transformer.transform(X_test_counts)
y_pred = clf.predict(X_test_tfidf)

print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

joblib.dump(clf, 'dark_pattern_classifier.joblib')
joblib.dump(count_vect, 'dark_pattern_vectorizer.joblib')
