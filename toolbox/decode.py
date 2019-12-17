import base64


def data_url_decode(src, filename):
    """
    解码 Base64 编码的 Data Uri
    """
    data = src.split(',')[1]
    content = base64.b64decode(data)
    with open(filename, 'wb') as file:
        file.write(content)
