from math import log10

def zhTW2Num(text: str):
    power = {"零": 0, "十": 10, "百": 100, "千": 1000, "萬": 10000, "億": 100000000}
    number = {"零": 0, "一": 1, "二": 2, "兩": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
    point_index = 0
    res = 0.0
    conversion_list = []

    for (i, char) in enumerate(text):
        if char == "點":
            point_index = len(conversion_list)
        val = number.get(char)
        if val != None:
            conversion_list.append(val)
        else:
            val = power.get(char)
            if val != None:
                conversion_list.append(val)

    if point_index > 0:
        float_list = conversion_list[point_index:]
        for (i, num) in enumerate(float_list):
            res += (num * pow(10, -i - 1))
    else:
        point_index = len(conversion_list)

    integral_list = conversion_list[:point_index]
    decimal = 0
    integral = 0
    if any(element >= 10 for element in integral_list):
        is_zero_appeared = False
        unknown_decimal_num = 0
        for (i, num) in enumerate(integral_list):
            if is_zero_appeared:
                # Find the decimal of the number after 0
                if num < 10:
                    unknown_decimal_num = num
                else:
                    # Check the next number is decimal or not
                    if (i + 1) < len(integral_list) and integral_list[i + 1] > num:
                        # 十萬, 百萬, 千萬...
                        decimal = int(log10(num * integral_list[i + 1]))
                    else:
                        # Update the current decimal
                        decimal = int(log10(num))
                    if unknown_decimal_num == 0:
                        # 零十....
                        unknown_decimal_num = 1
                    integral += (unknown_decimal_num * pow(10, decimal))
                    unknown_decimal_num = 0
                    is_zero_appeared = False
            else:
                # Find value between 0 ~ 9.
                if i == 0:
                    integral += num
                    if num == 10:
                        # 10 ~ 19
                        decimal = 1
                elif i == 1 and num >= 10:
                    # find the maximum decimal
                    decimal = int(log10(num))
                    integral *= num
                elif num < 10:
                    if num == 0:
                        # If 零 appeared in Chinese, the next number's decimal won't be the current decimal - 1
                        # ex: 一萬零三十 => 10030
                        is_zero_appeared = True
                    else:
                        decimal -= 1
                        integral += (num * pow(10, decimal))
                elif num > pow(10, decimal):
                    # 十萬, 百萬, 千萬...
                    decimal = int(log10(num))
                    integral *= num

        # If number of unknown decimal exists after loop, add it into the result
        # ex: 一百零六 => 106
        integral += unknown_decimal_num
        res += integral
    else:
        # Give digits only. e.g. 一零六
        for (i, num) in enumerate(integral_list):
            res += (num * pow(10, (len(integral_list) - i - 1)))
    return res
