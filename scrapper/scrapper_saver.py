import csv


class ScrapperSaver:
    __encoding = "utf-8"
    __delimiter = ";"
    __newline = ""
    __list_page_file = ""
    __detail_page_file = ""
    __all_items_file = ""

    def __init__(self, options: {}):
        try:
            self.__list_page_file = options["list_page"]
            self.__detail_page_file = options["detail_page"]
        except KeyError:
            print("list_page and detail_page options are required in ScrapperSaver object "
                  "if you pass the ScrapperSaver into Scrapper")

        try:
            self.__all_items_file = options["all_items"]
        except KeyError:
            print("all_items option is required in ScrapperSaver object")

    def save_list_page_row(self, item: {}):
        self.__save_row(self.__list_page_file, item)

    def save_detail_page_row(self, item: {}):
        self.__save_row(self.__detail_page_file, item)

    def save_all_items(self, all_items: []):
        fieldnames = self.__get_fields(all_items[0])

        with open(self.__all_items_file, "a", encoding=self.__encoding, newline=self.__newline) as file:
            writer = csv.DictWriter(file, delimiter=self.__delimiter, fieldnames=fieldnames)
            writer.writerow(fieldnames)
        with open(self.__all_items_file, "a", encoding=self.__encoding, newline=self.__newline) as file:
            writer = csv.DictWriter(file, delimiter=self.__delimiter, fieldnames=fieldnames)
            for item in all_items:
                writer.writerow(item)

    def __save_row(self, file_name: "", item: {}):
        try:
            file = open(file_name, "a+", encoding=self.__encoding, newline=self.__newline)
            writer = csv.DictWriter(file, delimiter=self.__delimiter, fieldnames=self.__get_fields(item))

            file.seek(0)
            if not file.readline():
                writer.writeheader()

            writer.writerow(item)
            file.close()
        except:
            print("File write error: %s" % file_name)

    @staticmethod
    def __get_fields(item: {}):
        return dict(zip(item.keys(), item.keys()))
