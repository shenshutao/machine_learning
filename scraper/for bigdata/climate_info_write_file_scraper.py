import urllib.request
import os
import json
import re
from bs4 import BeautifulSoup

os.chdir("/Users/shutao/Desktop/BDA - spider")
base_url = "https://en.tutiempo.net"

pre_define_continent_list = ['Asia']
#downloaded_list =['Thailand', 'Cambodia'，'Indonesia', 'Thailand', 'Philippines', 'Vietnam', 'Japan', 'Myanmar', 'Sri Lanka', 'Singapore']
#pre_define_country_list = ['China']
#pre_define_city_list = ['HONG KONG OBSERVATO', 'Beijing', 'Shanghai', 'Lhasa', 'XIAN', 'Jiuzhaigou County', 'Shangri-La County', 'Chengdu', 'Huangshan', 'Hangzhou', 'Guangzhou', 'Shenzhen']
pre_define_year_list = ['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018',
                       'Clima 2008', 'Clima 2009', 'Clima 2010', 'Clima 2011', 'Clima 2012', 'Clima 2013', 'Clima 2014', 'Clima 2015', 'Clima 2016', 'Clima 2017', 'Clima 2018']

with open('climate_country_city.json') as json_data:
    country_city_list = json.load(json_data)

pre_define_country_list = country_city_list.keys()


def get_page(uri):
    url = base_url + uri
    req = urllib.request.Request(url, headers={'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"})
    resp = urllib.request.urlopen(req)
    soup = BeautifulSoup(resp, "html.parser")
    return soup

main_page = get_page("/climate")

continent_div = main_page.find("div", {"class": "mlistados mt10"})
for li in continent_div.ul.contents:
    continent_name = li.text.strip()
    if continent_name not in pre_define_continent_list:
        continue

    continent_href = li.a["href"].strip()

    continent_page = get_page(continent_href)
    country_div = continent_page.find("div", {"class": "mlistados mt10"})
    for country_li in country_div.ul.contents:
        country_name = country_li.a.text.strip()
        if country_name not in pre_define_country_list:
            continue

        outfile = open('final_climate_data_' + country_name + '.csv', 'w')

        title = ",".join(
            ["continent_name", "country_name", "city_name", "year_name", "month_name", "day_name", "T", "TM", "Tm",
             "SLP", "H", "PP", "VV", "V", "VM", "VG", "RA", "SN", "TS", "FG"]) + "\n"
        outfile.write(title)
        outfile.flush()

        country_href = country_li.a["href"].strip()
        country_page = get_page(country_href)
        city_divs = country_page.find_all("div", {"class": "mlistados mt10"})

        city_li_list =[]
        for city_div in city_divs:
            city_li_list.extend(city_div.ul.contents)

        num_div = country_page.find("div", {"class": "AntSig"})
        if num_div is not None:
            last_li = num_div.ul.contents[-1]
            last_href = last_li.a["href"]
            m = re.search('(.*)/(\d*)/', last_href)

            for city_page_num in range(2, int(m.group(2))+1):
                page_href = m.group(1) + "/" + str(city_page_num)
                country_page_rest = get_page(page_href)
                more_city_div = country_page_rest.find_all("div", {"class": "mlistados mt10"})
                for city_div in more_city_div:
                    city_li_list.extend(city_div.ul.contents)

        pre_define_city_list = country_city_list[country_name].get('city')
        for city_li in city_li_list:
            try:
                city_name = city_li.text.strip()

                if pre_define_city_list is not None:  # if None, collect all.
                    if city_name not in map(str.upper, pre_define_city_list):
                        continue

                print('start city: ', country_name, ' ', city_name)
                city_href = city_li.find("a")["href"].strip()

                city_page = get_page(city_href)
                yearly_table = city_page.find("table", {"class": "medias"})

                interator = None
                if yearly_table is None:
                    year_table = city_page.find("div", {"class": "mlistados"})
                    interator = year_table.ul.contents
                else:
                    interator = yearly_table.find_all("td", {"class": "tc1"})

                for year_td in interator:
                    year_name = year_td.text.strip()
                    if year_name not in pre_define_year_list:
                        continue

                    year_href = year_td.find("a")["href"].strip()

                    year_page = get_page(year_href)
                    month_div = year_page.find("div", {"class": "mlistados mt10"})
                    for month_li in month_div.ul.contents:
                        month_name = month_li.text.strip()
                        month_href = month_li.a["href"].strip()

                        month_page = get_page(month_href)
                        day_table = month_page.find("table", {"class": "medias"})
                        for day_td in day_table.find_all("tr")[1:-2]:
                            day_name = day_td.contents[0].text.strip()
                            T = day_td.contents[1].text.strip()
                            TM = day_td.contents[2].text.strip()
                            Tm = day_td.contents[3].text.strip()
                            SLP = day_td.contents[4].text.strip()
                            H = day_td.contents[5].text.strip()
                            PP = day_td.contents[6].text.strip()
                            VV = day_td.contents[7].text.strip()
                            V = day_td.contents[8].text.strip()
                            VM = day_td.contents[9].text.strip()
                            VG = day_td.contents[10].text.strip()
                            RA = day_td.contents[11].text.strip()
                            SN = day_td.contents[12].text.strip()
                            TS = day_td.contents[13].text.strip()
                            FG = day_td.contents[14].text.strip()

                            record = ",".join([continent_name, country_name, city_name, year_name, month_name, day_name, T, TM, Tm, SLP, H, PP, VV, V, VM, VG, RA, SN, TS, FG]) + "\n"
                            outfile.write(record)

                        #print("Finish month: ", month_name)
                    print("Finish year: ", year_name)
                outfile.flush()
            except Exception as e:
                print(city_name, e)

            print("Finish city: ", city_name)
        print("Finish country: ", country_name)
    print("Finish continent: ", continent_name)

outfile.close()
