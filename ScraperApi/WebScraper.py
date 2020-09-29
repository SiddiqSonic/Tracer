from itertools import islice
import requests, pickle, re, os, time
from django.conf import settings
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stop_words = set(stopwords.words('english'))


with open(os.path.join(settings.BASE_DIR, r'analysis\Naive\classifier.pickle'), 'rb') as f:
    clf = pickle.load(f)

with open(os.path.join(settings.BASE_DIR, r'analysis\Naive\tfidfVectorizerModel.pickle'), 'rb') as f:
    tfidf = pickle.load(f)

with open(os.path.join(settings.BASE_DIR, r'analysis\Naive\Mobile_osclassifier.pickle'), 'rb') as f:
    mob_os_clf = pickle.load(f)

with open(os.path.join(settings.BASE_DIR, r'analysis\Naive\Mobile_ostfidfVectorizerModel.pickle'), 'rb') as f:
    mob_os_tfidf = pickle.load(f)

with open(os.path.join(settings.BASE_DIR, r'analysis\Naive\Mobile_Stroageclassifier.pickle'), 'rb') as f:
    mob_stroag_clf = pickle.load(f)

with open(os.path.join(settings.BASE_DIR, r'analysis\Naive\Mobile_StroagetfidfVectorizerModel.pickle'), 'rb') as f:
    mob_stroag_tfidf = pickle.load(f)

with open(os.path.join(settings.BASE_DIR, r'analysis\Naive\Mobile_Displayclassifier.pickle'), 'rb') as f:
    mob_display_clf = pickle.load(f)

with open(os.path.join(settings.BASE_DIR, r'analysis\Naive\Mobile_DisplaytfidfVectorizerModel.pickle'), 'rb') as f:
    mob_display_tfidf = pickle.load(f)

with open(os.path.join(settings.BASE_DIR, r'analysis\Naive\Mobile_Cameraclassifier.pickle'), 'rb') as f:
    mob_camera_clf = pickle.load(f)

with open(os.path.join(settings.BASE_DIR, r'analysis\Naive\Mobile_CameratfidfVectorizerModel.pickle'), 'rb') as f:
    mob_camera_tfidf = pickle.load(f)


class GsmarenaScraper():
    def moblie_links(self, phone_name, count):

        url = "https://www.gsmarena.com/results.php3?sQuickSearch=yes&sName=" + phone_name + ""

        user_agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        headers = {'User-Agent': user_agent}

        html_page = requests.get(url, headers=headers)
        html = html_page.text

        soup = BeautifulSoup(html, 'html.parser')
        soup = soup.findAll('div', class_="makers")

        for links in soup:
            links = links.find_all('a')

            print(len(links))
            for link in links:
                count = count - 1
                if count >= 0:
                    url = "https://www.gsmarena.com/" + link['href']
                    time.sleep(1)
                    self.all_opinions(url)
                    print("check")
    mobile_data_list = []

    def all_opinions(self, url):
        user_agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        headers = {'User-Agent': user_agent}

        html_page = requests.get(url, headers=headers)
        html = html_page.text
        soup = BeautifulSoup(html, 'html.parser')
        #############        The below code scrap the mobile features        #############

        mobile_image = soup.find_all("div", class_="specs-photo-main")
        mobile_name = soup.find_all("h1", class_="specs-phone-name-title")
        mobile_os = soup.select("span[data-spec=os-hl]")
        mobile_storage = soup.select("span[data-spec=storage-hl]")
        mobile_display1 = soup.select("span[data-spec=displaysize-hl]")
        mobile_display2 = soup.select("div[data-spec=displayres-hl]")
        mobile_camer = soup.find_all("li", class_="help accented help-camera")

        for m_img,m_name,m_os, m_storage, m_display1, m_display2, m_camera in zip(mobile_image,mobile_name,mobile_os, mobile_storage, mobile_display1,mobile_display2, mobile_camer):
            mobile_featuers = {}

            links = m_img.find_all('img')
            for link in links:
                mobile_featuers["Mobile_image"] = link["src"]
            mobile_featuers["Mobile_Name"] = m_name.text
            mobile_featuers["Operating_System"] = m_os.text
            mobile_featuers["Storage"] = m_storage.text
            mobile_featuers["Display"] = m_display1.text + " " + m_display2.text
            camera = m_camera.text
            mobile_featuers["Camera"] = " ".join(camera.split())
            self.mobile_data_list.append(mobile_featuers)

        #############             Scraping mobile featuer code end            #############
        link = soup.findAll('div', class_="button-links")
        for links in link:
            links = links.find_all('a', class_="button")
            flag = True
            for link in links:
                if flag:
                    url = "https://www.gsmarena.com/" + link['href']
                    self.opinions_text(url)
                    flag = False

    count = 3
    review = []

    def opinions_text(self, url):

        user_agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        headers = {'User-Agent': user_agent}

        html_page = requests.get(url, headers=headers)
        html = html_page.text
        soup = BeautifulSoup(html, 'html.parser')
        reviews = soup.findAll('p', class_='uopin')
        reply_date = soup.findAll('a', class_='uinreply')
        replys = soup.findAll('span', class_='uinreply-msg')

        for review in reviews:
            review = review.text
            for date in reply_date:
                date = str(date.text)
                review = review.replace(date, '')
            for reply in replys:
                review = review.replace(reply.text, '')
            self.review.append(review)
        soup = soup.findAll('div', class_="nav-pages")
        for link in soup:
            if self.count >= 0:
                link = link.find_all('a')
                if not link:
                    break
                url = "https://www.gsmarena.com/" + link[-1]['href']
                time.sleep(1)
                print(self.count)
                self.count = self.count - 1
                self.opinions_text(url)
            else:
                break

    def scraper(self, phone_name='Nokia', count=2):
        count = int(count)
        phone_name = phone_name.replace('_',' ')
        self.moblie_links(phone_name, count)
        data = []
        mob_data = []
        for text in self.review:
            dic = {}
            dic['text'] = text
            dic['clean_text'] = self.clean_text(text)
            dic['sentiment'] = self.get_text_sentiment(text)
            data.append(dic)
        for featuer in self.mobile_data_list:
            dic = {}

            dic['Mobile_image'] = featuer["Mobile_image"]
            dic['Mobile_Name'] = featuer["Mobile_Name"]
            dic['Operating_System'] = featuer["Operating_System"]
            s = self.get_Mobile_os_sentiment(featuer["Operating_System"])
            dic['mob_os_sentiment']=''.join(s)
            dic['Storage'] = featuer["Storage"]
            s = self.get_Mobile_stroage_sentiment(featuer["Storage"])
            dic['mob_stroag_sentiment'] = ''.join(s)
            dic['Display'] = featuer["Display"]
            s = self.get_Mobile_display_sentiment(featuer["Display"])
            dic['mob_display_sentiment'] = ''.join(s)
            dic['Camera'] = featuer["Camera"]
            s = self.get_Mobile_camera_sentiment(featuer["Camera"])
            dic['mob_camera_sentiment'] = ''.join(s)
            mob_data.append(dic)
        return data,mob_data

    def clean_text(self, text):
        text = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', ' ', text)
        text = re.sub(r'@[A-Za-z0-9_]+', ' ', text)
        text = text.lower()
        text = re.sub(r"that's", "that is", text)
        text = re.sub(r"there's", "there is", text)
        text = re.sub(r"what's", "what is", text)
        text = re.sub(r"where's", "where is", text)
        text = re.sub(r"it's", "it is", text)
        text = re.sub(r"who's", "who is", text)
        text = re.sub(r"i'm", "i am", text)
        text = re.sub(r"she's", "she is", text)
        text = re.sub(r"he's", "he is", text)
        text = re.sub(r"they're", "they are", text)
        text = re.sub(r"who're", "who are", text)
        text = re.sub(r"ain't", "am not", text)
        text = re.sub(r"wouldn't", "would not", text)
        text = re.sub(r"shouldn't", "should not", text)
        text = re.sub(r"couldn't", "could not", text)
        text = re.sub(r"can't", "can not", text)
        text = re.sub(r"won't", "will not", text)
        text = re.sub(r'@[^\s]+', ' ', text)
        text = re.sub(r"\W", " ", text)
        text = re.sub(r"\d", " ", text)
        text = re.sub(r"^\s", " ", text)
        text = re.sub(' +', ' ', text)
        text = text.strip()
        word_tokens = word_tokenize(text)
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        filtered_sentence = ' '.join(filtered_sentence)
        return filtered_sentence

    def get_text_sentiment(self, text):
        ls = [text]
        text = tfidf.transform(ls).toarray()
        return clf.predict(text)

    def get_Mobile_os_sentiment(self, featuer):
        ls = [featuer]
        featuer = mob_os_tfidf.transform(ls).toarray()
        return mob_os_clf.predict(featuer)
    def get_Mobile_stroage_sentiment(self, featuer):
        ls = [featuer]
        featuer = mob_stroag_tfidf.transform(ls).toarray()
        return mob_stroag_clf.predict(featuer)
    def get_Mobile_display_sentiment(self, featuer):
        ls = [featuer]
        featuer = mob_display_tfidf.transform(ls).toarray()
        return mob_display_clf.predict(featuer)
    def get_Mobile_camera_sentiment(self, featuer):
        ls = [featuer]
        featuer = mob_camera_tfidf.transform(ls).toarray()
        return mob_camera_clf.predict(featuer)

    def wordcount(self, text=[]):
        counts = dict()
        for word in text:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
        return counts



    def take(n, iterable):
        "Return first n items of the iterable as a list"
        return list(islice(iterable, n))

