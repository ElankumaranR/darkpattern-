import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import BernoulliNB
from sklearn import metrics
from joblib import dump


df1 = pd.read_csv('normie.csv')
df2 = pd.read_csv('dark_patterns.csv')

df1 = df1[pd.notnull(df1["Pattern String"])]
df1 = df1[df1["classification"] == 0]
df1["classification"] = "Not Dark"
df1.drop_duplicates(subset="Pattern String")

df2 = df2[pd.notnull(df2["Pattern String"])]
df2["classification"] = "Dark"
col = ["Pattern String", "classification"]
df2 = df2[col]

df = pd.concat([df1, df2])

X_train, X_test, y_train, y_test = train_test_split(
    df['Pattern String'], df["classification"], train_size = .25)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

clf = BernoulliNB().fit(X_train_tfidf, y_train)

y_pred = clf.predict(count_vect.transform(X_test))

print("Accuracy: ", metrics.accuracy_score(y_pred, y_test))



dump(clf, 'presence_classifer.joblib')
dump(count_vect, 'presence_vectorizer.joblib')