import os
import shutil
import subprocess
import tempfile
from typing import Dict


script_template = """
cd "{clone_dir}"
git clone "{repo_url}"
cd "{work_dir}"
git checkout {rev}
python -m venv venv
source "{work_dir}"/venv/bin/activate
pip uninstall -q -y --disable-pip-version-check --require-virtualenv {plugin_name}
python3 -m pip install pip==21
pip install -q --disable-pip-version-check --require-virtualenv -e .
idem doc {plugin_idem_doc_key} --output=json > "{out_file}"
"""


def fetch_schema(hub, plugin_conf: Dict, rev: str):
    tmp_dir = tempfile.mkdtemp()
    try:
        return _fetch_schema_for_rev(plugin_conf, rev, tmp_dir)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _fetch_schema_for_rev(plugin_conf: Dict, rev: str, clone_dir: str):

    repo_url = plugin_conf["repo_url"]
    plugin_name = plugin_conf["plugin_name"]
    plugin_idem_doc_key = f"states.{plugin_conf['idem_doc_root_name']}"

    out_file = os.path.abspath(os.path.join(clone_dir, f"{rev}.json"))
    work_dir = os.path.join(clone_dir, os.path.splitext(os.path.basename(repo_url))[0])

    script_file = f"schema-{rev}.sh"
    command = ["/bin/bash", script_file]

    with open(os.path.join(clone_dir, script_file), "w") as f:
        script = script_template.format(
            **{
                "clone_dir": clone_dir,
                "repo_url": repo_url,
                "rev": rev,
                "plugin_name": plugin_name,
                "plugin_idem_doc_key": plugin_idem_doc_key,
                "out_file": out_file,
                "work_dir": work_dir,
            }
        )
        f.write(script)

    print(f"Fetching schema for commit/tag {rev}")

    ret = subprocess.run(
        command,
        cwd=clone_dir,
        capture_output=True,
    )

    if not ret or ret.returncode != 0:
        print(f"Error fetching schema: {str(ret.stderr, 'utf-8')}")
        return None

    with open(os.path.join(work_dir, out_file)) as f:
        result = f.read()

    if result:
        end_mark = result.rfind("}")
        if end_mark != -1:
            result = result[: end_mark + 1]

    return result


def get_bool_attr(hub, test_schema: Dict, attribute: str, default_value: str) -> bool:
    attr_value = default_value
    if attribute in test_schema and test_schema[attribute]:
        attr_value = test_schema[attribute]
    return eval(attr_value)
