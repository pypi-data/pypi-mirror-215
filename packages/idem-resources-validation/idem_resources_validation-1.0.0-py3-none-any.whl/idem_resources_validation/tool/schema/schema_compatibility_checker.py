import json
import re
from typing import Dict
from typing import Set

from deepdiff import DeepDiff

from idem_resources_validation.tool.schema.results_collector import ResultsCollector


def check(
    hub,
    current_schema: Dict,
    base_schema: Dict,
    validate_all_resources: bool,
    resources_to_validate: Set[str],
) -> ResultsCollector:

    global all_resources_validation
    all_resources_validation = validate_all_resources

    if not all_resources_validation:
        _build_resources_path_regex(resources_to_validate)

    collector = ResultsCollector()
    exclude_paths = set()

    current_schema = _escape_square_brackets(current_schema)
    current_resources = _enumerate_resources(current_schema)
    base_schema = _escape_square_brackets(base_schema)
    base_resources = _enumerate_resources(base_schema)

    if current_resources != base_resources:
        removed = base_resources.difference(current_resources)
        if removed:
            for resource in removed:
                resource_formatted = f"root['{resource}']"
                if not all_resources_validation and not re.search(
                    resources_path_regex, resource_formatted
                ):
                    continue
                collector.add_breaking(
                    schema_path=resource_formatted, description="Resource removed"
                )
                exclude_paths.add(rf"root\[.*{resource}.*\]")

        added = current_resources.difference(base_resources)
        if added:
            for resource in added:
                resource_formatted = f"root['{resource}']"
                if not all_resources_validation and not re.search(
                    resources_path_regex, resource_formatted
                ):
                    continue
                collector.add_non_breaking(
                    schema_path=resource_formatted, description="Resource added"
                )
                exclude_paths.add(rf"root\[.*{resource}.*\]")

    for k in current_schema.keys():
        exclude = {
            key
            for key in current_schema[k].keys()
            if key not in ["parameters", "return_annotation"]
        }
        for key in exclude:
            exclude_paths.add(rf"root\[.*\]\['{key}'\]")

    changes = DeepDiff(
        base_schema,
        current_schema,
        exclude_regex_paths=list(exclude_paths),
        include_obj_callback=_include_obj_callback,
    )

    for v in changes.get("dictionary_item_added") or []:
        collector.add_non_breaking(
            schema_path=v, description=f"{_description_for(v, 'added')}"
        )

    for v in changes.get("dictionary_item_removed") or []:
        collector.add_breaking(
            schema_path=v, description=f"{_description_for(v, 'removed')}"
        )

    changed_schema_values = changes.get("values_changed") or []
    missing_type_str = "dataclasses._MISSING_TYPE object"

    for v in changed_schema_values:
        current_changes = changed_schema_values.get(v)

        # Remove 'dataclasses._MISSING_TYPE object checks' findings from the report
        # if both new_value and old_value contains the string.
        if (
            current_changes.get("new_value").find(missing_type_str) != -1
            and current_changes.get("old_value").find(missing_type_str) != -1
        ):
            continue

        collector.add_breaking(
            schema_path=v, description=f"{_description_for(v, 'changed')}"
        )

    return collector


def _include_obj_callback(obj, path):
    if all_resources_validation:
        return True
    else:
        return re.search(resources_path_regex, path)


def _build_resources_path_regex(resources: Set[str]):
    global resources_path_regex
    resources_path_regex = r"root\['states\.("

    for resource in resources:
        escaped_str = resource.replace(".", r"\.")
        resources_path_regex += escaped_str
        resources_path_regex += "|"

    # remove the last pipe "|" in the regex
    resources_path_regex = resources_path_regex[: len(resources_path_regex) - 1]
    resources_path_regex += r")\..*?']"


def _escape_square_brackets(schema: Dict) -> Dict:
    json_schema = json.dumps(schema)
    # remove opening square brackets '[' in annotation typings and replace it with empty space
    json_schema = re.sub(r"(\b[a-zA-Z]*?)\[", r"\1 ", json_schema)
    # remove closing square brackets ']' in annotation typings and replace it with empty space
    # matches also multiple closing brackets in this case 'typing.Dict[str, typing.Dict[str, typing.Any]]'
    json_schema = re.sub(r"(\b[a-zA-Z]*?)\]{1,}", r"\1 ", json_schema)
    return json.loads(json_schema)


def _enumerate_resources(schema: Dict) -> Set[str]:
    return {".".join(s.split(".")[2:-1]) for s in schema.keys()}


def _description_for(change: str, op: str) -> str:
    parts = [x.rstrip("]") for x in change.split("[")]
    if parts[0] == "root":
        depth = len(parts)
        if depth == 2:
            return f"{op} method {parts[1]}"
        elif depth == 3:
            return f"{op} {parts[1]} method's {parts[2]} property"
        elif depth == 4:
            return f"{op} parameter {parts[3]}"
        elif depth == 5:
            return f"{op} {parts[3]} parameter's {parts[4]} property"
        elif depth >= 6 and depth % 3 == 0:  # 6, 9, 12 ...
            return f"Annotation type change: {op} {parts[depth - 1]}"
        elif depth >= 7 and (depth - 1) % 3 == 0:  # 7, 10, 13 ...
            return (
                f"Change in {parts[depth - 2]} type: {op} parameter {parts[depth - 1]}"
            )
        elif depth >= 8 and (depth - 2) % 3 == 0:  # 8, 11, 14 ...
            return f"Change in {parts[depth - 3]} type: {op} {parts[depth - 2]} parameter's {parts[depth - 1]} property"

    return f"Cannot parse change: {change}"
