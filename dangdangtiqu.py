import urllib.request
import re
import urllib.parse
from lxml import etree

def load_page(url, filename):

    '''


    '''

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "Cookie":"__permanent_id=20240613213250172349148731057634526; ddscreen=2; __visit_id=20240618160014819111175766873577045; __out_refer=; dest_area=country_id%3D9000%26province_id%3D111%26city_id%3D0%26district_id%3D0%26town_id%3D0; __rpm=%7Cmix_104655.850573%2C6411.1.1718700341920; search_passback=bf839150446a5d1d3449716600000000300cc8002e497166; __trace_id=20240618164543488425064592402963245; pos_9_end=1718700343700; pos_6_start=1718700343820; pos_6_end=1718700343825; ad_ids=3225968%2C3225808%2C3225883%7C%231%2C1%2C2"}

    request = urllib.request.Request(url, headers=headers)

    response = urllib.request.urlopen(request)

    # print(response.r4ead())

    return response.read().decode("gbk")
def extract_book_name(book_title):
    book_title = re.sub(r'【.*?】', '', book_title)
    # 去除方括号内的内容
    book_title = re.sub(r'\[.*?\]', '', book_title)
    # 去除可能的价格信息，例如：¥23.90
    book_title = re.sub(r'¥\d+\.\d+', '', book_title)
    # 去除可能的出版社信息，例如：人民文学出版社
    book_title = re.sub(r'\（.*?\）', '', book_title)
    # 去除可能的作者信息，例如：苏轼著
    book_title = re.sub(r'[\（（].*?[\））]', '', book_title)
    # 去除可能的评论数信息，例如：书籍评论数: 4
    book_title = re.sub(r'书籍评论数：\d+', '', book_title)
    # 去除可能的营销信息，例如：新华书店正版...
    book_title = re.sub(r'新华书店正版.*?团购客户请咨询在线客服！', '', book_title, flags=re.DOTALL)
    match = re.match(r'([^（（]+?)[（（]', book_title)
    if match:
        title = match.group(1).strip()
        return title
    else:
        return book_title
def parse_page(html_content):
    # 类别：//*[@id="12810"]  //*[@id="12808"]  //*[@id="search_nature_rg"]  //*[@id="component_59"]
    # 书籍名称：//*[@id="p29245864"]/p[1]/a   //*[@id="p28995532"]/p[1]/a
    # 书籍价格：//*[@id="p29245864"]/p[3]/span[1]   //*[@id="p28995532"]/p[3]/span[1]
    # 书籍出版社：//*[@id="p29245864"]/p[5]/span[3]/a
    # 书籍作者：//*[@id="p29245864"]/p[5]/span[1]/a[1]  //*[@id="p28995532"]/p[5]/span[1]/a[1]
    # 书籍评论数：//*[@id="p29245864"]/p[4]/a   //*[@id="p28995532"]/p[4]/a   //*[@id="p27885837"]/p[4]/a
    root = etree.HTML(html_content)
    items = []
    try:
        items_list = root.xpath('//ul[@class="bigimg"]//li')

        for item_ in items_list:
            name = item_.xpath(".//a/text()")[0].strip()
            name = extract_book_name(name)
            name = name.split('新华书店正版，')[0].strip()
            name = name.split('，')[0].strip()
            name = name.split('。')[0].strip()
            name = name.split('--')[0].strip()
            if len(name.split(' ')) > 1:
                name = name.split(' ')[0] + name.split(' ')[1]

            name = name.strip()

            book_url = 'https:' + item_.xpath(".//img/@src")[0]
            if 'url_none' in book_url:
                book_url = 'https:' + item_.xpath(".//img/@data-original")[0]

            price = item_.xpath(".//p[@class='price']/span[1]/text()")[0].strip()
            publisher = item_.xpath(".//a[@name='P_cbs']/text()")
            if publisher:
                publisher = publisher[0].strip()
            else:
                publisher = "无"
            author = item_.xpath(".//a[@name='itemlist-author']/text()")
            if author:
                author = author[0].strip()
            else:
                author = "无"
            comments = item_.xpath('.//p[@class="search_star_line"]/a/text()')
            if comments:
                comments = comments[0].strip().replace('条评论', '')
            else:
                comments = "0"
            item = {
                "书籍名称": name,
                "书籍封面url": book_url,
                "书籍价格": price,
                "书籍出版社": publisher,
                "书籍作者": author,
                "书籍评论数": comments
            }
            items.append(item)
            print(item)
    except Exception as e:
        print('爬取失败，原因：', e)
    #return items
    print(items)

def tieba_spider(begin, end):
    url_template = "https://category.dangdang.com/pg{}-cp01.03.32.00.00.00.html"
    for i in range(int(begin), int(end) + 1):
        pageurl = url_template.format(i)
        print(pageurl)
        html = load_page(pageurl, " ")
        # print(html)
        parse_page(html)
if __name__ == "__main__":
    begin = int(input("请输入起始页码:"))
    end = int(input("请输入结束页码:"))
    tieba_spider(begin, end)