#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3

class DatabaseManager:
    def __init__(self, dbfile):
        self._DBFILE = dbfile
        self.init_db()

    def init_db(self):
        queries = [
            """
            CREATE TABLE IF NOT EXISTS modules
            (
              id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
              language TEXT NOT NULL,
              name TEXT UNIQUE NOT NULL,
              doc TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS entities
            (
              entity_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
              module_id INTEGER NOT NULL,
              parent_entity_id INTEGER,
              name TEXT NOT NULL,
              is_class INTEGER NOT NULL,
              doc TEXT,
              signature TEXT,
              return TEXT,
              source TEXT,
              FOREIGN KEY(module_id) REFERENCES modules(id)
            );
            """
        ]

        with self.getDB() as con:
            for query in queries:
                self.execute_query(con, query)

    def execute_query(self, connection, query, parameters=None):
        with connection:
            cursor = connection.cursor()
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)

    def getDB(self):
        return sqlite3.connect(self._DBFILE)

    def reset_db(self):
        self.closeDB()
        if os.path.exists(self._DBFILE):
            os.remove(self._DBFILE)
        self.init_db()

    def closeDB(self):
        # Close the database connection if it's open
        self.getDB().close()

    def get_next_module_id(self):
        with self.getDB() as con:
            cursor = con.cursor()
            cursor.execute("SELECT MAX(id) FROM modules;")
            result = cursor.fetchone()[0]
            return result + 1 if result is not None else 1

    def get_next_entity_id(self):
        with self.getDB() as con:
            cursor = con.cursor()
            cursor.execute("SELECT MAX(entity_id) FROM entities;")
            result = cursor.fetchone()[0]
            return result + 1 if result is not None else 1

    def save_modules(self, modules_data):
        query = "INSERT INTO modules (id, language, name, doc) VALUES (?, ?, ?, ?)"

        with self.getDB() as con:
            cursor = con.cursor()
            cursor.executemany(query, modules_data)

    def save_entities(self, entities_data):
        query = """
        INSERT INTO entities
          (entity_id, module_id, parent_entity_id, name, is_class, doc,
           signature, return, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        with self.getDB() as con:
            cursor = con.cursor()
            cursor.executemany(query, entities_data)

    def save_module(self, _id, mname, mdoc):
        query = "INSERT INTO modules (name, doc) VALUES (?, ?)"

        with self.getDB() as con:
            cursor = con.cursor()
            cursor.execute(query, (mname, mdoc))
            _id = cursor.lastrowid

        return _id

    def save_entity(self, name, module_id, parent_entity_id, is_class, doc, signature, _return, source_code):
        query = """
        INSERT INTO entities
         (
           module_id,
           parent_entity_id,
           name,
           is_class,
           doc,
           signature,
           return,
           source
         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        with self.getDB() as con:
            cursor = con.cursor()
            cursor.execute(query, (module_id, parent_entity_id, name, is_class, doc, signature, _return, source_code))
            _id = cursor.lastrowid

        return _id

    def save_modules_and_entities(self, modules_data, entities_data):
        with self.getDB() as con:
            self.save_modules(modules_data)
            self.save_entities(entities_data)

    def save_module_and_entity(self, module_data, entity_data):
        module_id = self.save_module(*module_data)
        entity_data[1] = module_id
        entity_id = self.save_entity(*entity_data)
        return module_id, entity_id


    def get_all_modules(self):
        with self.getDB() as con:
            cur = con.cursor()
            cur.execute("SELECT name FROM modules")
            modules = cur.fetchall()
            return tuple(m[0] for m in modules)

    def delete_module(self, module_name):
        with self.getDB() as con:
            cursor = con.cursor()
            # Get the module ID
            cursor.execute("SELECT id FROM modules WHERE name=?", (module_name,))
            module_id = cursor.fetchone()

            if module_id is not None:
                # Delete entities associated with the module
                cursor.execute("DELETE FROM entities WHERE module_id=?", module_id)

                # Delete the module
                cursor.execute("DELETE FROM modules WHERE name=?", (module_name,))
                con.commit()
            else:
                print(f"Module '{module_name}' not found.")

    def get_module_starts_with(self, prefix):
        # Print a list of modules starting with the given prefix
        cur = self.getDB().cursor()
        cur.execute("SELECT name FROM modules WHERE name LIKE ? || '%'", (prefix,))
        modules = cur.fetchall()

        return modules

    def get_module(self, module_name):
        cur = self.getDB().cursor()
        cur.execute("SELECT id, doc FROM modules WHERE name = ?", (module_name,))
        module = cur.fetchone()

        return module

    def get_top_layer_entities(self, module_id):
        cur = self.getDB().cursor()
        cur.execute("SELECT entity_id, name, is_class FROM entities WHERE module_id = ? AND parent_entity_id IS NULL", (module_id,))
        entities = cur.fetchall()
        return entities
 
    def get_entity(self, module_id, parent_entity_id, entity_name):
        # Check if the entity name exists in the entities table with the given module id and parent entity id
        cur = self.getDB().cursor()
        if parent_entity_id is None:
            cur.execute(
                "SELECT entity_id, name, is_class, doc, signature, return, source FROM entities WHERE module_id = ? AND parent_entity_id IS NULL AND name = ?",
                (module_id, entity_name))
        else:
            cur.execute(
                "SELECT entity_id, name, is_class, doc, signature, return, source FROM entities WHERE module_id = ? AND parent_entity_id = ? AND name = ?",
                (module_id, parent_entity_id, entity_name))

        entity = cur.fetchone()

        return entity 

    def get_children_entities(self, module_id, parent_entity_id):
        cur = self.getDB().cursor()
        cur.execute("SELECT entity_id, name, is_class FROM entities WHERE module_id = ? AND parent_entity_id = ?", (module_id, parent_entity_id))
        entities = cur.fetchall()
        return entities
