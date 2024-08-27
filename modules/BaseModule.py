from abc import ABC, abstractmethod
from telnetlib import EC

from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class BaseModule(ABC):
    def __init__(self, domain):
        self.domain = domain
        self.driver = None

    @abstractmethod
    def get_videos(self, source):
        """
        Retrieve video URLs from the given source.
        :param source: URL or identifier of the video page.
        :return: List of video URLs.
        """
        pass

    @abstractmethod
    def get_db(self):
        """
        Crawl the database and retrieve all video metadata.
        :return: Dictionary with video metadata.
        """
        pass

    @staticmethod
    def download_video(video_url, save_path):
        """
        Download the video from the given URL.
        :param video_url: The URL of the video to download.
        :param save_path: The path where the video should be saved.
        :return: Path to the saved video file.
        """
        import requests
        response = requests.get(video_url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return save_path
        else:
            raise Exception(f"Failed to download video from {video_url}")

    def search_by_keyword(self, keyword, absolute=True):
        """
        Search for videos using the given keyword.
        :param keyword: Search keyword.
        :param absolute: Whether to use absolute URLs or relative paths.
        :return: Generator yielding dictionaries with video metadata.
        """
        if not self.driver:
            raise RuntimeError("WebDriver is not initialized. Call `init_driver` first.")

        search_url = self._build_search_url(keyword)
        self.driver.get(search_url)

        try:
            video_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.video-item'))
            )

            for element in video_elements:
                title = element.find_element(By.CSS_SELECTOR, 'h3.title').text.strip()
                video_url = element.find_element(By.CSS_SELECTOR, 'a.video-link').get_attribute('href')
                yield {title: video_url}

        except TimeoutException:
            print(f"Timeout while searching for keyword: {keyword}")
        except WebDriverException as e:
            print(f"WebDriver error while searching for keyword: {keyword} - {e}")
        except Exception as e:
            print(f"Error searching for keyword: {keyword} - {e}")

    def _build_search_url(self, keyword):
        """
        Build the search URL based on the keyword.
        :param keyword: Search keyword.
        :return: Constructed search URL.
        """
        base_url = self.domain
        # This example assumes a query parameter named 'search'
        return f"{base_url}/search?query={keyword}"

    def init_driver(self):
        """
        Initialize the Selenium WebDriver.
        """
        # Example implementation, adjust as necessary
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def close_driver(self):
        """
        Close the Selenium WebDriver.
        """
        if self.driver:
            self.driver.quit()
            self.driver = None
