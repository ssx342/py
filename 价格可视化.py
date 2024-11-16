import pyecharts
from pyecharts.charts import Line
from pyecharts import options as opts
import pymysql
# 数据库配置信息
db_config = {
    'user': 'root',
    'password': '123456',
    'host': 'localhost',
    'database': 'dddb',
    'charset': 'utf8mb4'
}

# 连接数据库
connection = pymysql.connect(**db_config)
try:
    with connection.cursor() as cursor:
        try:
            # 查询前100个书籍的价格
            select_query = "SELECT id, price FROM booksinfo ORDER BY id LIMIT 100"
            cursor.execute(select_query)

            # 获取查询结果
            books_data = cursor.fetchall()

            # 调整为ECharts的数据格式
            books_ids = [book[0] for book in books_data]  # 提取书籍ID作为x轴
            # price字段是数值字符串，需要转换为float
            books_prices = [float(book[1].replace('¥', '')) for book in books_data]  # 提取并转换价格

            # 创建折线图
            line = (
                Line()
                .add_xaxis(books_ids)              # 添加X轴数据
                .add_yaxis("Price", books_prices)  # 添加Y轴数据
                .set_global_opts(title_opts=opts.TitleOpts(title="Books Prices"))    # 设置标题
            )

            # 渲染图表到HTML文件中
            line.render("books_prices_line_chart.html")

        except pymysql.MySQLError as err:
            print("数据库查询出错：", err)

finally:
    # 关闭数据库连接
    connection.close()

print("图表已生成，请打开 'books_prices_line_chart.html' 查看。")
