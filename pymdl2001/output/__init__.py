def print_key_info(info=[]):
    """
        对按键信息作输出处理
        :param info:
        :return:
        """
    # for item in info:
    #     print(item)
    print(info)
    chars = []
    dic = info[-1]
    for c in dic:
        if dic[c] == 1:
            chars.append(c)
    chars.sort()
    for c in chars:
        print(c, end='')
    else:
        print()
