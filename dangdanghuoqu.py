import urllib.request
import urllib.parse
import time

def load_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    return response.read()


def write_page(html, filename):
    print("正在保存", filename)
    with open(filename, 'wb') as file:
        file.write(html)


def dangdang_spider(kw, begin, end):
    base_url = "https://search.dangdang.com/?"  # 注意这里移除了key=
    key = urllib.parse.urlencode({"key": kw})  # 构造key参数
    initial_url = base_url + key  # 初始URL，包含搜索关键词

    for page in range(int(begin), int(end) + 1):
        # 假设当当网的分页参数是page_index=x，这里需要根据实际情况调整
        page_param = urllib.parse.urlencode({"page_index": page})  # 构造分页参数，这里假设是page_index
        if page > 1:  # 第一页不需要额外的分页参数
            page_url = f"{initial_url}&{page_param}"  # 构造搜索和分页的URL
        else:
            page_url = initial_url  # 第一页直接使用初始URL

        print(page_url)
        html = load_page(page_url)
        filename = f"D:\\dangdang_page_{page}.html"  # 更好的文件名，包括关键词可能会更好
        write_page(html, filename)
        time.sleep(1)  # 休眠时间


if __name__ == "__main__":
    kw = input("请输入关键词:")
    begin = input("请输入起始页码:")
    end = input("请输入结束页码:")
    try:
        begin = int(begin)
        end = int(end)
        dangdang_spider(kw, begin, end)
    except ValueError:
        print("输入的页码必须为整数！")