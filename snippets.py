import logging

#Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
  """
  Store a snippet with an associated name.

  Returns the name and the snippet
  """
  logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
  return name, snippet

def get(name):
  """Retrieve the snippet with a given name.

  If there is no such snippet, returns false

  Returns the snippet.
  """
  logging.error("FIXME: Unimplemented - get({!r})".format(name))
  return ""

def update(name, snippet):
  """
  Update an existing snippet
  
  Returns the name and the new value of the snippet
  """
  logging.error("FIXME: Unimplemented - update({!r}, {!r})".format(name, snippet))
  return name, snippet

def delete(name):
  """
  Delete an existing snippet
  
  Confirms that a snippet was deleted
  """
  logging.error("FIXME: Unimplemented - delete({!r})".format(name))
  return ""