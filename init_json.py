import json

# 定义一个函数来保存用户信息到JSON文件
def save_user_info_to_json(user_info, filename):
    with open(filename, 'w') as file:
        json.dump(user_info, file)

# 定义一个函数来加载JSON文件中的用户信息
def load_user_info_from_json(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # 如果文件不存在，返回一个空字典

# 示例用户信息字典
user_info = {
    'admin': '123'
}

# 保存用户信息到JSON文件
save_user_info_to_json(user_info, 'user_info.json')

# 加载JSON文件中的用户信息
loaded_user_info = load_user_info_from_json('user_info.json')
print("Loaded user info:", loaded_user_info)
