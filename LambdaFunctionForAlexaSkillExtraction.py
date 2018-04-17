from bs4 import BeautifulSoup as bs
import requests as rq
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}
titles = []
links = []
s = [
    """'https://www.amazon.com/s/ref=sr_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284819011&page='+str(j)+'&ie=UTF8&qid=1523302187'""",
    """'https://www.amazon.com/s/ref=lp_14284865011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284864011%2Cn%3A14284865011&page='+str(j)+'&ie=UTF8&qid=1523389246'""",
    """'https://www.amazon.com/s/ref=lp_14284820011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284820011&page='+str(j)+'&ie=UTF8&qid=1523389647'""",
    """'https://www.amazon.com/s/ref=lp_14284821011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284821011&page='+str(j)+'&ie=UTF8&qid=1523389808'""",
    """'https://www.amazon.com/s/ref=lp_14284822011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284822011&page='+str(j)+'&ie=UTF8&qid=1523389961'""",
    """'https://www.amazon.com/s/ref=lp_14284827011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284827011&page='+str(j)+'&ie=UTF8&qid=1523390091'""",
    """'https://www.amazon.com/s/ref=lp_14284831011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284831011&page='+str(j)+'&ie=UTF8&qid=1523390209'""",
    """'https://www.amazon.com/s/ref=lp_17388364011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284837011%2Cn%3A17388364011&page='+str(j)+'&ie=UTF8&qid=1523390374'""",
    """'https://www.amazon.com/s/ref=lp_13727921011_nr_n_8?fst=as%3Aoff&rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284832011&bbn=13727922011&ie=UTF8&qid=1523390535&rnid=13727922011'""",
    """'https://www.amazon.com/s/ref=lp_14284837011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284837011&page='+str(j)+'&ie=UTF8&qid=1523390696'""",
    """'https://www.amazon.com/s/ref=lp_14284844011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284844011&page='+str(j)+'&ie=UTF8&qid=1523390791'""",
    """'https://www.amazon.com/s/ref=lp_14284846011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284846011&page='+str(j)+'&ie=UTF8&qid=1523390866'""",
    """'https://www.amazon.com/s/ref=lp_14284851011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284851011&page='+str(j)+'&ie=UTF8&qid=1523390950'""",
    """'https://www.amazon.com/s/ref=lp_14284857011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284857011&page='+str(j)+'&ie=UTF8&qid=1523391035'""",
    """'https://www.amazon.com/s/ref=lp_14284858011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284858011&page='+str(j)+'&ie=UTF8&qid=1523391104'""",
    """'https://www.amazon.com/s/ref=lp_14284859011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284859011&page='+str(j)+'&ie=UTF8&qid=1523391169'""",
    """'https://www.amazon.com/s/ref=lp_14284862011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284862011&page='+str(j)+'&ie=UTF8&qid=1523391234'""",
    """'https://www.amazon.com/s/ref=lp_14284863011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284863011&page='+str(j)+'&ie=UTF8&qid=1523391297'""",
    """'https://www.amazon.com/s/ref=lp_14284864011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284864011&page='+str(j)+'&ie=UTF8&qid=1523391361'""",
    """'https://www.amazon.com/s/ref=lp_14284869011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284869011&page='+str(j)+'&ie=UTF8&qid=1523391362'""",
    """'https://www.amazon.com/s/ref=lp_14284874011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284874011&page='+str(j)+'&ie=UTF8&qid=1523391363'""",
    """'https://www.amazon.com/s/ref=lp_14284882011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284882011&page='+str(j)+'&ie=UTF8&qid=1523391364'""",
    """'https://www.amazon.com/s/ref=lp_14284889011_pg_'+str(j)+'?rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284889011&page='+str(j)+'&ie=UTF8&qid=1523393019'""",
]
a = []
for st in s:
    stt = st.split("+str(j)+")
    a.append(stt)
cnt = [55, 8, 3, 221, 37, 377, 48, 3, 2, 153, 29, 21, 220, 243, 108, 72, 8, 57, 17, 47, 42, 21, 40]
names = ['Business', 'Communication', 'Connected Car', 'Education and Reference', 'Food and Drink', 'Games, Trivia and Accessories',
         'Health and Fitness', 'Home Services', 'Kids', 'Lifestyle', 'Local', 'Movies and TV', 'Music and Audio', 'News',
         'Novelty and Humor', 'Productivity', 'Shopping', 'Smart Home', 'Social', 'Sports', 'Travel and Transportation',
         'Utilities', 'Weather'
         ]

invokations = []
descriptions = []

with open('output.csv', 'w') as f:
    wr = csv.writer(f)
    for i in range(24):
        try:
            for j in range(1, cnt[i]+1):
                stri = ""
                if i is 8:
                    stri = a[i][0].replace("'", "")
                else:
                    stri = a[i][0].replace("'", "")+str(j)+a[i][1].replace("'", "")+str(j)+a[i][2].replace("'", "")
                page = rq.get(stri, headers=headers)
                soup = bs(page.content, 'html.parser')
                for k in range(16*(j-1), 16*j):
                    cur = soup.find('li', id='result_'+str(k))
                    if cur:
                        titles.append(cur.find('h2').text)
                        l = cur.find('a')
                        link = l['href']
                        try:
                            page = rq.get(link, headers=headers)
                            soup = bs(page.content, 'html.parser')
                            try:
                                d2 = soup.find('div', id='a2s-skill-details')
                                inv = d2.find('span', {'class': 'a-text-bold'}).text
                            except:
                                inv = ''
                            try:
                                d1 = soup.find('div', id='a2s-description')
                                des = d1.find('span').text
                            except:
                                des = ''
                            if inv is '' and des is '':
                                print("Probably blocked by amazon now..")
                            invokations.append(inv)
                            descriptions.append(des)
                            wr.writerow([titles[-1], invokations[-1], descriptions[-1]])
                        except Exception as e:
                            print("Error in %s was %s.... :- ..." % (link, e))

        except Exception as e:
            print("Error in %s was .... :- ... %s" % (i, e))

