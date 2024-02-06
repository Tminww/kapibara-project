import requests
import feedparser
import sys
from requests.models import Response
import fake_useragent
from multiprocessing.pool import ThreadPool
import logging


# проверка статуса ответа
def response_res(response):
    status = True
    if response.status_code != 200:
        status = False
    return {"status": status, "code": response.status_code, "reason": response.reason}


# try-except декоратор
def try_request(req):
    def wrap(url):
        status = False
        try:
            response = req(url)
            error = 0
            status = True
        except Exception as ex:
            response = Response()
            response.reason = ex
            response.status_code = 444
            error = sys.exc_info()[1]
        return {"status": status, "response": response, "error": error}

    return wrap


# основная функция запроса
@try_request
def get_response(url):
    s = requests.Session()
    user = fake_useragent.UserAgent().random
    header = {"user-agent": user}
    response = s.get(url, headers=header)
    logging.info(f"{url}, {response.status_code}, {s.cookies}")
    return response


# проверка содержания ответа
def check_feed(response):
    status = False
    lenta = feedparser.parse(response.text)
    if lenta["entries"]:
        status = True
    return {"status": status, "lenta": lenta["entries"]}


# сборная всех проверок и запроса
def harvest_all(url):
    response = get_response(url)
    response_stat = response_res(response["response"])
    feed_res = check_feed(response["response"])
    res_dict = {
        "feed": url,
        "response": response,
        "response_status": response_stat,
        "feed_cheker": feed_res,
    }
    return res_dict


# многопоточная функция
def pool_data(rss_list):
    pool = ThreadPool(len(rss_list))
    try:
        feeds = pool.map(harvest_all, rss_list)
        pool.close()
        return feeds
    except Exception as ex:
        logging.exception(f"многопоточность сломалась")
        return []


def main():
    rss_list = [
        "https://feed1.xml",
        "https://feed2.xml",
        "https://feed3.xml",
    ]
    feeds = pool_data(rss_list)
    for item in feeds:
        if item["feed_cheker"]["status"]:
            lenta = feedparser.parse(item["response"]["response"].text)
            for titles in lenta["entries"]:
                print(titles["title"])


if __name__ == "__main__":
    main()
