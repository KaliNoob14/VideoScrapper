from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules.BaseModule import BaseModule  # Import adjusted for the modules directory

class Animewatchto(BaseModule):
    def __init__(self):
        super().__init__('https://aniwatchtv.to/')

    def get_videos(self, source):
        """
        Retrieve video URLs from the given source.
        :param source: URL of the video page.
        :return: List of video URLs.
        """
        video_urls = []
        self.driver.get(source)
        try:
            # Wait for the video elements to load
            video_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.video-link'))
            )
            for element in video_elements:
                video_url = element.get_attribute('href')
                video_urls.append(video_url)
        except Exception as e:
            print(f"Error retrieving videos: {e}")
        return video_urls

    def get_db(self):
        """
        Crawl the database and retrieve all video metadata.
        :return: Dictionary with video metadata.
        """
        video_metadata = {}
        self.driver.get(self.domain)
        try:
            # Wait for the video elements to load
            video_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.video-item'))
            )
            for element in video_elements:
                title = element.find_element(By.CSS_SELECTOR, 'h3.title').text.strip()
                video_url = element.find_element(By.CSS_SELECTOR, 'a.video-link').get_attribute('href')
                video_metadata[title] = video_url
        except Exception as e:
            print(f"Error retrieving video metadata: {e}")
        return video_metadata

    def search_by_keyword(self, keyword, absolute=None):
        """
        Search for videos by keyword.
        :param keyword: Search keyword.
        :param absolute: Optional URL to use instead of the default search URL.
        :return: Dictionary with video metadata based on the search results.
        """
        search_url = f"{self.domain}/search?q={keyword}" if not absolute else absolute
        self.driver.get(search_url)
        search_results = {}
        try:
            # Wait for the search results to load
            video_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.video-item'))
            )
            for element in video_elements:
                title = element.find_element(By.CSS_SELECTOR, 'h3.title').text.strip()
                video_url = element.find_element(By.CSS_SELECTOR, 'a.video-link').get_attribute('href')
                search_results[title] = video_url
        except Exception as e:
            print(f"Error during search: {e}")
        return search_results

    def close(self):
        """
        Close the Selenium WebDriver.
        """
        self.close_driver()
