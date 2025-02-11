def find_key_with_path(data, key_to_find, ignored_keys=[]):
    """
    Traverse the dictionary and find all occurrences of a given key.
    Returns a list of dictionaries containing the path and value for each match.
    Paths containing keys in the ignored_keys list are skipped.

    :param data: The input dictionary or list to search.
    :param key_to_find: The key to look for in the data structure.
    :param ignored_keys: A list of keys to ignore during traversal.
    :return: A list of dictionaries with 'path' and 'value' for each match.
    """
    results = []

    def recursive_search(d, current_path=[]):
        if isinstance(d, dict):
            for key, value in d.items():
                new_path = current_path + [key]

                if key in ignored_keys:
                    continue  # Skip paths containing ignored keys

                if key == key_to_find:
                    found_ignored_key_in_extension = False
                    if "extension" in new_path:
                        extension_url = get_value_from_path(data, new_path[:-2] + ["url"])
                        if extension_url:
                            for k in ignored_keys:
                                if k in extension_url:
                                    found_ignored_key_in_extension = True
                                    break
                    if found_ignored_key_in_extension:
                        continue
                    results.append({"path": new_path, "value": value})
                recursive_search(value, new_path)
        elif isinstance(d, list):
            for index, item in enumerate(d):
                new_path = current_path + [index]
                recursive_search(item, new_path)

    recursive_search(data)
    return results


def get_value_from_path(data, path):
    """
    Retrieve a value from a nested dictionary or list using a path array.

    :param data: The nested dictionary or list to retrieve the value from.
    :param path: A list representing the path to the desired value.
    :return: The value at the specified path, or None if the path is invalid.
    """
    try:
        for key in path:
            data = data[key]
        return data
    except (KeyError, IndexError, TypeError):
        return None
