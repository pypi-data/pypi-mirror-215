import json


class DataProcessor:
    def __init__(self, json_data):
        self.data = json_data

    def display_country_info(self):
        country_name = self.data['name']['common']
        official_name = self.data['name']['official']
        capital = self.data['capital'][0]
        population = self.data['population']
        area = self.data['area']

        print("Country: ", country_name)
        print("Official Name: ", official_name)
        print("Capital: ", capital)
        print("Population: ", population)
        print("Area: ", area, " square kilometers")


        def get_languages(self):
            languages = self.data['languages']
            print("Languages:")
            for language in languages:
                print(language, ": ", languages[language])

        def get_timezones(self):
            timezones = self.data['timezones']
            print("Timezones:")
            for timezone in timezones:
                print(timezone)

        def get_borders(self):
            borders = self.data['borders']
            print("Borders:")
            for border in borders:
                print(border)

        def get_flag_urls(self):
            flag_urls = self.data['flags']
            return flag_urls
