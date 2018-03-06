import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

driver1 = webdriver.Firefox()
driver2 = webdriver.Firefox()
url = "https://socialblade.com/youtube/top/5000"
driver1.get(url)
output_file = open('youtube_data.json', 'w', encoding='utf-8')
final_data = []


def get_block():
    for i in range(5, 100):
        try:
            block = driver1.find_element_by_xpath('/html/body/div[10]/div[2]/div[' + str(i) + ']')
            channel_name_tag = block.find_element_by_xpath('div[3]/a')
            print(channel_name_tag.text)
            get_more_data(channel_name_tag.text, channel_name_tag.get_attribute('href'))
        except NoSuchElementException:
            print("Error in page:-")
            driver1.refresh()
            try:
                block = driver1.find_element_by_xpath('/html/body/div[10]/div[2]/div[' + str(i) + ']')
                channel_name_tag = block.find_element_by_xpath('div[3]/a')
                print(channel_name_tag.text)
                get_more_data(channel_name_tag.text, channel_name_tag.get_attribute('href'))
            except:
                print("Unknown Error")


def get_more_data(name, url):
    new_url = url + "/monthly"
    driver2.get(new_url)
    try:
        for i in range(5, 35):
            block = driver2.find_element_by_xpath('/ html / body / div[16] / div / div[1] / div[' + str(i) + ']')
            date_tag = block.find_element_by_xpath('div[1]')
            subscribers_tag = block.find_element_by_xpath('div[3]/div[2]')
            subscribers = (subscribers_tag.text).replace(",", "")
            video_views_tag = block.find_element_by_xpath('div[4]/div[2]')
            video_views = (video_views_tag.text).replace(",", "")
            final_data.append({
                'channel_name': name,
                'date': date_tag.text,
                'subscribers': subscribers,
                'video_views': video_views
            })
    except NoSuchElementException:
        print("in Except")
        try:
            otherlink_tag = driver2.find_element_by_xpath('/html/body/div[10]/div[2]/div/h2/a')
            url2 = otherlink_tag.get_attribute('href')
            print(url2)
            driver2.get(url2)
            new_url = driver2.current_url + "/monthly"
            driver2.get(new_url)
            for i in range(5, 35):
                block = driver2.find_element_by_xpath('/ html / body / div[16] / div / div[1] / div[' + str(i) + ']')
                date_tag = block.find_element_by_xpath('div[1]')
                subscribers_tag = block.find_element_by_xpath('div[3]/div[2]')
                subscribers = (subscribers_tag.text).replace(",", "")
                video_views_tag = block.find_element_by_xpath('div[4]/div[2]')
                video_views = (video_views_tag.text).replace(",", "")
                final_data.append({
                    'channel_name': name,
                    'date': date_tag.text,
                    'subscribers': subscribers,
                    'video_views': video_views
                })
        except:
            print("unknown error")


def write():
    json.dump(final_data, output_file)


get_block()
write()
output_file.close()
driver1.close()
driver2.close()
