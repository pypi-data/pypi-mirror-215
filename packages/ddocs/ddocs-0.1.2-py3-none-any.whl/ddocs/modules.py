#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ddocs.db import DatabaseManager

import os
import sys
import shutil
import logging
import inspect
import importlib

import pkg_resources

class ModulesManager:
    def __init__(self, modules_filepath):

        self.modules_filepath = modules_filepath

        flag = False

        if not os.path.exists(modules_filepath):
            os.makedirs(modules_filepath)

            # Copy the "languages" folder to the specified filepath
            languages_folder_src = pkg_resources.resource_filename('ddocs','languages')
            languages_folder_dest = os.path.join(modules_filepath, 'languages')
            shutil.copytree(languages_folder_src, languages_folder_dest)

            flag = True

        database_path = os.path.join(modules_filepath, 'ddocs.db')
        modules_list_filepath = os.path.join(modules_filepath, 'languages', 'python.txt')

        self.dbm = DatabaseManager(database_path)
        self.modules = self.modules_list(modules_list_filepath)
        self.setup_logging()
        logging.info(f"{len(self.modules)} modules found")

        if flag:
            print(f"""

            This seems like a fresh install.

            Initializing new database based on {modules_list_filepath}.

            If this process gets interrupted you might have to delete the ddocs folder
            mentioned here: {modules_list_filepath}

            before re-running.

            Check out: https://github.com/gkegke/ddocs and looking for the
            python.txt section to understand what the file is intended for.
            """)
            self.getsave_new_modules(self.modules)
            print(f"""
            Add new libraries to {modules_list_filepath} and run ddocs.py --update
            to have those libraries data be tracked by ddocs.
            """)

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def modules_list(self, filepath):
        with open(filepath, "r") as f:
            return [line.strip() for line in f if not line.startswith("#")]

    def handle_module(self, module_name):
        try:
            module = importlib.import_module(module_name)
        except Exception as e:
            print(f"""
            module {module_name} doesn't seem to be installed on your system.

            The module has to be importable in the normal pythonic way
            for it to work with ddocs.

            e.g. as long as import {module_name} works in the interpreter or in a
            python file, then it should work here.

            Alternatively, you have made a spelling mistake when adding it in the
            languages/python.txt file.
            """)
            raise e

        mdoc = inspect.getdoc(module)
        mdata = self.get_entity_members(module, depth=0) if module else {}

        return {
            "doc": mdoc,
            "members": mdata
        }

    def get_entity_members(self, entity, depth):

        return {
            obj_mem: self.handle_entity(entity, obj_mem, depth)
            for obj_mem, _type in inspect.getmembers(entity)
            if callable(_type)
        }

    def handle_entity(self, thing, entity_name, depth=0):

        if depth > 1 or not callable(getattr(thing, entity_name)):
            return None

        obj = getattr(thing, entity_name)

        is_class = inspect.isclass(obj)
        doc = inspect.getdoc(obj)
        signature = ""
        _return = ""
        source_code = ""

        try:
            temp = inspect.signature(obj)
            if temp.return_annotation != inspect._empty:
                _return = str(temp.return_annotation)
            signature = str(temp)
        except (TypeError, ValueError):
            pass
        except Exception:
            return None

        try:
            source_code = inspect.getsource(obj)
        except Exception:
            pass

        mdata = {
            "name" : entity_name,
            "is_class": is_class,
            "doc": doc,
            "signature": signature,
            "return": _return,
            "source_code": source_code,
        }
        
        mdata["members"] = self.get_entity_members(obj, depth + 1)

        return mdata

    def get_data(self, modules=None):

        if modules is None:
            modules = self.modules

        mdata = {}

        for i, module in enumerate(modules, start=1):
            logging.info(f"Getting module: {i}/{len(modules)} {module}")
            mdata[module] = self.handle_module(module)

        logging.info(f"{len(mdata.keys())} modules data retrieved")

        return mdata

    def getsave_new_modules(self, modules_list):
        d = self.get_data(modules_list)
        modules = []
        entities = []
        m_id = self.dbm.get_next_module_id()
        e_id = self.dbm.get_next_entity_id()

        for module, mdata in d.items():
            try:
                modules.append((m_id, "Python", module, mdata.get("doc")))
                members = mdata.get("members", {})
            except Exception as e:
                print("module", module)
                print("mdata", mdata)
                raise e

            for ename, edata in members.items():

                if edata is None:
                    continue

                entities.append(self.create_entity(module, e_id, m_id, None, ename, edata))
                temp_e_id = e_id

                sub_members = edata.get("members", {})
                for sename, sedata in sub_members.items():

                    if sedata is None:
                        continue

                    e_id += 1
                    entities.append(self.create_entity(module, e_id, m_id, temp_e_id, sename, sedata))

                e_id += 1

            m_id += 1

        self.dbm.save_modules_and_entities(modules, entities)
    
    def create_entity(self, module, e_id, m_id, parent_e_id, ename, edata):
        try:
            return (
                e_id,
                m_id,
                parent_e_id,
                ename,
                int(edata["is_class"]),
                edata.get("doc"),
                str(edata["signature"]),
                edata.get("return", ""),
                edata.get("source_code", ""),
            )
        except Exception as e:
            print(f"An error occurred while processing entity {ename} in module {module}: {str(e)}")
            print(e_id, m_id, parent_e_id, ename, edata)
            return None

    def reset_database(self):
        # Drop the tables
        self.dbm.reset_db()

        logging.info("Reset complete.")

        # Insert modules and entities from the file
        self.update_database(self.modules_filepath)

        logging.info("Database reset and updated successfully.")


    def update_database(self, modules_filepath=None):

        if modules_filepath is None:
            modules_filepath = self.modules_filepath

        target_fp = os.path.join(modules_filepath, "languages", "python.txt")

        logging.info(f'''
        updating database based on {target_fp}...
        ''')

        # Read the module file
        modules_list = self.modules_list(target_fp)

        # Get the existing modules in the database
        existing_modules = self.dbm.get_all_modules()

        # Check for modules to delete
        modules_to_delete = list(set(existing_modules) - set(modules_list))
        modules_to_save = list(set(modules_list) - set(existing_modules))

        modules_to_delete.sort()
        modules_to_save.sort()

        if modules_to_delete:
            logging.info(f'''
            {len(modules_to_delete)} modules to be deleted
            ''')

            # Delete modules and related entities from the database
            for module in modules_to_delete:
                self.dbm.delete_module(module)

        if modules_to_save:
            logging.info(f'''
            {len(modules_to_save)} modules to be getsaved
            ''')
            self.getsave_new_modules(modules_to_save)

        logging.info(f'''
        finished updating database 
        ''')

    def update_module(self, module_name):

        # Check if the module exists in the file
        if module_name not in self.modules_list:
            logging.error(f"Module {module_name} not found in the module file.")
            sys.exit()

        logging.info(f'''
        updating module {module_name}
        ''')

        # Delete the module and its related entities from the database
        self.dbm.delete_module(module_name)

        # Insert the updated module and its entities into the database
        self.dbm.getsave_new_modules([module_name])

        logging.info(f'''
        finished updating module {module_name}
        ''')

    def list_all_modules(self):
        # Print a list of all modules
        modules = self.dbm.get_all_modules()
        for module in modules:
            print("- " + module)

    def module_starts_with(self, prefix):
        # Print a list of modules starting with the given prefix
        modules = self.dbm.get_module_starts_with(prefix) 

        if modules:
            for module in modules:
                logging.info("- " + module[0])
        else:
            print(f"No modules found beginning with {prefix}")

    def get_module(self, module_name):
        # Check if the module name exists in the modules table
        module = self.dbm.get_module(module_name)

        # If the module name does not exist, print an error message and exit
        if module is None:
            logging.error(f"Module {module_name} does not exist.")
            sys.exit()

        return module

    def print_module_doc(self, module_name, module_doc):
        # Print the module doc
        print(f"""Module {module_name}:

        {module_doc}

        """)

    def list_top_layer_entities(self, module_id):
        # Print all the entities that belong to the module and have no parent entity
        print("Entities:")
        entities = self.dbm.get_top_layer_entities(module_id)
        for id, name, is_class in entities:
            print(f"- {name} ({'class' if is_class else 'function'})")

    def get_entity(self, module_id, parent_entity_id, entity_name):
        # Check if the entity name exists in the entities table with the given module id and parent entity id

        entity = self.dbm.get_entity(module_id, parent_entity_id, entity_name)

        if entity is None:
            logging.error(f"Entity {entity_name} does not exist or is not a child of the previous entity.")
            sys.exit()

        return entity

    def print_entity_details(self, name, is_class, signature, return_, doc, source):
        # Print the entity details
        print(f'''
-----------------
Entity {name} ({'class' if is_class else 'function'}):

Signature: {signature}

Return: {return_}

Doc:

{doc}

Source:

{source}
----------------
        ''')

    def list_children_entities(self, module_id, parent_entity_id):
        # Print all the children entities of the final entity
        print("Children entities:")
        entities = self.dbm.get_children_entities(module_id, parent_entity_id)
        for _id, name, is_class in entities:
            print(f"- {name} ({'class' if is_class else 'function'})")

if __name__ == "__main__":

    from pprint import pprint
    import builtins

    m = ModulesManager("languages/python.txt")

    pprint(m.modules)
    print(len(m.modules))
