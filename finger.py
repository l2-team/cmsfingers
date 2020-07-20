import json
import threading

import requests
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed, FIRST_EXCEPTION, wait, ALL_COMPLETED
from optparse import OptionParser

threadingLock = threading.Lock()
show_count = 0
SCAN_COMPLATED = False


def md5encode(text):
    m = hashlib.md5()
    m.update(text.encode("utf-8"))
    return m.hexdigest()


def check_file_is_ok(url, path):
    """
    head 请求方式去判断文件是否存在, 减少正文响应时间
    :param url:
    :param path:
    :return:
    """
    target = url + path
    r = requests.head(target)

    if r.status_code == 200:
        return True
    return False


def get_request_md5(url, path, pattern):
    """
    通过请求路径获取内容的md5
    :param url:
    :param path:
    :param pattern:
    :return:
    """
    target = url + path
    r = requests.get(target)

    r_md5 = md5encode(r.text)

    if pattern == r_md5:
        return True
    return False


def load_cms_fingers():
    """
    加载CMS指纹
    :return:
    """
    with open("fingers_simple.json") as f:
        data = json.load(f)

    print("Update Time: {}".format(data.get("update_time")))
    print("CMS Fingers Count: {}".format(len(data['data'])))
    return data['data']


def check_thread(item):
    global show_count
    global SCAN_COMPLATED
    url, finger = item
    path = finger.get("path")

    threadingLock.acquire()
    show_count += 1
    if not SCAN_COMPLATED:
        print('\r', "扫描进度 {}/{}".format(show_count, fingers_count), end='', flush=True)
    threadingLock.release()

    if check_file_is_ok(url, path):
        match_pattern = finger.get("match_pattern")

        result = get_request_md5(url, path, match_pattern)

        if result:
            print("\nHint CMS名称: {}".format(finger.get("cms")))
            print("Hint 指纹文件: {}".format(finger.get("path")))
            print("Hint Md5: {}".format(finger.get("match_pattern")))
            SCAN_COMPLATED = True
            raise Exception("任务结束")


if __name__ == '__main__':
    usage = "%prog -u \"http://xxxx.com\" -t threads_number"
    parser = OptionParser(usage=usage)
    parser.add_option("-u", "--url", dest="url", help="目标URL")
    parser.add_option("-t", "--threads", dest="threads", type="int", default=10, help="线程大小, 默认为 10")
    options, args = parser.parse_args()

    if not options.url:
        parser.print_help()
        exit(0)

    fingers = load_cms_fingers()
    url = options.url

    fingers_count = len(fingers)

    executor = ThreadPoolExecutor(max_workers=options.threads)
    tasks = [executor.submit(check_thread, ((url, finger))) for finger in fingers]

    wait(tasks, return_when=FIRST_EXCEPTION)

    for task in reversed(tasks):
        task.cancel()

    wait(tasks, return_when=ALL_COMPLETED)
