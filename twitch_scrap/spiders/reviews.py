from time import sleep

import scrapy
from database.service import save_to_database, TableNamesMap
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class ReviewsSpider(scrapy.Spider):
    name = "reviews"
    allowed_domains = ["web-scraping.dev"]
    # start_urls = ["https://web-scraping.dev"]

    def start_requests(self):
        url = "https://web-scraping.dev/testimonials"
        yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        # with open('screenshot.png', 'wb') as image:
        #     image.write(response.meta['screenshot'])

        # driver = response.request.meta["driver"]
        # # adjust the ChromeDriver viewport
        # driver.set_window_size(1920, 1080)
        # driver.save_screenshot("screenshot.png")
        reviews = response.css("div.testimonial")
        for review in reviews:
            yield {
                "rate": len(review.css("span.rating > svg").getall()),
                "text": review.css("p.text::text").get()
            }


class DropsSpider(scrapy.Spider):
    name = "drops"
    allowed_domains = ["twitch.tv", "www.google.com.ua"]
    open_campaign_index = 4
    closed_campaign_index = 6
    data_extract_config = {'open_reward_campaigns': {'word_separator': 'Drops Inventory'},
                           'open_drop_campaigns': {'word_separator': '(Required)', 'index_increment': 2},
                           'closed_drop_campaigns': {'word_separator': '(Required)', 'index_increment': 2}}
    block_additional_information = {'open_drop_campaigns': {'status': 'open'},
                                    'closed_drop_campaigns': {'status': 'closed'}}

    def start_requests(self):
        url = "https://www.twitch.tv/drops/campaigns"
        yield SeleniumRequest(url=url, callback=self.parse)

    def login(self):
        pass
        # from selenium.webdriver.common.action_chains import ActionChains

        # driver = response.request.meta["driver"]
        # driver.implicitly_wait(10)
        # sleep(10)
        # driver.set_window_size(1920, 1080)
        # driver.save_screenshot("screenshot.png")

        # # adjust the ChromeDriver viewport

        # print('Waiting')
        # sleep(5)
        # print('Start login')
        # username_button = driver.find_element(By.ID, "login-username")
        # username_button.send_keys("GermaNika21")
        #
        # password_button = driver.find_element(By.ID, "password-input")
        # password_button.send_keys(">63@\"aMCFk_8gXs")
        #
        # driver.implicitly_wait(10)
        #
        # driver.set_window_size(1920, 1080)
        # driver.save_screenshot("screenshot1.png")
        # confirm_button = driver.find_element(By.CSS_SELECTOR, "[data-a-target='passport-login-button']")
        # print(confirm_button)
        # click the login submit button
        # confirm_button.click()

        # sleep(10)
        # driver.set_window_size(1920, 1080)
        # driver.save_screenshot("screenshot2.png")
        # ActionChains(driver).move_to_element(confirm_button).click(confirm_button).perform()
        # sleep(150)
        # print(response.body)

    def extract_block_data(self, block_name: str, data: list):
        separated_data = []
        word_separator = self.data_extract_config.get(block_name).get('word_separator')
        index_increment = self.data_extract_config.get(block_name).get('index_increment', 1)

        while word_separator in data:
            word_index = data.index(word_separator)
            separated_data.append(data[0:word_index + index_increment])
            data = [value for index, value in enumerate(data) if index not in range(0, word_index + index_increment)]

        separated_data = [value[0:4] for value in separated_data]

        separated_data = list(map(lambda data_list: ({'game': data_list[0], 'company': data_list[1],
                                                      'campaign_dates': data_list[2],
                                                      'campaign_name': data_list[3]}), separated_data))

        updated_data = self.update_block_with_additional_info(block_name, separated_data)
        return updated_data

    def update_block_with_additional_info(self, block_name: str, data_block: list):
        additional_information = self.block_additional_information.get(block_name)
        updated_block = [{**item, **additional_information} for item in data_block]
        return updated_block

    def process_data(self, unprocessed_data: dict):
        extracted_data = {}
        for block_name, data in unprocessed_data.items():
            extracted_data.update({block_name: self.extract_block_data(data=data, block_name=block_name)})

        return extracted_data

    def save_data(self, data_to_save: dict or list):
        save_to_database(TableNamesMap.campaigns.value, data_to_save)

    def parse(self, response):
        drop_blocks = response.xpath("//div[@class='Layout-sc-1xcs6mc-0 jmLWIr drops-root__content']/div")

        text_blocks = []
        for block in drop_blocks:
            text_blocks.append(block.xpath('./div//text()').extract())

        # drops_data = {'open_reward_campaigns': text_blocks[2], 'open_drop_campaigns': text_blocks[4],
        #               'closed_drop_campaigns': text_blocks[6]}
        # temporary exclude reward campaign from data processing
        drops_data = {'open_drop_campaigns': text_blocks[self.open_campaign_index],
                      'closed_drop_campaigns': text_blocks[self.closed_campaign_index]}
        processed_data = self.process_data(drops_data)

        for data_block in processed_data.values():
            self.save_data(data_block)

        return processed_data
