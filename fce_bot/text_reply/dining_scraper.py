import traceback


class DiningScraper:
    """
    Scraper class for CMU dining location web page.

    Page URL is here: https://apps.studentaffairs.cmu.edu/dining/conceptinfo/?page=listConcepts&soup=False&special=False&open=False&online=False&locationId=0&searchTerm=hunan
    Notice that there are url parameters to pass in to filter dining locations. The `searchTerm` parameter here should
    be especially helpful
    """

    def __init__(self, logger):
        self.logger = logger

    def query_dining_location(self, query: str) -> str:
        """
        Queries CMu dining location status
        Parameters:
            query (str): string query provided by user
        Returns:
            (str): string reply; empty string if no result found
        """
        try:
            # TODO: write code here
            # TODO: consider writing this method using a TTL cache (say time_to_live = 30 secs). In this way, we can 1)
            # TODO: speed up the application, 2) reduce number of times we hit the dining location website
            # TODO: Reading for TTLCache is here: https://www.geeksforgeeks.org/cachetools-module-in-python/
            raise NotImplementedError
        except Exception as e:
            self.logger.error(f"Following error happened: {e}")
            tb = traceback.format_exc()
            self.logger.error(tb)
            return "出现错误"
