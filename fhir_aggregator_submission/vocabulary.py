import sys
import uuid
from collections import defaultdict
from typing import Any

from fhir_aggregator_submission import find_key_with_path


def tree() -> defaultdict:
    """A recursive defaultdict."""
    return defaultdict(tree)


def extract_coding_values(
    resource: dict[str, Any], code_dict: dict[str, Any] | None
) -> dict[str, Any]:
    """
    Extracts coding values from `coding` and maintains a count dictionary.

    Args:
        resource (dict): A FHIR resource dictionary.
        code_dict (Dict[str, int], optional): A dictionary to store code display values and their counts. Defaults to defaultdict(int).

    Returns:
        Dict[str, int]: A recursive dictionary with code display values as keys and their counts as values.  Primary key is the resourceType + the first part of the path
    """

    if not code_dict:
        code_dict = tree()

    coding_matches = find_key_with_path(resource, "coding", ignored_keys=["extension"])
    for coding_match in coding_matches:
        path = coding_match["path"]
        # key is the resourceType + the first part of the path
        key = f"{resource['resourceType']}.{path[0]}"
        coding_list = coding_match["value"]
        for coding in coding_list:
            if "display" in coding:
                if coding["display"] not in code_dict[key]:
                    code_dict[key][coding["display"]] = {
                        "count": 0,
                        "valueCoding": coding,
                    }
                code_dict[key][coding["display"]]["count"] += 1

    return code_dict


# def extract_display_values(
#     resource: dict[str, Any],
#     code_dict: dict[str, int] = defaultdict(int),
#     category_dict: dict[str, int] = defaultdict(int),
# ) -> (dict[str, int], dict[str, int]):
#     """
#     Extracts display values from `code.coding` and `category.coding`
#     and maintains a count dictionary.
#
#     Args:
#         resource (dict): A FHIR resource dictionary.
#         code_dict (Dict[str, int], optional): A dictionary to store code display values and their counts. Defaults to defaultdict(int).
#         category_dict (Dict[str, int], optional): A dictionary to store category display values and their counts. Defaults to defaultdict(int).
#
#     Returns:
#         Tuple[Dict[str, int], Dict[str, int]]: A tuple containing the code and category dictionaries.
#     """
#
#     # Extract from code.coding.display
#     if "code" in resource and "coding" in resource["code"]:
#         for coding in resource["code"]["coding"]:
#             if "display" in coding:
#                 code_dict[coding["display"]] += 1
#
#     # Extract from category.coding.display
#     if "category" in resource:
#         if isinstance(resource["category"], list):  # Handle list of categories
#             for category in resource["category"]:
#                 if "coding" in category:
#                     for coding in category["coding"]:
#                         if "display" in coding:
#                             category_dict[coding["display"]] += 1
#
#     return code_dict, category_dict


def extract_extension_values(
    resource: dict[str, Any], extension_dict: dict[str, Any] | None
) -> dict[str, Any]:
    """
    Extracts values from `extension.value[x]` fields and maintains a count dictionary.

    Args:
        resource (dict): A FHIR resource dictionary.
        extension_dict (Dict[str, int], optional): A dictionary to store extension values and their counts. Defaults to defaultdict(int).

    Returns:
        Dict[str, int]: A dictionary with extension values as keys and their counts as values.
    """

    if not extension_dict:
        extension_dict = tree()

    if "extension" not in resource:
        return extension_dict

    for extension in resource["extension"]:
        key = f"{resource['resourceType']}.extension~{extension['url']}"
        if "valueCodeableConcept" in extension:
            for coding in extension["valueCodeableConcept"]["coding"]:
                if "display" in coding:
                    if coding["display"] not in extension_dict[key]:
                        extension_dict[key][coding["display"]] = {
                            "count": 0,
                            "valueCoding": coding,
                        }
                    extension_dict[key][coding["display"]]["count"] += 1
        elif "valueCoding" in extension:
            for coding in extension["valueCoding"]:
                if "display" in coding:
                    if coding["display"] not in extension_dict[key]:
                        extension_dict[key][coding["display"]] = {
                            "count": 0,
                            "valueCoding": coding,
                        }
                    extension_dict[key][coding["display"]]["count"] += 1
        elif "valueCode" in extension:
            if extension["valueCode"] not in extension_dict[key]:
                extension_dict[key][extension["valueCode"]] = {
                    "count": 0,
                    "valueCode": extension["valueCode"],
                }
            extension_dict[key][extension["valueCode"]]["count"] += 1
        elif "valueString" in extension:
            if extension["valueString"] not in extension_dict[key]:
                extension_dict[key][extension["valueString"]] = {
                    "count": 0,
                    "valueString": extension["valueString"],
                }
            extension_dict[key][extension["valueString"]]["count"] += 1
        elif "valueQuantity" in extension:
            if "range" not in extension_dict[key]:
                extension_dict[key] = {
                    "range": {"min": sys.maxsize, "max": -sys.maxsize - 1}
                }
            if (
                extension["valueQuantity"]["value"]
                < extension_dict[key]["range"]["min"]
            ):
                extension_dict[key]["range"]["min"] = extension["valueQuantity"][
                    "value"
                ]
                # print(key, 'min', extension_dict[key]["min"])
            if (
                extension["valueQuantity"]["value"]
                > extension_dict[key]["range"]["max"]
            ):
                extension_dict[key]["range"]["max"] = extension["valueQuantity"][
                    "value"
                ]
                # print(key, 'max', extension_dict[key]["max"])
        else:
            continue

    return extension_dict


def create_observation_component(code_dict, extension_dict):
    """
    Creates an Observation component from code_dict, category_dict, and extension_dict.

    Args:
        code_dict (dict): Dictionary with code display values and their counts.
        extension_dict (dict): Dictionary with extension values and their counts.

    Returns:
        dict: A FHIR Observation component.
    """
    observation_dict = {
        "resourceType": "Observation",
        "status": "final",
        "code": {
            "coding": [
                {
                    "system": "http://fhir-aggregator.org/fhir/CodeSystem/vocabulary",
                    "code": "vocabulary",
                    "display": "Vocabulary",
                }
            ]
        },
        "component": [
            {
                "code": {
                    "coding": [
                        {
                            "system": "http://fhir-aggregator.org/fhir/CodeSystem/vocabulary/path",
                            "code": key,
                            "display": key,
                        },
                        next(iter(value.values()))["valueCoding"],
                    ]
                },
                "valueInteger": next(iter(value.values()))["count"],
            }
            for key, value in code_dict.items()
        ],
    }
    extension_components = []
    for path, value_dict in extension_dict.items():
        path_components = path.strip().split("~")
        path = path_components[0].strip()
        system = path_components[1].strip()
        for code, value in value_dict.items():
            component = {
                "code": {
                    "coding": [
                        {
                            "system": system,
                            "code": code,
                            "display": code,
                        },
                        {
                            "system": "http://fhir-aggregator.org/fhir/CodeSystem/vocabulary/path",
                            "code": path,
                            "display": path,
                        },
                    ]
                },
                # "extension": [
                #     {
                #         "url": "http://fhir-aggregator.org/fhir/StructureDefinition/vocabulary-collector-extension/path",
                #         "valueString":  path
                #     }
                # ]
            }
            v = value
            value_x = None
            if isinstance(value, dict):
                for k in ["count"]:
                    if k in value:
                        value_x = {f"valueInteger": value[k]}
                        break
                if not value_x:
                    if sorted(value.keys()) == sorted(("min", "max")):
                        value_x = {
                            f"valueRange": {
                                "low": {"value": value["min"]},
                                "high": {"value": value["max"]},
                            }
                        }
                    else:
                        raise ValueError(
                            f"Unexpected value type: {value} no {['count', 'range']}"
                        )
            if not value_x:
                value_x = {"valueInteger": v}
            # xform from defaultdict back to dict
            component = dict(component)
            component.update(value_x)
            extension_components.append(component)
    observation_dict["component"].extend(extension_components)
    return observation_dict


def get_research_study_id(resource: dict[str, Any]) -> str:
    """Get the ResearchStudy ID from a resource."""
    assert "extension" in resource, f"Resource {resource} does not have an extension"
    reference = next(
        iter(
            [
                ext["valueReference"]["reference"]
                for ext in resource["extension"]
                if ext["url"]
                == "http://fhir-aggregator.org/fhir/StructureDefinition/part-of-study"
            ]
        ),
        None,
    )
    assert (
        reference
    ), f"Resource {resource} does not have a reference to a ResearchStudy"
    return reference.split("/")[-1]


def make_dicts() -> tuple[dict | None, dict]:
    """Create default dictionaries for coding and extension values."""
    coding_dict = None
    extension_dict: Any = defaultdict(int)
    return coding_dict, extension_dict


class VocabularyCollector:
    """Create a histogram of display values for a resource type."""

    research_study_vocabularies: dict[str, tuple[dict, dict]]

    def __init__(self):
        """Initialize the VocabularyCollector."""
        self.research_study_vocabularies = defaultdict(make_dicts)

    def collect(self, resource: dict[str, Any]) -> dict[str, Any]:
        """Collect display values from a resource."""
        research_study_id = get_research_study_id(resource)
        coding_dict, extension_dict = self.research_study_vocabularies[
            research_study_id
        ]
        coding_dict = extract_coding_values(resource, coding_dict)
        extension_dict = extract_extension_values(resource, extension_dict)
        self.research_study_vocabularies[research_study_id] = (
            coding_dict,
            extension_dict,
        )
        return resource

    def to_observations(self) -> list[dict[str, Any]]:
        """Convert the collected data into a FHIR Observation resource.

        Returns:
            list[dict]: A FHIR Observation resource - one per ResearchStudy observed.

        """
        observations = []
        for research_study_id, (
            coding_dict,
            extension_dict,
        ) in self.research_study_vocabularies.items():
            observation = create_observation_component(coding_dict, extension_dict)
            observation["focus"] = [{"reference": f"ResearchStudy/{research_study_id}"}]
            observation["extension"] = observation.get("extension", [])
            observation["extension"].append(
                {
                    "url": "http://fhir-aggregator.org/fhir/StructureDefinition/part-of-study",
                    "valueReference": {
                        "reference": f"ResearchStudy/{research_study_id}"
                    },
                }
            )
            observation["id"] = str(
                uuid.uuid5(
                    uuid.NAMESPACE_DNS, f"vocabulary-collector-{research_study_id}"
                )
            )
            observations.append(observation)
        return observations
