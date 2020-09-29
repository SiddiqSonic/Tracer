import pandas as pd
import re
from nltk.corpus import stopwords


#lading Dataset in pandas
dataset = pd.read_csv(r"C:/Users/Siddiq/Desktop/bigdata.csv")
dataset = pd.DataFrame(dataset)
dataset.columns = ["Text", "Reviews"]

corpus = []

for i in range(len(dataset)):
    text = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', ' ', dataset['Text'][i])
    text = re.sub(r'@[A-Za-z0-9_]+',' ', text)
    text = text.lower()
    text = re.sub(r"that's","that is",text)
    text = re.sub(r"there's","there is",text)
    text = re.sub(r"what's","what is",text)
    text = re.sub(r"where's","where is",text)
    text = re.sub(r"it's","it is",text)
    text = re.sub(r"who's","who is",text)
    text = re.sub(r"i'm","i am",text)
    text = re.sub(r"she's","she is",text)
    text = re.sub(r"he's","he is",text)
    text = re.sub(r"they're","they are",text)
    text = re.sub(r"who're","who are",text)
    text = re.sub(r"ain't","am not",text)
    text = re.sub(r"wouldn't","would not",text)
    text = re.sub(r"shouldn't","should not",text)
    text = re.sub(r"couldn't","could not",text)
    text = re.sub(r"can't","can not",text)
    text = re.sub(r"won't","will not",text)
    text = re.sub(r'@[^\s]+',' ', text)
    text = re.sub(r"\W"," ",text)
    text = re.sub(r"\d"," ",text)
    text = re.sub(r"^\s"," ",text)
    text = re.sub(' +',' ', text)
    text = text.strip()
    corpus.append(text)

print(corpus)
#creating Bag of word
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=2000,min_df=1,max_df=0.6,stop_words=stopwords.words('english'))
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, 1].values

#transforming into tfidf vectorizer
from sklearn.feature_extraction.text import TfidfTransformer
transformer=TfidfTransformer()
X=transformer.fit_transform(X).toarray()

# splitting the data set into training set and test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

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
with open('classifier.pickle','wb') as f:
    pickle.dump(classifier,f)

#creating bag of word tfidfvectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
TfVec = TfidfVectorizer(max_features=2000,min_df=1,max_df=0.6,stop_words=stopwords.words('english'))
X = TfVec.fit_transform(corpus).toarray()

#picking the tfidf vectorizer
with open('tfidfVectorizerModel.pickle','wb') as f:
    pickle.dump(TfVec,f)