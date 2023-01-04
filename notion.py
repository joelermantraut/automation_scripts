import re
from pprint import pprint
from notion_client import Client
from notion_client.helpers import (is_full_page,
                                    is_full_database,
                                    iterate_paginated_api,
                                    collect_paginated_api)

class NotionAccess(object):
    """
    Class to access Notion databases and pages.
    """
    def __init__(self, NOTION_TOKEN):
        """
        Access https://www.notion.so/my-integrations to get or create
        notion token.
        """
        super(NotionAccess, self).__init__()
        self.NOTION_TOKEN = NOTION_TOKEN
        self.init()

    def init(self):
        self.notion = Client(auth=self.NOTION_TOKEN)

    def get_db_id_from_link(self, database_id):
        """
        Converts database link to database id.
        """
        if len(database_id) > 32:
            database_id = re.search('so/(.+?)\?', database_id).group(1)
        # If receives complete link to page

        return database_id

    def access_database(self, database_id, filtering=None):
        """
        Function to access a database. It can receive 32 chars string or
        complete link to page.

        https://www.notion.so/{database_id}?v={more_numbers}

        Returns database object, and a second argument to define if object
        is database or page, because filter parameter could return a page.
        """
        database_id = self.get_db_id_from_link(database_id)

        if filtering:
            database = self.notion.databases.query(
                **{
                    "database_id": database_id,
                    "filter": filtering
                }
            )
        else:
            database = self.notion.databases.query(
                **{
                    "database_id": database_id
                }
            )

        return database, is_full_database(database)

    def get_page_id_from_link(self, page_id):
        """
        Converts page link to page id.
        """
        if len(page_id) > 32:
            page_id = page_id[-32:]
        # If receives complete link to page, returns last 32 chars

        return page_id

    def access_page(self, database, page_id):
        """
        Function to access a page. It can receive 32 chars string or
        complete link to page.

        https://www.notion.so/{book_name}-{page_id}

        Returns page object, and a second argument to define if object
        is a full page.
        """
        page_id = self.get_page_id_from_link(page_id)

        for page in database["results"]:
            if self.get_page_id_from_link(page["url"]) == page_id:
                break

        return page, is_full_page(page)

    def get_content(self, database_id):
        database_id = self.get_db_id_from_link(database_id)

        all_results = collect_paginated_api(
            self.notion.databases.query, database_id=database_id
        )

        return all_results

    def get_properties(self, page):
        """
        Returns properties simplified, taking out IDs and other parameter
        that might not be useful.
        """
        new_properties = dict()

        properties = page["properties"]
        for property in properties:
            new_properties[property] = dict()

            properties_value = properties[property]
            property_type = properties_value["type"]

            new_properties[property]["type"] = property_type
            if property_type == "title":
                new_properties[property]["value"] = properties_value["title"][0]["plain_text"]
            elif property_type == "multi_select":
                multi_selectors = properties_value["multi_select"]
                multi_select_list = list()
                for multi_select in multi_selectors:
                    multi_select_list.append(multi_select["name"])

                new_properties[property]["multi_select"] = multi_select_list
            elif property_type == "number":
                new_properties[property]["value"] = properties_value["number"]
            elif property_type == "rich_text":
                new_properties[property]["value"] = properties_value["rich_text"][0]["plain_text"]
            elif property_type == "checkbox":
                new_properties[property]["value"] = properties_value["checkbox"]

        return new_properties

def main():
    with open(".credentials.txt", "r") as file:
        [NOTION_TOKEN, DATABASE_ID, PAGE_ID] = file.read().split(",")

    notion_object = NotionAccess(NOTION_TOKEN)
    db, is_db = notion_object.access_database(DATABASE_ID)
    page, is_page = notion_object.access_page(db, PAGE_ID)

    if is_page:
        properties = notion_object.get_properties(page)

    content = notion_object.get_content(DATABASE_ID)

    pprint(content)

if __name__ == "__main__":
    main()