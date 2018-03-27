import json

import datetime

import psycopg2
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

#driver1 = webdriver.Firefox()
driver2 = webdriver.Firefox()
url = "https://socialblade.com/youtube/top/5000"
#driver1.get(url)
output_file = open('youtube_data_' + str(datetime.datetime.now().strftime('%H_%M_%S')) + '.json', 'w', encoding='utf-8')
final_data = []
conn = psycopg2.connect(database="youtube_db", user="postgres", password="password")
cur = conn.cursor()


def get_block():
    '''  for i in range(5, 505):
        try:
            block = driver1.find_element_by_xpath('/html/body/div[9]/div[2]/div[' + str(i) + ']')
            channel_name_tag = block.find_element_by_xpath('div[3]/a')
            print(channel_name_tag.text)
            get_more_data(channel_name_tag.text, channel_name_tag.get_attribute('href'))
        except NoSuchElementException:
            print("Error in page:-")
            driver1.refresh()
            try:
                block = driver1.find_element_by_xpath('/html/body/div[9]/div[2]/div[' + str(i) + ']')
                channel_name_tag = block.find_element_by_xpath('div[3]/a')
                print(channel_name_tag.text)
                get_more_data(channel_name_tag.text, channel_name_tag.get_attribute('href'))
            except Exception as e:
                print("Inner Unknown Error",e)
        except Exception as e:
            print("Outer Unknown Error",e)'''
    try:
        cur.execute("SELECT * from core_data")
        all_data=cur.fetchall()
        counter=1
        for one_data in all_data:
            if one_data[2] is None:
                channel_id=one_data[0]
                channel_name=one_data[1]
                print(channel_name)
                channel_url=one_data[4]
                get_more_data(channel_id,channel_name,channel_url)
            counter += 1
    except Exception as e:
        print("Outer Unknown Error", e)


def check_or_update_db(channelid):
    cur.execute("SELECT * from core_data where id='" + str(channelid) + "'")
    check_data = cur.fetchone()
    if check_data[2] is None:
        print("in if")
        for social_tags in driver2.find_elements_by_xpath('/html/body/div[9]/div[2]/div'):
            channelurl = social_tags.find_element_by_xpath('a').get_attribute('href')
        imgurl = (driver2.find_element_by_xpath('//*[@id="YouTubeUserTopInfoAvatar"]').get_attribute('src'))
        cur.execute(
            "UPDATE core_data SET channel_url = '{0}',channel_img_url='{1}' WHERE id='{2}'".format(
                channelurl, imgurl, channelid))
        conn.commit()


def get_more_data(channelid,cname, url):
    new_url = url + "/monthly"
    driver2.get(new_url)
    name = (cname).replace('\'', "")
    name = (name).lstrip()

    try:

        channeltype = driver2.find_element_by_xpath('//*[@id="youtube-user-page-channeltype"]').text
        for i in range(5, 35):
            block = driver2.find_element_by_xpath('/ html / body / div[16] / div / div[1] / div[' + str(i) + ']')
            date_tag = block.find_element_by_xpath('div[1]')
            subscribers_tag = block.find_element_by_xpath('div[3]/div[2]')
            subscribers = (subscribers_tag.text).replace(",", "")
            video_views_tag = block.find_element_by_xpath('div[4]/div[2]')
            video_views = (video_views_tag.text).replace(",", "")

            final_data.append({
                'channel_id': channelid,
                'channel_type': channeltype,
                'date': date_tag.text,
                'subscribers': subscribers,
                'video_views': video_views
            })
        check_or_update_db(channelid)

    except NoSuchElementException:
        print("in Except")
        try:
            otherlink_tag = driver2.find_element_by_xpath('/html/body/div[10]/div[2]/div/h2/a')
            url2 = otherlink_tag.get_attribute('href')
            print(url2)
            driver2.get(url2)
            driver2.implicitly_wait(5)
            cur.execute("UPDATE core_data SET social_url='{0}' WHERE id='{1}'".format(driver2.current_url,channelid))
            conn.commit()
            new_url = driver2.current_url + "/monthly"
            driver2.get(new_url)
            channeltype = driver2.find_element_by_xpath('//*[@id="youtube-user-page-channeltype"]').text
            for i in range(5, 35):
                block = driver2.find_element_by_xpath('/ html / body / div[15] / div / div[1] / div[' + str(i) + ']')
                date_tag = block.find_element_by_xpath('div[1]')
                subscribers_tag = block.find_element_by_xpath('div[3]/div[2]')
                subscribers = (subscribers_tag.text).replace(",", "")
                video_views_tag = block.find_element_by_xpath('div[4]/div[2]')
                video_views = (video_views_tag.text).replace(",", "")
                final_data.append({
                    'channel_id': channelid,
                    'channel_type': channeltype,
                    'date': date_tag.text,
                    'subscribers': subscribers,
                    'video_views': video_views
                })
            check_or_update_db(channelid)
        except Exception as e:
            print("inner unknown error",e)
    except Exception as e:
        print("outer unknown error",e)



def write():
    json.dump(final_data, output_file)


get_block()
write()
output_file.close()
#driver1.close()
driver2.close()
