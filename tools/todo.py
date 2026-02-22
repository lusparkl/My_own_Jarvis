from services.local_db import get_table_values, delete_table_value, insert_into_table

def add_todo(title, description):
    """Use this to add todo to user's todo list.
  
    Args:
      title: Title of the task.
      description: Description of the task.

    Returns:
      Message with status of the creation.
    """
    insert_into_table("todo", title, description)
    return "Successfuly added new task!"

def get_todos():
    """Use this to get all current todos of the user to inform user about them/to get id of the todo to delete it
  
    Args:
      None.

    Returns:
      list with tuples(id, title, description)
    """
    return get_table_values("todo")

def delete_todo(id):
    """Use this to to delete outdated or fulfiled todo. Before use get_todos() to get id of the needed task.
  
    Args:
      id: ID of the task you want to delete. Use get_todos() to find it.

    Returns:
      None
    """
    delete_table_value("todo", id)