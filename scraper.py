import requests
from bs4 import BeautifulSoup
from datetime import datetime

output = [f"# 📰 오늘의 인기 커뮤니티 게시글 ({datetime.now().strftime('%Y-%m-%d')})\n"]

def fetch_ruliweb():
    url = "https://bbs.ruliweb.com/news/board/1001"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")
    posts = soup.select("table.board_list_table tbody tr:not(.notice)")
    output.append("## 루리웹")
    count = 0
    for post in posts:
        title_tag = post.select_one("a.deco")
        views_tag = post.select_one("td.view")
        likes_tag = post.select_one("td.recommend")
        if title_tag and views_tag and likes_tag:
            title = title_tag.text.strip()
            link = title_tag['href'] if 'http' in title_tag['href'] else 'https://bbs.ruliweb.com' + title_tag['href']
            views = views_tag.text.strip()
            likes = likes_tag.text.strip()
            output.append(f"- [{title}]({link}) 👍 {likes} 추천, 👁️ {views} 조회")
            count += 1
        if count >= 5:
            break
    output.append("")

def fetch_dcinside():
    url = "https://gall.dcinside.com/board/lists/?id=hit"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")
    posts = soup.select("table.gall_list tbody tr.ub-content")
    output.append("## 디시인사이드")
    count = 0
    for post in posts:
        title_tag = post.select_one("a.ub-word")
        views_tag = post.select_one("td.gall_count")
        rec_tag = post.select_one("td.gall_recommend")
        if title_tag and views_tag and rec_tag:
            title = title_tag.text.strip()
            link = "https://gall.dcinside.com" + title_tag['href']
            views = views_tag.text.strip()
            rec = rec_tag.text.strip()
            output.append(f"- [{title}]({link}) 👍 {rec} 추천, 👁️ {views} 조회")
            count += 1
        if count >= 5:
            break
    output.append("")

def fetch_dogdrip():
    url = "https://www.dogdrip.net/index.php?mid=dogdrip&sort_index=pop&order_type=desc"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")
    posts = soup.select("tr.title a.link")
    output.append("## 개드립")
    count = 0
    for post in posts:
        href = post.get('href')
        if not href or 'document_srl' not in href:
            continue
        title = post.text.strip()
        link = "https://www.dogdrip.net" + href
        output.append(f"- [{title}]({link})")
        count += 1
        if count >= 5:
            break
    output.append("")

fetch_ruliweb()
fetch_dcinside()
fetch_dogdrip()

with open("output.md", "w", encoding="utf-8") as f:
    f.write("\n".join(output))
