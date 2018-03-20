import psycopg2
import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

driver1 = webdriver.Firefox()
url = "https://socialblade.com/youtube/top/5000"
driver1.get(url)
conn = psycopg2.connect(database="youtube_db", user="postgres", password="password")
cur = conn.cursor()


def get_block():
    for i in range(5, 5005):
        try:
            block = driver1.find_element_by_xpath('/html/body/div[9]/div[2]/div[' + str(i) + ']')
            link_tag = block.find_element_by_xpath('div[3]/a')
            url = link_tag.get_attribute('href')
            url = (url).replace('\'', "\''")
            name = (link_tag.text).replace('\'', "\''")
            name = (name).lstrip()
            uploads_tag = block.find_element_by_xpath('div[4]/span')
            uploads = (uploads_tag.text).replace(",", "")
            subscribers_tag = block.find_element_by_xpath('div[5]/span')
            subscribers = (subscribers_tag.text).replace(",", "")
            video_views_tag = block.find_element_by_xpath('div[6]/span')
            video_views = (video_views_tag.text).replace(",", "")
            cur.execute("SELECT * from core_data where channel_name='" + str(name) + "'")
            check_data = cur.fetchone()
            date=str(datetime.datetime.now().date())
            if check_data is None:
                print(name)
                enter_data_in_core_table(name, url)
                cur.execute("SELECT * from core_data where channel_name='" + str(name) + "'")
                check_data = cur.fetchone()
                id = str(check_data[0])
                enter_data_in_channeldata_table(id, date, video_views, subscribers)
            else:
                id = str(check_data[0])
                enter_data_in_channeldata_table(id,date,video_views,subscribers)
        except StaleElementReferenceException:
            print("StaleElementReferenceException retyring...")
            driver1.refresh()
            try:
                block = driver1.find_element_by_xpath('/html/body/div[9]/div[2]/div[' + str(i) + ']')
                link_tag = block.find_element_by_xpath('div[3]/a')
                url = link_tag.get_attribute('href')
                url = (url).replace('\'', "\''")
                name = (link_tag.text).replace('\'', "\''")
                name = (name).lstrip()
                uploads_tag = block.find_element_by_xpath('div[4]/span')
                uploads = (uploads_tag.text).replace(",", "")
                subscribers_tag = block.find_element_by_xpath('div[5]/span')
                subscribers = (subscribers_tag.text).replace(",", "")
                video_views_tag = block.find_element_by_xpath('div[6]/span')
                video_views = (video_views_tag.text).replace(",", "")
                cur.execute("SELECT * from core_data where channel_name='" + str(name) + "'")
                check_data = cur.fetchone()
                date = str(datetime.datetime.now().date())
                if check_data is None:
                    print(name)
                    enter_data_in_core_table(name, url)
                    cur.execute("SELECT * from core_data where channel_name='" + str(name) + "'")
                    check_data = cur.fetchone()
                    id = str(check_data[0])
                    enter_data_in_channeldata_table(id, date, video_views, subscribers)
                else:
                    id = str(check_data[0])
                    enter_data_in_channeldata_table(id, date, video_views, subscribers)
            except:
                print("unknown error")
        except:
            print("unknown error")

def enter_data_in_core_table(name, social_url):
    cur.execute("INSERT INTO core_data (channel_name,social_url) VALUES ('{0}','{1}')".format(name, social_url))
    conn.commit()

def enter_data_in_channeldata_table(id,date,view_count,subscriber_count):
    cur.execute("SELECT * FROM channel_data WHERE date='{0}' AND id_from_core_data='{1}'".format(date,id))
    check=cur.fetchone()
    if check is None:
        cur.execute("INSERT INTO channel_data (id_from_core_data, date, view_count, subscribers_count) VALUES ('{0}','{1}','{2}','{3}')".format(id,date,view_count,subscriber_count))
        conn.commit()
        print("data added")
    else:
        print("data already there")
get_block()

driver1.close()
