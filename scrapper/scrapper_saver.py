import csv


class ScrapperSaver:
    __encoding = "utf-8"
    __delimiter = ";"
    __newline = ""
    __list_page_file = ""
    __detail_page_file = ""
    __all_items_file = ""

    def __init__(self, options: {}):

        if "list_page" in options and "detail_page" in options:
            self.__list_page_file = options["list_page"]
            self.__detail_page_file = options["detail_page"]
        elif "all_items" not in options:
            raise Exception(
                "You should to specify `all_items` or `list_page` and `detail_page` options in ScrapperSaver object")

        try:
            self.__all_items_file = options["all_items"]
        except KeyError:
            print("`all_items` has not been specified in ScrapperSaver's options")

    def save_list_page_row(self, item: {}):
        self.__save_row(self.__list_page_file, item)

    def save_detail_page_row(self, item: {}):
        self.__save_row(self.__detail_page_file, item)

    def save_all_items(self, all_items: []):
        fieldnames = self.__get_fields(all_items[0])

        if not self.__all_items_file:
            raise Exception("File name of `all_items` doesn't exist in ScrapperSaver object")

        with open(self.__all_items_file, "a", encoding=self.__encoding, newline=self.__newline) as file:
            writer = csv.DictWriter(file, delimiter=self.__delimiter, fieldnames=fieldnames)
            writer.writerow(fieldnames)
        with open(self.__all_items_file, "a", encoding=self.__encoding, newline=self.__newline) as file:
            writer = csv.DictWriter(file, delimiter=self.__delimiter, fieldnames=fieldnames)
            for item in all_items:
                writer.writerow(item)

        print("Records has been successfully saved to the file %s!" % self.__all_items_file)

    def __save_row(self, file_name: "", item: {}):
        try:
            file = open(file_name, "a+", encoding=self.__encoding, newline=self.__newline)
            writer = csv.DictWriter(file, delimiter=self.__delimiter, fieldnames=self.__get_fields(item))

            file.seek(0)
            if not file.readline():
                writer.writeheader()

            writer.writerow(item)
            file.close()

            print("+++ Records has been successfully saved to the temporary file %s! +++" % file_name)
        except FileNotFoundError as e:
            raise Exception("ScrapperSaver object has no `list_page`, `detail_page` or `all_items` options") from e

    @staticmethod
    def __get_fields(item: {}):
        return dict(zip(item.keys(), item.keys()))
