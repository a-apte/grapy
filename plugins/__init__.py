import os
import importlib

plugin_dir = os.path.dirname(__file__)

vendor_plugins = {
    name: importlib.import_module('{}.{}'.format(
        os.path.split(plugin_dir)[1],
        name[:-3]))
    for name
    in os.listdir(plugin_dir)
    if name.startswith('vendor_')
}

rating_plugins = {
    name: importlib.import_module('{}.{}'.format(
        os.path.split(plugin_dir)[1],
        name[:-3]))
    for name
    in os.listdir(plugin_dir)
    if name.startswith('rating_')
}
