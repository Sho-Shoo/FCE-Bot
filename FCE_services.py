
def get_fce_info_by_cnum(cnum: int): 
    return f"{cnum} info: ... "

def get_fce_info_by_cname(cname: str): 
    return f"{cname} info ... "

def get_fce_info(query: str):
    try: 
        course_num = int(query)
        return get_fce_info_by_cnum(course_num)
    except ValueError: 
        return get_fce_info_by_cname(query) 
    except Exception as e:
        print(e)
        return "Unknown error encountered. Try again. "


