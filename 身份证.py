import re

def get_province(id_number):
    province_dict = {
        '11': '北京市', '12': '天津市', '13': '河北省', '14': '山西省', '15': '内蒙古自治区',
        '21': '辽宁省', '22': '吉林省', '23': '黑龙江省', '31': '上海市', '32': '江苏省',
        '33': '浙江省', '34': '安徽省', '35': '福建省', '36': '江西省', '37': '山东省',
        '41': '河南省', '42': '湖北省', '43': '湖南省', '44': '广东省', '45': '广西壮族自治区',
        '46': '海南省', '50': '重庆市', '51': '四川省', '52': '贵州省', '53': '云南省',
        '54': '西藏自治区', '61': '陕西省', '62': '甘肃省', '63': '青海省', '64': '宁夏回族自治区',
        '65': '新疆维吾尔自治区', '71': '台湾省', '81': '香港特别行政区', '82': '澳门特别行政区'
    }
    province_code = id_number[:2]
    return province_dict.get(province_code, '未知')

def calculate_verify_code(id_number):
    id_sum = sum(int(id_number[i]) * (2 ** (17 - i)) for i in range(17))
    verify_code = str((12 - id_sum % 11) % 11)
    if verify_code == '10':
        verify_code = 'X'
    return verify_code

def check_id_card(id_number):
    pattern = re.compile( 
        r'^(\d{6})(\d{4})(\d{2})(\d{2})(\d{3})([0-9Xx])$'
    )
    match = pattern.match(id_number)
    
    if match:
        area = get_province(id_number)
        day = f"{match.group(2)}-{match.group(3)}-{match.group(4)}"
        gender_code = match.group(5)
        gender = "男" if int(gender_code) % 2 == 1 else "女"
        verify_code = calculate_verify_code(id_number)
        
        if verify_code == match.group(6).upper():
            return f"所属地区：{area}，出生日期：{day}，性别：{gender}，检验数：{verify_code}，校验通过"
        else:
            return "校验失败：身份证号码校验码错误"
    else:
        return "输入的身份证号码格式不正确"

id_number = input("请输入您的身份证号码：")
result = check_id_card(id_number)
print(result)