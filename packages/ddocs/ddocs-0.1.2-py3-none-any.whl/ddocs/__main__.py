#!/usr/bin/env python3

import argparse
import sys
import subprocess
import platformdirs

import pkg_resources

from ddocs.modules import ModulesManager

DESCRIPTION = '''

Offline and fast documentation (+ source code) cli viewer for python libraries.
For when using a browser can be a pain. Also an optional gui.

'''

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("--gui", help="Open simple gui version of ddocs.", nargs="?", const=True)
    parser.add_argument("--search", help="Search for modules starting with the argument.")
    parser.add_argument("--update", help="Update the database to match the modules located in the languages/python.txt file.", nargs="?", const=True)
    parser.add_argument("--update-module", help="Deletes the input module data from the database and re-downloads the latest data if the module is found in the languages/python.txt file.")
    parser.add_argument("--reset-database", help="Resets the entire database, then downloads module data given the languages/python.txt file. This can take some time.", nargs='?', const=True)
    parser.add_argument("--list-all", help="List all modules in the database", nargs="?", const=True)
    parser.add_argument("module", nargs="?", help="Name of the module e.g. builtins, math, numpy")
    parser.add_argument("entities", nargs="*", help="Optional name of entities in the module e.g. str, sqrt, vectorize")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Create an instance of ModulesManager
    target_dir = platformdirs.user_config_dir("ddocs", "gkegke")

    manager = ModulesManager(target_dir)

    # Check if no module name is given
    if len(sys.argv) == 1:
        print("No arguments given.")
        parser.print_help()
        sys.exit()

    if args.gui:
        gui_path = pkg_resources.resource_filename('ddocs', 'gui.py')
        subprocess.run(["python3", gui_path])
        sys.exit()

    if args.list_all:
        manager.list_all_modules()
        sys.exit()

    # Check if --update option is provided
    if args.update:
        print("Updating the database...")
        manager.update_database()
        print("Database updated successfully.")
        sys.exit()

    # Check if --reset-database option is provided
    if args.reset_database:
        print("Resetting the entire database...")
        manager.reset_database()
        print("Database reset and updated successfully.")
        sys.exit()

    # Check if --update-module option is provided
    if args.update_module:
        print(f"Updating module {args.update_module}...")
        manager.update_module(args.update_module, args.update)
        print(f"Module {args.update_module} updated successfully.")
        sys.exit()

    # If --search option is provided, find modules starting with the inputted prefix
    if args.search:
        print(f"Searching for modules starting with '{args.search}'")
        manager.module_starts_with(args.search)
        sys.exit()

    # Get the module name if provided
    module_name = args.module

    # Check module existence if module name is provided
    module = manager.get_module(module_name)

    # Get the module id and doc from the query result
    module_id, module_doc = module

    # Print the module doc
    manager.print_module_doc(module_name, module_doc)

    # If no entity names are given, list all the entities that belong to the module and have no parent entity
    if len(args.entities) == 0:
        manager.list_top_layer_entities(module_id)
        sys.exit()

    # Loop through the provided entity names and check their validity
    parent_entity_id = None

    for i, entity_name in enumerate(args.entities):
        entity = manager.get_entity(module_id, parent_entity_id, entity_name)

        # Get the entity attributes from the query result
        entity_id, name, is_class, doc, signature, return_, source = entity

        # Print the entity details
        manager.print_entity_details(name, is_class, signature, return_, doc, source)

        # Update the parent entity id to the current entity id
        parent_entity_id = entity_id

    # Print all the children entities of the final entity
    manager.list_children_entities(module_id, parent_entity_id)

if __name__ == '__main__':
    main()
