import sys 
import pkg_resources; 
import tabulate


def list_pkg():
    try:
      from pip import get_installed_distributions
    except:
      from pip._internal.utils.misc import get_installed_distributions

    tabpackages = []
    for _, package in sorted([('%s %s' % (i.location, i.key), i) for i in get_installed_distributions()]):
      tabpackages.append([package.location, package.key, package.version])

    print(tabulate.tabulate(tabpackages))

# import pkgutil.iter_modules()

""" applies to the system scope or to a virtual environment scope

packages installed by setuptools, pip and (god forbid) easy_install
"""

installed_packages = list(sorted(["==".join([d.project_name, d.version]) + '\n' for d in pkg_resources.working_set]))
# import pkg_resources; installed_packages = [(d.project_name, d.version) for d in pkg_resources.working_set]

# env_name = sys.argv[0].split('/')[-1]
env_name = sys.executable.replace('/bin/python','').split('/')[-1]
with open(f'{env_name}_requirements.txt', 'w') as f:
    f.writelines(installed_packages)


help("modules")

## not shoing modules installed via namespalce packages
python -c 'help("modules")'

## cmd
pydoc modules

pip freeze 

pip list --local

sys.modules.keys()
sys.builtin_module_names 

## importing modules
importlib.util.find_spec()



import sys
import os
import shutil
import pkgutil
import importlib
import collections

if sys.version_info.major == 2:
    raise NotImplementedError('CPython 2 is not supported yet')


def main():

    # name this file (module)
    this_module_name = os.path.basename(__file__).rsplit('.')[0]

    # dict for loaders with their modules
    loaders = collections.OrderedDict()

    # names`s of build-in modules
    for module_name in sys.builtin_module_names:

        # find an information about a module by name
        module = importlib.util.find_spec(module_name)

        # add a key about a loader in the dict, if not exists yet
        if module.loader not in loaders:
            loaders[module.loader] = []

        # add a name and a location about imported module in the dict
        loaders[module.loader].append((module.name, module.origin))

    # all available non-build-in modules
    for module_name in pkgutil.iter_modules():

        # ignore this module
        if this_module_name == module_name[1]:
            continue

        # find an information about a module by name
        module = importlib.util.find_spec(module_name[1])

        # add a key about a loader in the dict, if not exists yet
        loader = type(module.loader)
        if loader not in loaders:
            loaders[loader] = []

        # add a name and a location about imported module in the dict
        loaders[loader].append((module.name, module.origin))

    # pretty print
    line = '-' * shutil.get_terminal_size().columns
    for loader, modules in loaders.items():
        print('{0}\n{1}: {2}\n{0}'.format(line, len(modules), loader))
        for module in modules:
            print('{0:30} | {1}'.format(module[0], module[1]))


if __name__ == '__main__':
    main()