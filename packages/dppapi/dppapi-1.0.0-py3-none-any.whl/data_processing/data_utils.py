import json


class DataProcessor:
    def __init__(self, json_data):
        self.data = json.loads(json_data)[0]

    def display_country_info(self):
        country_name = self.data['name']['common']
        official_name = self.data['name']['official']
        capital = self.data['capital'][0]
        population = self.data['population']
        area = self.data['area']
        currency_name = self.data['currencies']['PLN']['name']
        currency_symbol = self.data['currencies']['PLN']['symbol']

        print("Country: ", country_name)
        print("Official Name: ", official_name)
        print("Capital: ", capital)
        print("Population: ", population)
        print("Area: ", area, " square kilometers")
        print("Currency: ", currency_name, "(", currency_symbol, ")")

        def get_languages():
            languages = self.data['languages']
            print("Languages:")
            for language in languages:
                print(language, ": ", languages[language])

        def get_timezones():
            timezones = self.data['timezones']
            print("Timezones:")
            for timezone in timezones:
                print(timezone)

        def get_borders():
            borders = self.data['borders']
            print("Borders:")
            for border in borders:
                print(border)

        def get_flag_urls():
            flag_urls = self.data['flags']
            return flag_urls
