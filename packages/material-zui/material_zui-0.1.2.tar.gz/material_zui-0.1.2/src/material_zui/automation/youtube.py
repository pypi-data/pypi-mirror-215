import os
from pyparsing import Any
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from datetime import datetime
from pytube import YouTube, Playlist
from pytube.exceptions import VideoUnavailable

from material_zui.automation.type import Video, Videos
from material_zui.automation.Constant import Constant
from material_zui.selenium import Zui_Selenium_Chrome
from material_zui.file import get_files_info, write_json, load_json_array, ZuiFile
from material_zui.date_time import add_days
from material_zui.list import list_range, map_to, filter_to
from material_zui.string import list_match, trim_space, remove_special_characters
from material_zui.utility import pipe, pipe_list


class Zui_Youtube(Zui_Selenium_Chrome):
    '''
    - Tested on `Ubuntu` platform, it might work on `Linux` (or `MacOS`), not sure for `Window`
    - Upload video use `Selenium` to automation
        - Automation base on the system UI, so it can be out updated in the future due to the update UI
    - Download video base on `pytube`, detail here: https://pytube.io/en/latest/index.html
    '''

    def __go_to_content_page(self) -> None:
        self.driver.find_element(
            By.XPATH, '//*[@id="menu-paper-icon-item-1"]').click()

    def get_account_info(self) -> str:
        '''
        Example result:
        ```txt
        Google Account: {Account name}
        ({username}@gmail.com)
        ```
        '''
        self.driver.get("https://google.com")
        account_element = self.driver.find_element(By.CLASS_NAME, "gb_3a")
        return account_element.get_attribute("aria-label")

    def upload_video(self, video: Video) -> None:
        '''
        Upload single video to YouTube
        @is_publish: direct publish
        @schedule: format `MM/DD/YYYY, HH:MM`
        '''
        title = video['title']
        description = video['description']
        path = video['path']
        is_publish = video['is_publish']
        playlist = video.get('playlist')
        tags = video.get('tags')
        schedule = video.get('schedule')

        print('Access youtube studio')
        self.driver.get("https://studio.youtube.com")

        # click upload
        self.delay()
        upload_button = self.driver.find_element(
            By.XPATH, '//*[@id="upload-icon"]')
        upload_button.click()

        # import video
        print('Importing video')
        self.delay()
        file_input = self.driver.find_element(
            By.XPATH, '//*[@id="content"]/input')
        abs_path = os.path.abspath(str(path))
        file_input.send_keys(abs_path)

        # set title
        print('Setting title:', title)
        sleep(7)
        title_element = self.driver.find_element(
            By.XPATH, '//*[@id="textbox"]')
        title_element.send_keys(Keys.CONTROL + 'a')
        title_element.send_keys(Keys.BACKSPACE)
        title_element.send_keys(title)

        # set description
        print('Setting description:', description)
        self.delay()
        description_element = self.driver.find_element(
            By.XPATH, '//*/ytcp-video-description/div/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div')
        description_element.send_keys(description)

        # set playlist
        self.delay()
        if playlist:
            print('Setting playlist:', playlist)
            # open playlist
            self.driver.find_element(
                By.CLASS_NAME, Constant.PL_DROPDOWN_CLASS).click()

            # load playlist
            sleep(5)
            playlist_items_container = self.driver.find_element(
                By.ID, Constant.PL_ITEMS_CONTAINER_ID)
            playlist_item = self.safe_find_element(
                By.XPATH, Constant.PL_ITEM_CONTAINER.format(playlist), playlist_items_container)
            sleep(Constant.USER_WAITING_TIME)
            if playlist_item:
                # choose playlist existed
                playlist_item.click()
            else:
                # new playlist
                self.driver.find_element(
                    By.XPATH, '//*[@id="dialog"]/div[2]/div/ytcp-button').click()
                self.delay()
                self.driver.find_element(
                    By.XPATH, '//*/tp-yt-paper-listbox/tp-yt-paper-item[1]').click()

                # edit playlist title
                self.delay()
                self.driver.find_element(
                    By.XPATH, "//*/ytcp-playlist-metadata-editor/div/div[1]/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div").send_keys(playlist)

                # create new playlist
                sleep(Constant.USER_WAITING_TIME)
                self.driver.find_element(
                    By.XPATH, '//*[@id="create-button"]').click()

            # save playist
            sleep(Constant.USER_WAITING_TIME)
            done_button = self.driver.find_element(
                By.CLASS_NAME, Constant.PL_DONE_BUTTON_CLASS)
            done_button.click()

        # select kid option
        self.delay()
        self.driver.find_element(
            By.XPATH, '//*[@id="audience"]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]').click()

        # set tags
        if tags and len(tags):
            print('Setting tags:', tags)

            # open advance option
            self.delay()
            self.driver.find_element(
                By.XPATH, '//*[@id="toggle-button"]/div').click()

            # click tags
            self.delay()
            tags_element = self.driver.find_element(
                By.XPATH, '//*/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[4]/ytcp-form-input-container/div[1]/div/ytcp-free-text-chip-bar/ytcp-chip-bar/div/input')
            tags_element.click()

            # add tags
            for tag in tags:
                tags_element.send_keys(tag)
                tags_element.send_keys(Keys.ENTER)

        # click next 3 time
        self.delay()
        next_button = self.driver.find_element(
            By.XPATH, '//*[@id="next-button"]')
        for _ in range(3):
            next_button.click()
            self.delay(5)

        # publish or schedule
        self.delay()
        if is_publish:  # click public to direct publish
            print('Setting publish')
            self.driver.find_element(
                By.XPATH, '//*[@id="privacy-radios"]/tp-yt-paper-radio-button[3]').click()
        elif schedule:  # schedule
            print('Setting schedule:', schedule)
            date_time = datetime.strptime(schedule, "%m/%d/%Y, %H:%M")
            self.driver.find_element(
                By.ID, Constant.SCHEDULE_CONTAINER_ID).click()
            self.driver.find_element(By.ID, Constant.SCHEDULE_DATE_ID).click()

            self.delay()
            self.driver.find_element(
                By.XPATH, Constant.SCHEDULE_DATE_TEXTBOX).clear()
            self.driver.find_element(By.XPATH, Constant.SCHEDULE_DATE_TEXTBOX).send_keys(
                datetime.strftime(date_time, "%b %e, %Y"))
            self.driver.find_element(
                By.XPATH, Constant.SCHEDULE_DATE_TEXTBOX).send_keys(Keys.ENTER)
            self.driver.find_element(By.XPATH, Constant.SCHEDULE_TIME).click()
            self.driver.find_element(By.XPATH, Constant.SCHEDULE_TIME).clear()
            self.driver.find_element(By.XPATH, Constant.SCHEDULE_TIME).send_keys(
                datetime.strftime(date_time, "%H:%M"))
            self.driver.find_element(
                By.XPATH, Constant.SCHEDULE_TIME).send_keys(Keys.ENTER)

        # submit
        # 1. click done (for private video)
        # 2. click publish (for publish video)
        # 3. click schedule (for schedule video)
        print('Submit video')
        self.delay()
        self.driver.find_element(
            By.XPATH, '//*[@id="done-button"]').click()
        self.delay(10)

        video_processing_element = self.safe_find_element(
            By.XPATH, '//*[@id="close-button"]/div')
        if video_processing_element:
            video_processing_element.click()

    def upload_videos(self, videos: Videos) -> None:
        '''
        Upload multiple videos to YouTube
        '''
        for index, video in enumerate(videos):
            self.upload_video(video)
            self.delay()
            print('Uploaded video', index+1)
        self.__go_to_content_page()

    def upload_videos_from_file_info(self, video_path: str, json_file_path: str) -> None:
        '''
        Upload multiple videos from json data file
        @video_path: video path including video to publish
        @json_file_path: json file path including video info
        '''
        def map_item(video: dict[Any, Any], _: int) -> Video:  # type: ignore
            file_name = str(video['file_name'])
            path = f'{video_path}/{file_name}'
            return {
                'title': video['title'],
                'description': video['description'],
                'path': path,
                'playlist': video.get('playlist'),
                'tags': video.get('tags'),
                'is_publish': video.get('is_publish') or False,
                'schedule': video.get('schedule')
            }
        items = load_json_array(json_file_path)
        videos: Videos = map_to(items, map_item)
        self.upload_videos(videos)

    def download_video(self, url: str, video_output_path: str) -> None:
        '''
        If error network, try again with VPN connected
        '''
        try:
            youtube = YouTube(url)
            video_stream = youtube.streams.get_highest_resolution()
        except VideoUnavailable:
            print(f'Video {url} is unavaialable, skipping.')
        else:
            print("Downloading:", youtube.title)
            if video_stream:
                video_stream.download(video_output_path)
                print("Download complete")

    # def download_video2(self, url: str, video_output_path: str) -> None:
    #     '''
    #     If error network, try again with VPN connected
    #     '''
    #     # video_list = ['https://www.youtube.com/watch?v=xTN2ktqKSBk',
    #     #               'https://www.youtube.com/watch?v=w5Ji-VEnbmc']
    #     # Looping through the list
    #     try:
    #         yt = YouTube(url)
    #         print('Downloading Link: ')

    #         # filters out all the files with "mp4" extension
    #         stream = yt.streams.filter(res="360p").first()
    #         if stream:
    #             # print('Downloading video: ' + yt.streams[0].title)
    #             stream.download(video_output_path)
    #         print('Task Completed!')
    #     except:
    #         print("Connection Error")

    def download_videos(self, urls: list[str], video_output_path: str) -> None:
        '''
        If error network, try again with VPN connected
        '''
        for url in urls:
            self.download_video(url, video_output_path)

    def get_playlist_videos(self, playlist_url: str) -> list[str]:
        playlist = Playlist(playlist_url)
        return list(playlist.video_urls)

    def download_playlist_video(self, playlist_url: str, video_output_path: str, limit: int = 0, start_index: int = 0) -> None:
        '''
        If error network, try again with VPN connected
        '''
        # playlist = Playlist(playlist_url)
        # urls = list(playlist.video_urls)
        urls = self.get_playlist_videos(playlist_url)
        download_urls: list[str] = list_range(urls, limit, start_index)
        self.download_videos(download_urls, video_output_path)

    def video_title_to_json(self, directory_path: str, json_path: str, playlist: str, start_day_schedule: str = "", time_schedules: list[str] = ["11:00", "19:00"]) -> None:
        filenames = get_files_info(directory_path, 'mp4')

        def handle(file: ZuiFile, index: int) -> dict[str, Any]:
            index_schedule = index % len(time_schedules)
            diff_day = int(index/len(time_schedules))

            file_name = file['file_name']
            name = file['name']
            title = pipe(
                remove_special_characters,
                trim_space
            )(name)

            raw_tags = pipe_list(remove_special_characters, trim_space)(
                list_match('(#)([^ ]+)', 2)(name.strip('#')))
            tags = filter_to(raw_tags, lambda tag, _: len(tag) > 1)

            start_day = datetime.strptime(
                start_day_schedule, "%m/%d/%Y") if start_day_schedule else datetime.now()
            day_schedule = add_days(start_day, diff_day)
            time_schedule = time_schedules[index_schedule].split(
                ':')
            day_schedule = day_schedule.replace(
                hour=int(time_schedule[0]), minute=int(time_schedule[1]))
            schedule = datetime.strftime(day_schedule, "%m/%d/%Y, %H:%M")

            result: dict[str, Any] = {
                'file_name': file_name,
                "title": title,
                "description": title,
                "playlist": playlist,
                "tags": tags,
                "is_publish": False,
                "schedule": schedule
            }
            return result
        file_info = map_to(filenames, handle)
        write_json(file_info, json_path)

    # def get_video_info(self, url: str):
    #     youtube = YouTube(url)
    #     video_stream = youtube.streams.get_highest_resolution()
    #     print("Downloading video:", youtube.title,
    #           youtube.description, youtube.thumbnail_url)
    #     print(youtube.captions['en'])
    #     print(youtube.channel_url)
    #     print(youtube.channel_id)
    #     print(youtube.keywords)
    #     print(youtube.rating)
        # print(youtube.vid_info)
