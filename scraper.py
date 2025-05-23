import requests
from bs4 import BeautifulSoup
from datetime import datetime

output = [f"# 📰 오늘의 인기 커뮤니티 게시글 ({datetime.now().strftime('%Y-%m-%d')})\n"]

def fetch_ruliweb():
    url = "https://bbs.ruliweb.com/news/board/1001"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")
    posts = soup.select(".board_main tr.table_body")[:5]
    output.append("## 루리웹")
    for post in posts:
        title_tag = post.select_one("a.subject")
        if title_tag:
            title = title_tag.text.strip()
            link = title_tag['href']
            stats = post.select("td")
            views = stats[-1].text.strip()
            likes = stats[-2].text.strip()
            output.append(f"- [{title}]({link}) 👍 {likes} 추천, 👁️ {views} 조회")
    output.append("")

def fetch_dcinside():
    url = "https://gall.dcinside.com/board/lists/?id=hit"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")
    posts = soup.select("table.gall_list tbody tr.ub-content")[:5]
    output.append("## 디시인사이드")
    for post in posts:
        title_tag = post.select_one("a.subject")
        if title_tag:
            title = title_tag.text.strip()
            link = "https://gall.dcinside.com" + title_tag['href']
            views = post.select_one("td.gall_count").text.strip()
            rec = post.select_one("td.gall_recommend").text.strip()
            output.append(f"- [{title}]({link}) 👍 {rec} 추천, 👁️ {views} 조회")
    output.append("")

def fetch_dogdrip():
    url = "https://www.dogdrip.net/index.php?mid=dogdrip&sort_index=pop&order_type=desc"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")
    posts = soup.select(".ed.board-list .title a")[:5]
    output.append("## 개드립")
    for post in posts:
        title = post.text.strip()
        link = "https://www.dogdrip.net" + post['href']
        output.append(f"- [{title}]({link})")
    output.append("")

fetch_ruliweb()
fetch_dcinside()
fetch_dogdrip()

with open("output.md", "w", encoding="utf-8") as f:
    f.write("\n".join(output))
