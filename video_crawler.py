import psycopg2
import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

driver1 = webdriver.Firefox()
conn = psycopg2.connect(database="youtube_db", user="postgres", password="password")
cur = conn.cursor()


def get_video_data():
    try:
        cur.execute("SELECT * from core_data")
        curserdata = cur.fetchall()
        for one_entry in curserdata:
            try:
                cid = one_entry[0]
                channel_name = one_entry[1]
                temp_url = one_entry[4]
                channel_url = temp_url + '/videos'
                driver1.get(channel_url)
                for i in range(1, 51):
                    block = driver1.find_element_by_xpath('/html/body/div[15]/div[2]/div[13]/div[' + str(i) + ']')
                    date = block.find_element_by_xpath('div[1]').text
                    title_tag = block.find_element_by_xpath('div[2]/a')
                    title = title_tag.text
                    title = (title).replace('\'', "\''")
                    link = title_tag.get_attribute('href')
                    views = block.find_element_by_xpath('div[3]').text
                    comment_count = block.find_element_by_xpath('div[6]/a').text
                    enter_data_in_db(cid, title, link, date, views, comment_count)
                conn.commit()
            except NoSuchElementException:
                print("element  not found")
    except Exception as e:
        print("unknown error", e)


def enter_data_in_db(cid, title, link, date, views, comment_count):
    cur.execute(
        "SELECT * FROM video_data WHERE cid='{0}' AND upload_date='{1}' AND video_name='{2}'".format(cid, date, title))
    check = cur.fetchone()
    if check is None:
        cur.execute(
            "INSERT INTO video_data (cid, video_name, video_url, upload_date, views_count, comment_count) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')".format(
                cid, title, link, date, views, comment_count))

    else:
        print("data already there")


get_video_data()
driver1.close()
conn.close()
