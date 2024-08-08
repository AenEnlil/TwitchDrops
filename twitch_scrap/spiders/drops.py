from time import sleep

import scrapy
from database.core import db_session
from database.service import save_to_database, TableNamesMap
from datetime import datetime
from scrapy_selenium import SeleniumRequest


class DropsSpider(scrapy.Spider):
    name = "drops"
    allowed_domains = ["twitch.tv", "www.google.com.ua"]
    open_campaigns_index, closed_campaign_index = None, None
    data_extract_config = {'open_reward_campaigns': {'word_separator': 'Drops Inventory'},
                           'open_drop_campaigns': {'word_separator': '(Required)', 'index_increment': 2},
                           'closed_drop_campaigns': {'word_separator': '(Required)', 'index_increment': 2}}
    block_additional_information = {'open_drop_campaigns': {'status': 'open'},
                                    'closed_drop_campaigns': {'status': 'closed'}}
    excluded_words = {'company': ['Use', "Watch to Redeem"]}

    def start_requests(self):
        url = "https://www.twitch.tv/drops/campaigns"
        yield SeleniumRequest(url=url, callback=self.parse)

    def set_campaigns_index(self, text_blocks):
        # TODO: add reward campaigns
        for index, text in enumerate(text_blocks):
            if 'Open Drop Campaigns' in text:
                self.open_campaigns_index = index+1

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

    def split_campaign_dates(self, data_item: dict):
        campaign_dates = data_item.pop('campaign_dates')
        gmt_index = campaign_dates.find('GMT')
        current_year = datetime.now().year

        string_without_gmt = campaign_dates[:gmt_index]
        split_string = string_without_gmt.split('-')

        start_date = datetime.strptime(split_string[0].strip(), '%a, %b %d, %I:%M %p')
        final_start_date = start_date.replace(year=current_year)

        end_date = datetime.strptime(split_string[1].strip(), '%a, %b %d, %I:%M %p')
        if start_date.month > end_date.month:
            current_year += 1
        final_end_date = end_date.replace(year=current_year)

        data_item.update({'start_date': final_start_date, 'end_date': final_end_date})

        return data_item


    def extract_game_data(self, data: list):
        game_data = []

        for game in data:
            extracted_data = []
            extracted_data.extend(game[0:4])
            reward_block_start_index, reward_block_end_index = game.index('Rewards'), game.index('How to Earn the Drop')
            extracted_data.extend(game[reward_block_start_index+1:reward_block_end_index])
            game_data.append(extracted_data)
        return game_data

    def extract_block_data(self, block_name: str, data: list):
        # TODO: fix bug - while extracting data if game contains more than one campaign next game will be skipped
        separated_data = []
        word_separator = self.data_extract_config.get(block_name).get('word_separator')
        index_increment = self.data_extract_config.get(block_name).get('index_increment', 1)

        while word_separator in data:
            word_index = data.index(word_separator)
            separated_data.append(data[0:word_index + index_increment])
            data = [value for index, value in enumerate(data) if index not in range(0, word_index + index_increment)]

        separated_data = self.extract_game_data(separated_data)

        separated_data = list(map(lambda data_list: ({'game': data_list[0], 'company': data_list[1],
                                                      'campaign_dates': data_list[2], 'campaign_name': data_list[3],
                                                      'rewards': data_list[4:]}), separated_data))
        cleaned_data = list(filter(self.excluded_words_filter, separated_data))
        cleaned_data = list(map(self.split_campaign_dates, cleaned_data))

        updated_data = self.update_block_with_additional_info(block_name, cleaned_data)
        return updated_data

    def excluded_words_filter(self, data: dict):
        excluded_words = self.excluded_words

        flag = True

        for key in excluded_words:
            if data.get(key).strip() in excluded_words.get(key):
                flag = False

        return flag

    def update_block_with_additional_info(self, block_name: str, data_block: list):
        additional_information = self.block_additional_information.get(block_name)
        updated_block = [{**item, **additional_information} for item in data_block]
        return updated_block

    def process_data(self, unprocessed_data: dict):
        extracted_data = {}
        for block_name, data in unprocessed_data.items():
            extracted_data.update({block_name: self.extract_block_data(data=data, block_name=block_name)})

        return extracted_data

    def save_data(self, data_to_save: list):
        save_to_database(db_session, TableNamesMap.campaigns.value, data_to_save, exclude_duplicates=True)

    def parse(self, response):
        drop_blocks = response.xpath("//div[@class='Layout-sc-1xcs6mc-0 jmLWIr drops-root__content']/div")

        text_blocks = []
        for block in drop_blocks:
            text_blocks.append(block.xpath('./div//text()').extract())

        self.set_campaigns_index(text_blocks)
        # drops_data = {'open_reward_campaigns': text_blocks[2], 'open_drop_campaigns': text_blocks[self.open_campaign_index],
        #               'closed_drop_campaigns': text_blocks[self.closed_campaign_index]}
        # reward and closed campaigns are temporary excluded from data processing
        drops_data = {'open_drop_campaigns': text_blocks[self.open_campaigns_index]}
        processed_data = self.process_data(drops_data)

        for data_block in processed_data.values():
            self.save_data(data_block)

        return processed_data
