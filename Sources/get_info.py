def get_info_from_title_str(title_str: str)-> dict:
    """
    从文件名字符串中提取：文件名、作者、发表时间等信息，并以字典类型返回结果。
    例如
    title_str = '4. Revisiting Double-Spending Attacks on the Bitcoin Blockchain_New Findings(J.Zheng&etal, Jun.2021).pdf'
    info_dict = get_info_from_title_str(title_str)
    其中
    info_dict = {
        'title': 'Revisiting Double-Spending Attacks on the Bitcoin Blockchain_New Findings',
        'authors': ('J.Zheng', 'etal'),  # 从中可以进一步提取更细的作者信息
        'public_month': 'June',
        'public_year': '2021',
        'file_type': 'pdf',
        # 若有其他信息，应该进一步添加 key-value 对
    }
    """
    info_dict = {}


    return info_dict

