# 使用flask框架
# 我是想要将URL重定向到pnpm run dev的Vue项目，（即当访问/时，重定向到http://localhost:5173/）所有URL都应该对应至http://localhost:5173/{URL}
# 实现代码
import httpx
from flask import Flask, request
from urllib.parse import urljoin

app = Flask(__name__)
VUE_DEV_SERVER = "http://localhost:5173"

# 创建持久化客户端，启用连接池和压缩
client = httpx.Client(
    base_url=VUE_DEV_SERVER,
    timeout=30.0,
    follow_redirects=True,
    headers={"Accept-Encoding": "gzip"},
)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    target_url = urljoin(VUE_DEV_SERVER + "/", path)
    
    try:
        # 移除 hop-by-hop 头部（如 Connection）
        headers = {k: v for k, v in request.headers if k.lower() != 'connection'}
        
        resp: httpx.Response = client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            params=request.args,
            data=request.get_data(),
            files=request.files,
            timeout=30.0
        )

        print(resp.content)
        
        return (
            resp.content,
            resp.status_code,
            dict(resp.headers)
        )
    except Exception as e:
        return f"Proxy Error: {str(e)}", 500

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(port=5000, debug=True)
