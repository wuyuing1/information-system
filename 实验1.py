import re

locations = {
    '11': '北京市', '12': '天津市', '13': '河北省', '14': '山西省',
    '15': '内蒙古自治区', '21': '辽宁省', '22': '吉林省', '23': '黑龙江省',
    '31': '上海市', '32': '江苏省', '33': '浙江省', '34': '安徽省',
    '35': '福建省', '36': '江西省', '37': '山东省', '41': '河南省', '42': '湖北省',
    '43': '湖南省', '44': '广东省', '46': '海南省', '50': '重庆市',
    '51': '四川省', '52': '贵州省', '53': '云南省', '54': '西藏自治区', '61': '陕西省',
    '62': '甘肃省', '63': '青海省', '64': '宁夏回族自治区', '65': '新疆维吾尔自治区', '71': '台湾省',
    '81': '香港特别行政区', '82': '澳门特别行政区'
}

def extract_id_info(id_number):
    s = re.search(r'^(\d{2})(\d{4})(\d{4})(\d{2})(\d{2})(\d{2})(\d)(\d|X)$', id_number)
    if s:
        gender = int(s.group(7)) % 2
        province = locations.get(s.group(1))
        birth_date = s.group(3) + '年' + s.group(4) + '月' + s.group(5) + '日'
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check = '10X98765432'
        check_sum = sum(int(id_number[i]) * weights[i] for i in range(17))
        check_digit = check[check_sum % 11]
        if id_number[-1].upper() != check_digit:
            return '该身份证校验码有误'
        else:
            info = ''
            gender_info = '男' if gender == 1 else '女'
            info += f'性别：{gender_info}\n'
            info += f'户籍所在地：{province}\n'
            info += f'出生日期：{birth_date}\n'
            return info
    else:
        return '身份证号码格式错误'

# 从文件读取身份证号码
file_path = r'C:\Users\13936\Desktop\身份证.txt'  # 文件路径
try:
    with open(file_path, 'r') as file:
        id_numbers = file.readlines()
        for id_number in id_numbers:
            id_number = id_number.strip()
            info = extract_id_info(id_number)
            print('身份证号码:', id_number)
            print(info)
            print('----------------------------------------')
except FileNotFoundError:
    print('文件不存在，请确认文件路径是否正确')
