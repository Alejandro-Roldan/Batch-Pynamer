"""Code related to the plugins"""

import os

import batchpynamer.config as bpn_config

package_plugins_dirname = os.path.dirname(__file__)
plugin_dirs = [
    os.path.join(package_plugins_dirname, "plugins/"),
    bpn_config.plugins_folder_path,
]
