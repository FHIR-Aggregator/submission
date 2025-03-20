import requests


def test_search_parameters(fhir_base_urls, expected_part_of_study_search_parameters):
    """Test search parameters."""
    for base_url in fhir_base_urls:
        url = f"{base_url}/metadata"
        search_includes = []
        response = requests.get(url)
        response.raise_for_status()
        metadata = response.json()
        for rest in metadata['rest']:
            for resource in rest['resource']:
                for search_include in resource.get('searchInclude', []):
                    search_includes.append(search_include)
        actual = sorted([_ for _ in search_includes if 'part-of-study' in _])
        assert actual == expected_part_of_study_search_parameters, f"Unexpected search parameters: {actual} in {base_url}"


def test_search_definition_urls(fhir_base_urls, expected_search_definition_urls):
    for base_url in fhir_base_urls:
        url = f"{base_url}/metadata"
        search_includes = []
        response = requests.get(url)
        response.raise_for_status()
        metadata = response.json()
        """searchParam"""
        actual_definitions = []
        for rest in metadata['rest']:
            for resource in rest['resource']:
                for search_param in resource.get('searchParam', []):
                    actual_definitions.append(search_param['definition'])
        assert set(actual_definitions).issuperset(set(expected_search_definition_urls))