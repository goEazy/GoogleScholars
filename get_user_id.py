import urllib.request
import sys
import re
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

with open("user_id.csv", mode='w', encoding='utf-8') as file_id:
    file_id.write("Name,User Id\n");
file_id.close();

with open("scholar_database.csv", mode='w', encoding='utf-8') as file_sdb:
    file_sdb.write("Name;User Id;Name of Paper;Authors;Publication Date;Journal;Volume;Issue;Pages;Total Citations\n");
    print("Writting");
file_sdb.close();

scholar = "https://scholar.google.co.in";
person = "";
person_id = "";
mega_count = 0;
verified_email = "iemcal.com"
#iemcal.com is taken as an example"
def articleFunction(paper_url):
    paper_url = scholar + paper_url;
    req_paper = Request(paper_url, headers={'User-Agent':'Mozilla/5.0'});
    html_paper = urlopen(req_paper).read();
    html_paper = html_paper.decode('utf-8');
    soup_paper = BeautifulSoup(html_paper, 'html.parser');
    title_d = soup_paper.find('div', attrs={"id" : "gsc_title"});
    title = title_d.text;
    print("Title : " + title);
    to_find = ['Authors', 'Publication date', 'Journal', 'Volume', 'Issue', 'Pages', 'Total citations'];
    details = soup_paper.find_all('div', attrs={"class" : "gs_scl"});
    got_value = ["","","","","","",""]
    for detail in details:
        key_d = detail.find('div', attrs={"class":"gsc_field"});
        key = key_d.text;
        val_d = detail.find('div', attrs={"class":"gsc_value"});
        for tf in to_find:
            if(key == tf):
                if(key == 'Total citations'):
                    vall = val_d.find('div', attrs={"style":"margin-bottom:1em"}).text;
                    regex = "^Cited by (.+?)$";
                    pattern = re.compile(regex);
                    got_value[to_find.index(tf)] = pattern.findall(vall)[0];
                else:
                    got_value[to_find.index(tf)] = val_d.text;
    for tf in to_find:
        print(tf + " : " + got_value[to_find.index(tf)]);
    try:
        with open("scholar_database.csv", mode="a", encoding='utf-8') as file_sdb:
            file_sdb.write(person+";"+person_id+";"+title+";"+got_value[0]+";"+got_value[1]+";"+got_value[2]+";"+got_value[3]+";"+got_value[4]+";"+got_value[5]+";"+got_value[6] + "\n");
        file_sdb.close();
        #print("File Written");
    except:
        print("File Not Written");


def userFunction(user_url):
    req_user = Request(user_url, headers={'User-Agent':'Mozilla/5.0'});
    html_user = urlopen(req_user).read();
    html_user = html_user.decode('utf-8');
    soup_user = BeautifulSoup(html_user, 'html.parser');
    papers = soup_user.find_all('td',attrs={"class" : "gsc_a_t"});
    print(len(papers))
    cc=0;
    global mega_count
    for paper in papers:
        try:
            paper_name = paper.a.text;
            paper_link = paper.a['href'];
            cc=cc+1;
            print("\n");
            #print(str(cc+mega_count) + ". " + paper_name);
            articleFunction(paper_link);
        except:
            print("...");
    if(cc>=20):
        try:
            extra = "&cstart="+str(mega_count+cc)+"&pagesize=20";
            mega_count+=20;
            user_url = user_url + extra;
            #print(user_url);
            userFunction(user_url);
        except:
            print(cc);

lines = [line.rstrip('\n') for line in open('faculty_list.txt')]
#print(str(lines));
for name in lines:
    #print(name);
    srch_url = scholar+"/citations?mauthors="+name+"+iemcal.com&hl=en&view_op=search_authors";
    req_srch = Request(srch_url, headers={'User-Agent':'Mozilla/5.0'});
    try:
        html_srch = urlopen(req_srch).read();
        html_srch = html_srch.decode('utf-8');
        soup_srch = BeautifulSoup(html_srch, 'html.parser');
        #print(htmltext)
        #print(soup.prettify());
        users = soup_srch.find_all('h3',attrs={"class" : "gsc_1usr_name"});
        for link in users:
            user_link = link.a['href'];
            person = link.text;
            regex = "user=(.+?)&hl=en"
            pattern = re.compile(regex);
            person_id = re.findall(pattern, user_link)[0];
            with open("user_id.csv", mode='a', encoding='utf-8') as file_id:
                file_id.write(person + "," + person_id + "\n");
            print(link.text);
            global mega_count;
            mega_count = 0;
            userFunction(scholar+user_link);
            print("\n---------------------------------------------------****---------------------------------------------------\n\n");
    except:
        print("Error");
