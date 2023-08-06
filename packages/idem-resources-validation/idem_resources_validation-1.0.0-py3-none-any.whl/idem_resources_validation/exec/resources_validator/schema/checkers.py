import json
import os
from os.path import isfile
from pathlib import Path
from typing import Any
from typing import Dict


def validate_schema(hub, ctx) -> Dict[str, Any]:
    result = dict(comment=[], ret=None, result=True)

    plugin_conf_file = os.environ["PLUGIN_CONFIG_FILE"] or None
    if not isfile(plugin_conf_file):
        raise Exception(
            f"The provided plugin conf file: {plugin_conf_file} does not exist."
        )

    test_config = {}
    with open(plugin_conf_file) as config_file:
        test_config = json.load(config_file)

    base_rev = test_config["base_version"]
    target_rev = test_config["target_version"]

    base_schema_json = hub.tool.schema.scm_utils.fetch_schema(test_config, base_rev)
    base_schema = json.loads(base_schema_json)

    current_schema_json = hub.tool.schema.scm_utils.fetch_schema(
        test_config, target_rev
    )
    current_schema = json.loads(current_schema_json)

    collector = hub.tool.schema.schema_compatibility_checker.check(
        current_schema,
        base_schema,
        hub.tool.schema.scm_utils.get_bool_attr(
            test_config, "validate_all_resources", "True"
        ),
        test_config["resources_to_validate"],
    )

    compatibility_report = collector.revisions(target_rev, base_rev).report_as_json()
    plugin_conf_file_name = Path(plugin_conf_file).stem
    with open(f"compatibility-report-{plugin_conf_file_name}.json", "w") as f:
        f.write(compatibility_report)

    return_msg = f"\nSchema compatibility check completed ({base_rev} -> {target_rev})"

    if collector.has_breaking_changes and hub.tool.schema.scm_utils.get_bool_attr(
        test_config, "fail_on_breaking_changes", "False"
    ):
        return_msg = (
            f"{return_msg}\nSchema compatibility check contains breaking changes."
        )
        raise Exception(return_msg)

    result["comment"] = ""
    result["ret"] = return_msg
    return result
