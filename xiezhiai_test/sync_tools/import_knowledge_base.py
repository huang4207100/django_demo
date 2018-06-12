import requests
import base64

urlBase='http://39.106.49.104:8022'

realBase='http://47.94.21.219:8023'
testBase='http://39.106.49.104:8022'

def rest_post(url, post_form_map={}, post_json_map={}, header_map={}, files={}, timeout=0):
    # print ('11')
    try:
        res = ""
        if timeout <= 0:
            res = requests.post(url=url, data=post_form_map, json=post_json_map, headers=header_map, files=files)
        else:
            res = requests.post(url=url, data=post_form_map, json=post_json_map, headers=header_map, files=files, timeout=timeout)
        #return json.dumps(res.json()), True
        #print("header:%s" % (str(res.headers)), " ", type(res.headers))
        return res.json(), res.headers, True
    except Exception as e:
        print("post:%s json:%s form:%s headers:%s timeout:%s err:" % (url, str(post_json_map), str(post_form_map), str(header_map), timeout), e)
        return None, None, False

my_header = {}

def user_login(mobile="12345678",pwd="12332111"):
    url = '%s/bg/login' % (urlBase)
    j = {
        "mobile": mobile ,  # 电话号码
        "pwd": base64.b64encode(pwd.encode()).decode('utf-8')  # 设置的密码
    }
    res, _h, ret = rest_post(url=url, post_json_map=j)

    if ret == False or res['succ'] == False:
        print("login failed %s false: %s" % (str(j), str(res)))
        return False, None

    i = res['data']
    i2 = i.get("header")
    global my_header
    my_header = {
        'UID': i2.get("UID"),
        'TENANTID': i2.get("TENANTID"),
        'LTIME': i2.get("LTIME"),
        'SIGN': i2.get("SIGN"),
    }

    print("login success %s succ:%s" % (str(j), str(res)))
    return True, res['data']

#16 批量增加问题信息 POST
def upload_excel_to_tenant(file_name=r"/home/liangtian/services/model.xlsx", package_id=0):
    url = '%s/bg/add_question_by_excel' % (urlBase)
    form = {
        "package_id": package_id,
    }
    with open(file=file_name, mode='rb') as f:

        res, _h, ret = rest_post(url=url, post_form_map=form, header_map=my_header, files={'file': f})
        if ret == False or res['succ'] == False:
            print("upload_excel_to_tenant %s false:%s" % (str(form), str(res)))
            return False
        print("upload_excel_to_tenant %s succ:%s" % (str(form), str(res)))
        return True

#20. 活动知识库包的excel文件   POST
def get_package_excel(package_id=0):
    url = '%s/bg/get_package_excel' % (urlBase)
    form = {
        "package_id": package_id,
    }
    res, _h, ret = rest_post(url=url, post_form_map=form, header_map=my_header)
    if ret == False or res['succ'] == False:
        print("get_package_excel failed %s false:%s" % (str(form), str(res)))
        return False
    print("get_package_excel success %s succ:%s" % (str(form), str(res)))
    return True, res

def format_print(s):
    print()
    print(s)
    print()

#15得到所有的问题列表  POST "category_id": [631]  && "key_words": ["0"]
def get_question_lst(package_id=0,pn=1,ps=20,cond={}):
    j = {
        "package_id": package_id,
        "ps": ps,
        "pn": pn,
        "cond": cond
    }
    r = requests.post("{0}/bg/get_question_lst".format(urlBase), json=j, headers=my_header)
    jr = r.json()
    print("get_question", jr)
    if jr.get("succ") is True:
        print("PASS: get question")
        return jr
    else:
        print("FAILURE: get question")
        return False

#13删除问题   POST
def del_question(id=[3441]):

    j = {
        "main_ids": id
    }
    r = requests.post("{0}/bg/del_question".format(urlBase), json=j, headers=my_header)
    jr = r.json()
    print("del_question", jr)
    if jr.get("succ") is True:
        print("PASS: del question")
        return False
    else:
        print("FAILURE: del question")
        return True

def download_from_url(url):
    excel = requests.get(url)
    with open("info.xlsx",'wb') as f:
        f.write(excel.content)

def del_all_question():
    n = 1
    while True:
        n += 1
        if n == 100:
            return

        try:
            rs = get_question_lst()['data']['list']
        except:
            print("接口出错")
            return

        if len(rs) == 0:
            break

        ids = [x['id'] for x in rs]
        print(ids)
        del_question(id=ids)

if __name__ == "__main__":
    # 查询的账号和密码
    # 上传的账号和密码
    urlBase = realBase
    user_login(mobile='13721095230',pwd='xzkj123456')
    excelurl = get_package_excel()[1]["data"]["endpoint_ori"]
    download_from_url(excelurl)

    urlBase = realBase
    user_login(mobile='17302396584',pwd='12345678')
    del_all_question()
    upload_excel_to_tenant(file_name='info.xlsx')
