import requests
import MiejskiDefinicja
import datetime

def sprawdz_raw(slowo):
    baselink = "https://www.miejski.pl/slowo-" + slowo.replace(" ", "+")
    r = requests.get(baselink)
    if r.status_code == 200:
        return r.text
    else:
        return ""

def sprawdz_link(link):
    return sprawdz(link.replace("https://www.miejski.pl/slowo-", "").replace("+", " "))

def sprawdz(slowo):
    r = sprawdz_raw(slowo)
    definicje : list[object] = []
    url = "https://www.miejski.pl/slowo-" + slowo.replace(" ", "+")
    for i in range(len(r.split('<article id="')) - 1):
        iddef = r.split('<article id="')[i + 1].split('"')[0]
        article = r.split(f"""<article id="{iddef}""")[1]
        classnegative = article.split(">")[0]
        iddef = iddef.split(classnegative + ">")[0]
        #article = article.split(classnegative + ">")[1]
        slowo = article.split("<header><h1>")[-1].split("</h1></header>")[0]
        ocena = article.split('<span class="rating">')[1].split("</span>")[0]
        definicja = article.split("</div>\r\n                                <p>\r\n                ")[-1].split("                </p>\r\n")[0]
        if(True):
            footer = article.split("<footer>")[1].split("</footer>")[0]
            dialog = []
            if(len(article.split("<blockquote>")) != 1):
                xd = article.split("<blockquote>")[-1].split("</blockquote>")[0].split("<br />")
                for i in xd:
                    dialog.append(i.replace("\n-", "").replace("\r", "").replace("  ", ""))
            else:
                dialog = None
                
            author = footer.split('<div class="author">Autor:')[1].split("</div>")[0].split("</a>")[0].split(">")[1]
            tags = []
            tagsnew = footer.split('<div class="tags">Tagi:')[-1].split("</div>")[0]
            temptags = tagsnew.split("</a>")
            for i in temptags:
                z = i.split(">")[-1]
                if(z == author):
                    continue
                tags.append(z)
            tags.pop(len(tags) - 1)
            # <div class="published-date" title="2021-02-01 18:15:54">Data dodania: 2021-02-01</div>
            dateandtime = footer.split('<div class="published-date" title="')[-1].split('">')[0]
            date = datetime.date(
                int(dateandtime.split(" ")[0].split("-")[0]),
                int(dateandtime.split(" ")[0].split("-")[1]),
                int(dateandtime.split(" ")[0].split("-")[2])
            )
            time = None
            try:
                time = datetime.time(
                    int(dateandtime.split(" ")[1].split(":")[0]),
                    int(dateandtime.split(" ")[1].split(":")[1]),
                    int(dateandtime.split(" ")[1].split(":")[2])
                )
            except:
                time = datetime.time(0, 0, 0)
        #except:
        #    dialog : list[str] = []
        #    tags : list[str] = []
        #    author : str = ""
        #    date : datetime.date = datetime.date.today()
        #    time : datetime.time = datetime.time(0, 0, 0)
        definicje.append(
            MiejskiDefinicja.Definicja(slowo, ocena, definicja, dialog, tags, author, date, time, url, iddef)
        )
    return definicje