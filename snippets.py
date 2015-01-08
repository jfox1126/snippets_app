import psycopg2
import logging
import argparse
import sys

#Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")

def put(name, snippet):
  """Store a snippet with an associated name."""
  cursor = connection.cursor()
  with connection, connection.cursor() as cursor:
    try: 
      command = "insert into snippets values (%s, %s)"
      cursor.execute(command, (name, snippet))
    except psycopg2.IntegrityError as e:
      connection.rollback()
      command = "update snippets set message=%s where keyword=%s"
      cursor.execute(command, (snippet, name))
  logging.debug("Snippet stored successfully.")
  return name, snippet

def get(name):
  """Retrieve the snippet with a given name."""
  command = "select message from snippets where keyword=%s"
  with connection, connection.cursor() as cursor:
    cursor.execute(command, (name,))
    message = cursor.fetchone()
  if not message:
    logging.error("No snippet: " + name)
    print "No '" + name + "' in the database"
    sys.exit()
  logging.debug("Snippet retrieved successfully.")
  return message[0]

def update(name, snippet):
  """Update an existing snippet"""
  command = "update snippets set message=%s where keyword=%s"
  with connection, connection.cursor() as cursor:
    cursor.execute(command, (snippet, name))
    connection.commit()
  return name, snippet

def delete(name):
  """Delete an existing snippet"""
  command = "delete from snippets where keyword=%s"
  with connection, connection.cursor() as cursor:
    cursor.execute(command, (name,))
    connection.commit()
  return name

def catalog():
  """Return a list of all keywords"""
  with connection, connection.cursor() as cursor:
    cursor.execute("select * from snippets order by keyword")
    keywords = cursor.fetchall()
  return keywords

def search(string):
  """Search for a snippet containing a specific string"""
  with connection, connection.cursor() as cursor:
    cursor.execute("select * from snippets where message like '%{}%'".format(string))
    match = cursor.fetchall()
  return match

def main():
  """Main function"""
  logging.info("Constructing parser")
  parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
  
  subparsers = parser.add_subparsers(dest="command", help="Available commands")
  
  # Subparser for the put command
  logging.debug("Constructing put subparser")
  put_parser = subparsers.add_parser("put", help="Store a snippet")
  put_parser.add_argument("name", help="The name of the snippet")
  put_parser.add_argument("snippet", help="The snippet text")
  
  # Subparser for the get command
  logging.debug("Constructing get subparser")
  get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
  get_parser.add_argument("name", help="The name of the snippet to retrieve")
  
  # Subparser for update
  logging.debug("Constructing update subparser")
  update_parser = subparsers.add_parser("update", help="Update a snippet")
  update_parser.add_argument("name", help="The name of the snippet")
  update_parser.add_argument("snippet", help="The snippet text")
  
  # Subparser for delete
  logging.debug("Constructing delete subparser")
  delete_parser = subparsers.add_parser("delete", help="Delete a snippet")
  delete_parser.add_argument("name", help="The name of the snippet")
  
  # Subparser for catalog()
  logging.debug("Constructing catalog subparser")
  catalog_subparser = subparsers.add_parser("catalog", help="Returns full database")
  
  # Subparser for delete
  logging.debug("Constructing search subparser")
  delete_parser = subparsers.add_parser("search", help="Search for a string within a snippet")
  delete_parser.add_argument("string", help="The string to search for")
  
  arguments = parser.parse_args(sys.argv[1:])
  # Convert parsed arguments from Namespace to dictionary
  arguments = vars(arguments)
  command = arguments.pop("command") #could use arguments.get(command) instead. What's the value of pop()?

  if command == "put":
    name = arguments.get("name")
    snippet = arguments.get("snippet")
    name, snippet = put(name, snippet) #why can't I just run put(name, snippet)?
    print("Stored {!r} as {!r}".format(snippet, name))
  elif command == "get":
    name = arguments.get("name")
    name = get(name) 
    print("Retrieved snippet: {!r}".format(name))
  elif command == "update":
    name = arguments.get("name")
    snippet = arguments.get("snippet")
    name, snippet = update(name, snippet)
    print("Stored {!r} as {!r}".format(snippet, name))
  elif command == "delete":
    name = arguments.get("name")
    name = delete(name)
    print("Deleted {!r}".format(name))
  elif command == "catalog":
    keywords = catalog()
    print("This table has the following snippets:")
    for x in keywords:
      print x[0] + ": " + x[1]
  elif command == "search":
    string = arguments.get("string")
    match = search(string)
    print("The following snippets contain {!r}:".format(string))
    for x in match:
      print x[0] + ": " + x[1]

if __name__=="__main__":
  main()