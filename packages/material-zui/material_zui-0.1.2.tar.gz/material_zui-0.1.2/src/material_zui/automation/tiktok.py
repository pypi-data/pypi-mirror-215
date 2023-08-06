from bs4 import BeautifulSoup, ResultSet
import requests
from selenium.webdriver.common.keys import Keys

from material_zui.utility.common import pipe

from .data import MAX_DAY_SCHEDULE, SCROLL_HOURS
from material_zui.date_time import to_date_time, now
from material_zui.list import is_last_index
from material_zui.file import download, read_file_to_list, write_to_last
from material_zui.list.common import get, get_diff, list_range, map_to
from material_zui.selenium import Zui_Selenium_Chrome
from material_zui.string import list_match


class Zui_Tiktok(Zui_Selenium_Chrome):
    '''
    Base on repo: https://github.com/codewithvincent1/tiktokVideoScraper
    '''

    def set_browser_info(self, cookies: dict[str, str] = {}, headers: dict[str, str] = {}) -> None:
        '''
        Use for download tiktok video, by pass if you don't use this function
        1. Access https://ssstik.io to get `cUrl` request
        2. Access https://curlconverter.com to convert that `cUrl` to `Python request`, then only need to use `cookies` and `headers`
        '''
        self.cookies: dict[str, str] = cookies
        self.headers: dict[str, str] = headers

    def get_video_urls_from_channel(self, channel_url: str, limit: int = 0, start_index: int = 0) -> list[str]:
        '''
        Get all video url of channel
        @limit: number of url to get
        @start_index: position index to start, default from `0`
        '''
        videos: ResultSet
        i = 1
        end_index = start_index+limit

        print("Open channel", channel_url)
        self.driver.get(channel_url)

        print("Geting video url")
        self.delay()
        screen_height = self.driver.execute_script(
            "return window.screen.height;")
        if end_index != 0:  # incase exist limit param
            while True:
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                videos = soup.find_all(
                    "div", {"class": "tiktok-yz6ijl-DivWrapper"})
                scroll_height = self.driver.execute_script(
                    "return document.body.scrollHeight;")
                if (screen_height) * i > scroll_height or len(videos) >= end_index:
                    break
                self.driver.execute_script(
                    "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
                i += 1
                self.delay()
        else:  # get all channel video url
            while True:
                self.driver.execute_script(
                    "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
                i += 1
                self.delay()
                scroll_height = self.driver.execute_script(
                    "return document.body.scrollHeight;")
                if (screen_height) * i > scroll_height:
                    break

            self.delay()
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            videos = soup.find_all(
                "div", {"class": "tiktok-yz6ijl-DivWrapper"})

        urls = list(map(lambda video: video.a["href"], videos))
        # urls = map_to(videos, lambda video, _: video.a["href"])
        return urls[start_index:end_index] if end_index != 0 else urls

    def get_video_urls(self, url: str, step_scroll: int = 1, limit: int = 0, start_index: int = 0) -> list[str]:
        print("Access url", url)
        self.driver.get(url)
        self.delay()

        for index in range(step_scroll):
            print(index+1, "Scrolling to", self.scroll_height)
            self.scroll_to_end()
            self.delay()

        urls = self.get_urls("tiktok-bbkab3-DivContainer")
        download_urls = list_range(urls, limit, start_index)
        return download_urls

    def download_video(self, url: str, output_directory_path: str) -> None:
        '''
        Use https://ssstik.io to download tiktok video
        '''
        params = {'url': 'dl'}
        data = {
            'id': url,
            'locale': 'en',
            'tt': '',  # NOTE: This value gets changed, please use the value that you get when you copy the curl command from the network console
        }

        print(f"Getting the download link: {url}")
        response = requests.post('https://ssstik.io/abc', params=params,
                                 cookies=self.cookies, headers=self.headers, data=data)
        download_soup = BeautifulSoup(response.text, "html.parser")
        download_link: str = download_soup.a["href"]  # type: ignore
        video_title: str = download_soup.p.getText().strip()  # type: ignore
        safe_video_title = video_title.replace(
            "/", "-").replace('"', "").replace("'", "")

        print("Saving the video")
        self.delay()
        download(download_link,
                 f"{output_directory_path}/{safe_video_title}.mp4")

    def download_videos(self, urls: list[str], output_directory_path: str, delay_each_video: int = 10) -> None:
        '''
        Download video by list url
        @urls: list video url to download
        @output_directory_path: path to save all video downloaded
        @delay_each_video: time delay each video (seconds)
        '''
        print(f"Downloading {len(urls)} videos")
        for index, url in enumerate(urls):
            self.download_video(
                url=url, output_directory_path=output_directory_path)
            print('Downloaded video', index+1)
            if not is_last_index(urls, index):
                self.delay(delay_each_video)

    def download_channel_videos(self, channel_url: str, output_directory_path: str, limit: int = 0, start_index: int = 0, delay_each_video: int = 10) -> None:
        '''
        Use to download all channel video
        @output_directory_path: path to save all video downloaded
        @limit: number of url to get
        @start_index: position index to start, default from `0`
        '''
        urls: list[str] = self.get_video_urls_from_channel(
            channel_url=channel_url, limit=limit, start_index=start_index)
        self.download_videos(urls, output_directory_path, delay_each_video)

    def load_diff_urls(self, file_path_urls: str, input_urls: list[str]) -> list[str]:
        saved_urls = read_file_to_list(file_path_urls)
        diff_urls = get_diff(input_urls, saved_urls)
        print("New urls", len(diff_urls))
        print("Duplicate urls", len(input_urls)-len(diff_urls))
        write_to_last(file_path_urls, '\n---New urls---\n' +
                      "\n".join(diff_urls))
        return diff_urls

    def upload_video(self, caption: str, video_path: str, schedule: str = '') -> None:
        upload_url = 'https://www.tiktok.com/upload'
        print("Access url", upload_url)
        self.driver.get(upload_url)
        self.delay()

        print('Importing video')
        self.switch_to_frame('//*[@id="main"]/div[2]/div/iframe')
        self.upload_file(
            '//*[@id="root"]/div/div/div/div/div/div/div/input', video_path)
        self.delay(6)

        print('Setting caption:', caption)
        title: str = pipe(
            list_match('([^#]+)#', 1),
            get(0, caption)  # type: ignore
        )(caption)
        tags = list_match('#[^ ]+')(caption)
        print(tags, title)
        title_element = self.send_keys(
            '//*[@id="root"]/div/div/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div/div/div/div/div/div', title)
        self.delay()
        for tag in tags:
            title_element.send_keys(tag)
            self.delay()
            title_element.send_keys(Keys.SPACE)

        if schedule:
            date_time = to_date_time(schedule)
            hour = date_time.hour
            minute = date_time.minute
            day = date_time.day
            is_selected_day = False
            valid_date_elements = []
            print('Setting schedule:', date_time)

            print('Enable schedule')
            self.click(
                '//*[@id="root"]/div/div/div/div[2]/div[2]/div[2]/div[4]/div/div/div[2]')
            self.delay()

            print('Opening time popup')
            self.click(
                '//*[@id="root"]/div/div/div/div[2]/div[2]/div[2]/div[4]/div/div[2]/div[2]')
            self.delay()

            print('Setting minute:', minute)
            self.find_element_by_xpath(
                '//*[@id="root"]/div/div/div/div/div[2]/div[2]/div[4]/div/div[2]/div[2]/div/div[2]')

            print('Setting hour:', hour)
            scroll_hour_query = '//*[@id="root"]/div/div/div/div[2]/div[2]/div[2]/div[4]/div/div[2]/div[2]/div/div[2]/div/div[{}]'
            for scroll_hour in reversed(SCROLL_HOURS):
                scroll_hour_element = self.safe_click(
                    scroll_hour_query.format(scroll_hour+1))
                if scroll_hour_element:
                    self.delay()
            for scroll_hour in SCROLL_HOURS:
                if hour > scroll_hour:
                    self.safe_click(scroll_hour_query.format(scroll_hour+1))
                    self.delay()
            self.safe_click(scroll_hour_query.format(hour+1))

            print('Opening day popup')
            self.click(
                '//*[@id="root"]/div/div/div/div[2]/div[2]/div[2]/div[4]/div/div[2]/div[1]/span')
            self.delay()

            def select_day() -> None:
                nonlocal is_selected_day
                nonlocal valid_date_elements
                valid_date_elements = self.find_elements_by_class('valid')
                for valid_date_element in valid_date_elements:
                    day_valid = int(valid_date_element.text)
                    if day == day_valid:
                        is_selected_day = True
                        valid_date_element.click()
                        break

            print('Setting day', day)
            select_day()
            if (not is_selected_day and len(valid_date_elements) < MAX_DAY_SCHEDULE):
                print('Switching to next month')
                self.click(
                    '//*[@id="root"]/div/div/div/div[2]/div[2]/div[2]/div[4]/div/div[2]/div[1]/div/div[1]/span[3]/svg')
                select_day()

        print('Check copyright')
        self.click(
            '//*[@id="root"]/div/div/div/div[2]/div[2]/div[2]/div[5]/div[2]')

        # print('Submitting')
        # self.click(
        #     '//*[@id="root"]/div/div/div/div[2]/div[2]/div[2]/div[7]/div[2]/button')

    def upload_videos(self, caption: str, video_path: str, schedule: str = '') -> None:
        print()
