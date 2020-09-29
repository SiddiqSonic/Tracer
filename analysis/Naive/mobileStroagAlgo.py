import pandas as pd
import re
from nltk.corpus import stopwords


#lading Dataset in pandas
dataset = pd.read_csv(r"C:/Users/Siddiq/Desktop/mobile_stroage.csv")
dataset = pd.DataFrame(dataset)
dataset.columns = ["Text", "Reviews"]

corpus = []

for i in range(len(dataset)):
    text = dataset['Text'][i]
    corpus.append(text)

print(corpus)
#creating Bag of word
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, 1].values

#transforming into tfidf vectorizer
from sklearn.feature_extraction.text import TfidfTransformer
transformer=TfidfTransformer()
X=transformer.fit_transform(X).toarray()

# splitting the data set into training set and test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)

# fitting naive bayes to the training set
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# predicting test set results
y_pred = classifier.predict(X_test)


# making the confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)
print(((cm[0][0]+cm[1][1]+cm[2][2])/len(X_test))*100)

#Pickling the classifier
import pickle
with open('Mobile_Stroageclassifier.pickle','wb') as f:
    pickle.dump(classifier,f)

#creating bag of word tfidfvectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
TfVec = TfidfVectorizer()
X = TfVec.fit_transform(corpus).toarray()

#picking the tfidf vectorizer
with open('Mobile_StroagetfidfVectorizerModel.pickle','wb') as f:
    pickle.dump(TfVec,f)