class Parameters():

    configuration = {}
    url_templates = {
        "check_ip" : "https://www.abuseipdb.com/check/[IP]/json?key=[API_KEY]&days=[DAYS]",
        "check_cidr" : "https://www.abuseipdb.com/check-block/json?key=[API_KEY]&network=[CIDR]&days=[DAYS]",
        "report_ip" : "https://www.abuseipdb.com/report/json?key=[API_KEY]&category=[CATEGORIES]&comment=[COMMENT]&ip=[IP]",
    }

    @staticmethod
    def get_config():
        return Parameters.configuration

    @staticmethod
    def set_config(config):
        Parameters.configuration = Parameters.dict_merge([Parameters.configuration, config])

    @staticmethod
    def merge_recursive(source, destination):
        """

        :rtype: dict
        """
        for key, value in source.items():
            if isinstance(value, dict):
                # get node or create one
                node = destination.setdefault(key, {})
                Parameters.merge_recursive(value, node)
            else:
                destination[key] = value

        return destination

    # taken from https://stackoverflow.com/questions/20656135/python-deep-merge-dictionary-data using recursion
    @staticmethod
    def dict_merge(list_dicts=[]):
        # print("List received: ")
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(list_dicts)
        # Merge multiple dicts
        target = {}
        while len(list_dicts) > 0:
            temp_dict = list_dicts.pop()
            # pp.pprint(temp_dict)
            target = Parameters.merge_recursive(target, temp_dict)
            # pp.pprint(target)
        return target