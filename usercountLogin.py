import requests
import os
import re

headers_login = {
    "Host": "forever.pork17.com",
    "User-Agent": "Mozilla/5.0 (Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0"
}

# 用户名和密码列表
users_list = [
    ('账号A', '密码A'),
    ('账号B', '密码B'),
    ('账号C11', '密码C')
]


def loginMain(headers_login):
    # 从网站登录后的主界面，获取剩余流量并写入result.txt
    def getRemainingTraffic():
        # print("开始获取剩余流量")
        # 打开LoginText.txt文件并读取内容
        with open(file_path_login, 'r', encoding='utf-8') as file:
            content = file.read()

        # 使用正则表达式匹配从id="remain">开始到第一个</code>结束的内容
        match = re.search(r'id="remain">(.*?)</code>', content, re.DOTALL)
        # 检查是否找到了匹配项
        if match:
            # 提取匹配到的内容（不包括id="remain">和</code>）
            extracted_text = match.group(1)

            # 拼接字符串"剩余流量"
            combined_text = "剩余流量：" + extracted_text

            # 将拼接后的字符串写入result.txt文件
            with open(file_path_result, 'a', encoding='utf-8') as file:
                file.write(combined_text + '\n')
            # print("成功将剩余流量写入result.txt")
            print(combined_text)
        else:
            print("在LoginText.txt中未找到匹配的剩余流量。")

    # 从网站登录后的主界面，获取上次签到时间并写入result.txt
    def getCheckinTime():
        # print("开始获取上次签到时间")
        # 打开LoginText.txt文件并读取内容
        with open(file_path_login, 'r', encoding='utf-8') as file:
            content = file.read()

        # 使用正则表达式匹配从从"上次签到时间："开始，直到第一个</p>结束的内容
        match = re.search(r'上次签到时间：(.*?)</p>', content, re.DOTALL)
        # 检查是否找到了匹配项
        if match:
            # 提取匹配到的内容（上次签到时间：和</p>）
            extracted_text = match.group(1)

            # 拼接字符串"上次签到时间"
            combined_text = "上次签到时间：" + extracted_text + '\n'
            combined_text_print = "上次签到时间：" + extracted_text
            # 将拼接后的字符串写入result.txt文件
            with open(file_path_result, 'a', encoding='utf-8') as file:
                file.write(combined_text + '\n')
            # print("成功将上次签到时间写入result.txt")
            print(combined_text_print)
        else:
            print("在LoginText.txt中未找到匹配的上次签到时间。")

    # 从网站用户资料界面，获取账户信息并写入result.txt
    def getUserInfo():
        # print("开始获取账户信息")
        # 打开UserText.txt文件并读取内容
        with open(file_path_user, 'r', encoding='utf-8') as file:
            content = file.read()

        # 使用正则表达式匹配从从"data-cfemail="开始，直到第一个">结束的内容
        match = re.search(r'data-cfemail="([^"]*)"', content, re.DOTALL)
        # 检查是否找到了匹配项
        if match:
            # 提取匹配到的内容（data-cfemail=和">）
            extracted_text = match.group(1)

            # 邮箱地址被加密，使用email-decode.min.js可解密
            # 解密方法参考：https://blog.csdn.net/weixin_44106555/article/details/126032204
            # print("已获取加密邮箱加密字符串，开始解密.......")

            # 十六进制转十进制
            def ox2dec(ox: str):
                return int(ox, 16)

            # 解密加密账户信息的方法
            def decodeEmail(to_decode: str):
                decode = []
                key = ox2dec(to_decode[:2])  # 前两位为密钥
                # data = []
                for i in range(2, len(to_decode), 2):
                    to_decode_i = ox2dec(to_decode[i:i + 2])
                    # print(to_decode_i,key)
                    decode_i = to_decode_i ^ key  # 十进制异或会先转二进制异或，结果再转回十进制
                    decode.append(chr(decode_i))  # 十进制数转字符
                return "".join(decode)

            # 获取解密后的账户信息
            extracted_text = decodeEmail(extracted_text)

            # 拼接字符串"账户信息："
            combined_text = "账户信息：" + extracted_text

            # 将拼接后的字符串写入result.txt文件
            with open('result.txt', 'a', encoding='utf-8') as file:
                file.write(combined_text + '\n')
            # print("成功将账户信息写入result.txt")
            return extracted_text
        else:
            print("在UserText.txt中未找到匹配的账户信息。")

    # 格式化cookie格式，为签到做准备
    def transform_string(s):
        # 替换单引号、逗号和括号
        s = s.replace("'", "")  # 移除单引号
        s = s.replace(", ", "; ")  # 将逗号加空格替换为分号加空格
        # 注意：这里我们不替换 '{' 和 '}' 为双引号，因为这不是标准的做法
        # 但如果你确实需要这样做（尽管不推荐），你可以添加以下两行
        s = s.replace("{", "")
        s = s.replace("}", "")

        # 由于没有单引号包围键值对了，我们可以安全地添加等号
        s = s.replace(": ", "=")

        # 如果你想在字符串的开始和结束添加双引号（尽管这也不是标准的）
        # s = "\"" + s + "\""

        return s

    # 登录后开始对数据进行处理，并进行签到

    #初始化txt记录保存路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = ''
    file_path_result = os.path.join(script_dir, 'result.txt')
    file_path_login = os.path.join(script_dir, 'LoginText.txt')
    file_path_user = os.path.join(script_dir, 'UserText.txt')
    with open(file_path_result, 'w', encoding='utf-8') as file:
        file.write('')
    # 网站登录URL
    login_url = 'https://forever.pork17.com/auth/login'

    # 创建一个session对象以处理cookies
    session = requests.Session()

    for email, passwd in users_list:
        # 准备登录表单数据
        payload = {
            'email': email,
            'passwd': passwd
        }

        # 发送POST请求到登录URL
        response = session.post(login_url, data=payload, headers=headers_login)

        # 检查登录是否成功
        if response.status_code == 200:
            # 假设状态码200表示登录成功，实际情况可能需要根据页面内容判断

            # 显示登录成功，并将结果写入result.txt
            loginfo = f"登录成功：{email}"
            print(loginfo)

            with open(file_path_result, 'a', encoding='utf-8') as file:
                file.write(loginfo + '\n')

            # 如果需要后续请求，并且登录成功设置了cookie或session，你可以使用session对象来保持登录状态
            session = requests.Session()
            session.post(login_url, data={'email': email, 'passwd': passwd})

            # 获取cookie值，并将其转换为字符串格式
            cookies = f"{session.cookies.get_dict()}"

            # 使用session对象发送其他请求，将保持登录状态，进行后续签到等操作
            # 保存网站登录后的主界面，用于获取剩余流量、上次签到时间
            def saveLoginInfo():
                response = session.get('https://forever.pork17.com/user')
                # 将网页数据暂存至LoginText.txt中，为截取所需数据做准备
                with open(file_path_login, 'w', encoding='utf-8') as file:
                    file.write(response.text)
                # print("成功保存 LoginText.txt")

            # 保存网站登录后的用户界面，用于获取用户名进行校对
            def saveUserInfo():
                response = session.get('https://forever.pork17.com/user/profile')
                # 将网页数据暂存至UserText.txt中，为截取所需数据做准备
                with open(file_path_user, 'w', encoding='utf-8') as file:
                    file.write(response.text)
                # print("成功保存 UserText.txt")
                return loginfo

            #开始签到
            def doCheckIn(cookies):
                # 调用函数并打印结果
                cookies = transform_string(cookies)
                url = 'https://forever.pork17.com/user/checkin'
                headers_checkIn = {
                    'Accept': "application/json, text/javascript, */*; q=0.01",
                    'Accept-Encoding': "gzip, deflate, br, zstd",
                    'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                    'Content-Length': "0",
                    'Cookie': cookies,
                    'Origin': "https://forever.pork17.com",
                    'Priority': "u=1, i",
                    'Referer': "https://forever.pork17.com/user",
                    'Sec-Ch-Ua': "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
                    'Sec-Ch-Ua-Mobile': "?0",
                    'Sec-Ch-Ua-Platform': "Windows",
                    'Sec-Fetch-Dest': "empty",
                    'Sec-Fetch-Mode': "cors",
                    'Sec-Fetch-Site': "same-origin",
                    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                    'X-Requested-With': "XMLHttpReques"
                }

                response = requests.post(url, headers=headers_checkIn)

                # 检查请求是否成功
                if response.status_code == 200:
                    print(f"签到成功: {email}")
                else:
                    print(f"请求失败，状态码：{response.status_code}，错误信息：{response.text}")

            def logout():
                response = session.get('https://forever.pork17.com/user/logout')
                print(f"已退出账户: {email}" + '\n')

            doCheckIn(cookies)  # 签到
            saveLoginInfo()  # 存储登录后的主界面数据，用于获取剩余流量、上次签到时间并存储
            saveUserInfo()  # 存储登录后的用户界面，用于获取用户名进行校对并存储
            getUserInfo()  # 从网站用户资料界面，获取账户信息并写入result.txt
            getRemainingTraffic()  # 从网站登录后的主界面，获取剩余流量并写入result.txt
            getCheckinTime()  # 从网站登录后的主界面，获取上次签到时间并写入result.txt
            logout()  # 退出
        else:
            print(f"登录失败: {username}, 状态码: {response.status_code}")
    # sleep(2)  # 暂停2秒（如果需要的话）


loginMain(headers_login)
