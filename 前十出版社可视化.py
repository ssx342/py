import flask
from flask import request, jsonify, make_response
import pymysql
import DBhelper
server = flask.Flask(__name__)
@server.route('/test', methods=['GET', 'POST'])
def get_top_publishers():
    try:
        # 连接到数据库
        conn = DBhelper.DBHelper(host="127.0.0.1", user="root", password="123456", db="dddb")
        sql = """  
            SELECT publisher, COUNT(name) AS num_books  
            FROM booksinfo  
            GROUP BY publisher  
            ORDER BY num_books DESC  
            LIMIT 10;  -- 只获取前10个出版社  
            """
        result = conn.fetch_all(sql)  # 假设fetch_all能正确处理并返回结果

        # 构造数据
        publisher_data = [{'name': row['publisher'], 'value': row['num_books']} for row in result]

        # 如果没有找到任何数据，可以返回一个空的数据集或适当的错误消息
        if not publisher_data:
            return jsonify({"error": "No publishers found"}), 404

            # 构造并返回JSON响应
        # 定义一个配置项字典，用于配置饼图的显示
        option = {
            # 配置图表的标题
            "title": {
                "text": "top10出版社的书籍分布",  # 设置标题文本
                "left": "center"  # 设置标题的位置为居中
            },
            # 配置提示框组件
            "tooltip": {
                "trigger": "item"  # 触发类型设置为'item'，即数据项图形触发
            },
            # 配置图例组件
            "legend": {
                "orient": "vertical",  # 设置图例的排列方向为垂直
                "left": "left"  # 设置图例的位置为左侧
            },
            # 配置系列列表
            'series': [
                {
                    'name': 'Top 10 Publishers by Books',  # 设置系列名称
                    'type': 'pie',  # 设置图表类型为饼图
                    'data': publisher_data,  # 设置饼图的数据，publisher_data需要在此前定义
                    # 配置数据项的高亮样式
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,  # 设置阴影的模糊大小
                            "shadowOffsetX": 0,  # 设置阴影水平方向上的偏移
                            "shadowColor": "rgba(0, 0, 0, 0.5)"  # 设置阴影的颜色
                        }
                    }
                }
            ]
        }

        resp = make_response(jsonify(option))   # 设置HTTP响应的头部信息
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp   # 返回一个含title,tooltip,legend,series字段的JSON响应对象
    except pymysql.MySQLError as e:   # 异常处理
        print(f"MySQL Error: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


if __name__ == "__main__":
    server.run(port=8000,debug=True)