import requests,pickle,re,os,time
from django.conf import settings
from bs4 import BeautifulSoup

with open(os.path.join(settings.BASE_DIR, r'analysis\Naive\classifier.pickle'), 'rb') as f:
    clf = pickle.load(f)

with open(os.path.join(settings.BASE_DIR, r'analysis\Naive\tfidfVectorizerModel.pickle'), 'rb') as f:
    tfidf = pickle.load(f)

class GsmarenaScraper():
    def moblie_links(self,phone_name,count):
        phone_name = phone_name.replace('_',' ')
        url = "https://www.gsmarena.com/results.php3?sQuickSearch=yes&sName=" + phone_name + ""

        user_agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        headers = {'User-Agent': user_agent}

        html_page = requests.get(url, headers=headers)
        html = html_page.text

        soup = BeautifulSoup(html,'html.parser')
        soup = soup.findAll('div',class_="makers")

        for links in soup:
            links = links.find_all('a')

            print(len(links))
            for link in links:
                count = count - 1
                if count >= 0:
                    url="https://www.gsmarena.com/"+link['href']
                    time.sleep(1)
                    self.all_opinions(url)
                    print("check")

    def all_opinions(self,url):
        user_agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        headers = {'User-Agent': user_agent}

        html_page = requests.get(url, headers=headers)
        html = html_page.text
        soup = BeautifulSoup(html, 'html.parser')
        soup = soup.findAll('div', class_="button-links")
        for links in soup:
            links = links.find_all('a',class_="button")
            flag = True
            for link in links:
                if flag:
                    url ="https://www.gsmarena.com/"+link['href']
                    self.opinions_text(url)
                    flag = False

    count = 10
    review = []
    def opinions_text(self,url):

        user_agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        headers = {'User-Agent': user_agent}

        html_page = requests.get(url, headers=headers)
        html = html_page.text
        soup = BeautifulSoup(html, 'html.parser')
        reviews = soup.findAll('p', class_='uopin')
        reply_date = soup.findAll('a',class_='uinreply')
        replys = soup.findAll('span',class_='uinreply-msg')

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
                url = "https://www.gsmarena.com/" + link[-1]['href']
                time.sleep(1.5)
                print(self.count)
                self.count = self.count - 1
                self.opinions_text(url)

    def scraper(self,phone_name='Nokia',count=2):
        self.moblie_links(phone_name, count)
        data = []
        for text in self.review:
            dic = {}
            dic['text'] = text
            dic['clean_text']=self.clean_text(text)
            dic['sentiment']=self.get_text_sentiment(text)
            data.append(dic)
        return data

    def clean_text(self,text):
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
        return text

    def get_text_sentiment(self, text):
        ls = [text]
        text=tfidf.transform(ls).toarray()
        return clf.predict(text)



