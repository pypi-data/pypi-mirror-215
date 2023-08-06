
import os
import sys

import pkg_resources
import platformdirs
import dearpygui.dearpygui as dpg

from ddocs.db import DatabaseManager

dbm = None

def text_toggle_button(title, text):
    displayed = f"{text}"
    limited = displayed if len(displayed) < 100 else displayed[:100] + "... Click to read more"

    dpg.add_text(title)

    dpg.add_button(
        label=limited,
        callback=change_label,
        user_data={
            "displayed" : displayed,
            "limited" : limited
        }
    )

def update_module_filter_results(sender, app_data):
    prefix = dpg.get_value("query")
    print("prefix", prefix)
    module_names = dbm.get_module_starts_with(prefix)
    clear_table("filtered_modules")
    for module_name in module_names:
        module_name = module_name[0]
        with dpg.table_row(parent="filtered_modules"):
            dpg.add_button(
                        label=module_name,
                        user_data=module_name,
                        callback=show_module
                    )

def create_module_filter_window():
    with dpg.window(label="Module filter", width=1200, height=1000, no_close=True):
        module_names = dbm.get_all_modules()
        dpg.add_input_text(
            label="Module name..",
            tag="query",
            callback=update_module_filter_results,
            default_value=""
        )
        with dpg.table(label="Modules", tag="filtered_modules", header_row=True):
            dpg.add_table_column(label="Name")
            for module_name in module_names:
                with dpg.table_row(parent="filtered_modules"):
                    dpg.add_button(
                        label=module_name,
                        user_data=module_name,
                        callback=show_module
                    )

def show_module(sender, app_data, module_name):
    module_id, module_doc = dbm.get_module(module_name)
    entities = dbm.get_top_layer_entities(module_id)

    with dpg.window(
        label=f"Module: {module_name}",
        width=500, height=1000,
    ):
        text_toggle_button(f"Doc:\n", f"{module_doc}")

        dpg.add_text("Child Entities:\n")

        for _id, name, is_class in entities:
            dpg.add_button(
                label=f"{name} - {'class' if is_class else 'function'}",
                user_data={
                    "module_id" : module_id,
                    "parent_entity_id" : None,
                    "entity_id" : _id,
                    "entity_name" : name,
                    "crumbs" : [f"Module: {module_name}"]
                },
                callback=show_entity
            )

def change_label(sender, app_data, user_data):
    current_label = dpg.get_item_label(sender)
    if current_label == user_data["displayed"]:
        new_label = user_data["limited"]
    else:
        new_label = user_data["displayed"]

    dpg.configure_item(sender, label=new_label)

def show_entity(sender, app_data, user_data):
    result = dbm.get_entity(
        user_data["module_id"],
        user_data["parent_entity_id"],
        user_data["entity_name"],
    )

    e_id, name, is_class, doc, signature, _return, source = result

    e = {
        "id" : e_id,
        "name" : name,
        "Type" : "Class" if is_class else "Function",
        "Doc" : doc,
        "Signature" : signature,
        "Return" : _return,
        "Source" : source
    }

    crumbs = user_data["crumbs"] + [f"{name} ({e['Type']})"]

    _label = " > ".join(crumbs)

    with dpg.window(
        label=_label,
        width=500, height=1000,
    ):
        for field in ("Type", "Doc", "Signature", "Return", "Source"):
            text_toggle_button(f"{field}:", e[field])

        dpg.add_text("Child Entities:\n")

        entities = dbm.get_children_entities(user_data["module_id"], e["id"])

        #dpg.add_table(label="Entity children", tag=f"entity_children_{e['id']}", header_row=True)
        for _id, name, is_class in entities:
            dpg.add_button(
                label=f"{name} - {'class' if is_class else 'function'}",
                user_data={
                    "module_id" : user_data["module_id"],
                    "parent_entity_id" : e["id"],
                    "entity_id": _id,
                    "entity_name" : name,
                    "crumbs" : user_data["crumbs"] + [name]
                },
                callback=show_entity
            )

def clear_table(table_tag):
    for tag in dpg.get_item_children(table_tag)[1]:
        dpg.delete_item(tag)

def main():
    
    ## initalize
    target_dir = platformdirs.user_config_dir("ddocs", "gkegke")

    if not os.path.exists(target_dir):
        print("""
        Please run ddocs once before using this gui.

        ddocs initializes a lot of useful configurations.
        """)
        
        sys.exit()

    # dirty, make gui a class in future
    global dbm
    dbm = DatabaseManager(os.path.join(target_dir,"ddocs.db"))

    ## core
    dpg.create_context()
    dpg.create_viewport(title='ddocs simple gui', width=1200, height=1000)

    with dpg.font_registry():
        font_folder = pkg_resources.resource_filename("ddocs", "fonts")
        font_path = os.path.join(font_folder, "OpenSans.ttf")
        default_font = dpg.add_font(font_path, 30)

    dpg.bind_font(default_font)

    create_module_filter_window()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":

    main()