"""
The function below returns all of the information needed in a list of rows,
each row representing a unique object
"""
from contextlib import closing
from sqlite3 import connect
import sys



#----------------------------------------------------------#

# The function below returns all of the information needed in a list of rows,
# each row representing a unique object

# A function that connects to the database
def get_rows(label=None, department=None, agent=None, classifier=None):
    """
     A function that connects to the database
    """
    try:
        with connect('lux.sqlite', isolation_level=None, uri=True) as connection:
            with closing(connection.cursor()) as cursor:
                #Query
                query = "SELECT objects.id, objects.label, \
                objects.date \
                FROM objects \
                INNER JOIN productions ON objects.id = productions.obj_id \
                INNER JOIN agents ON productions.agt_id = agents.id \
                INNER JOIN objects_departments ON objects.id = objects_departments.obj_id \
                INNER JOIN departments ON objects_departments.dep_id = departments.id \
                INNER JOIN objects_classifiers ON objects.id = objects_classifiers.obj_id \
                INNER JOIN classifiers ON objects_classifiers.cls_id = classifiers.id \
                WHERE (label LIKE ? OR ? IS NULL) \
                AND (departments.name LIKE ? OR ? IS NULL) \
                AND (agents.name LIKE ? OR ? IS NULL) \
                AND (classifiers.name LIKE ? OR ? IS NULL) \
                GROUP BY objects.id \
                ORDER BY objects.label ASC, objects.date ASC, agents.name ASC,\
                productions.part ASC, classifiers.name ASC \
                LIMIT 1000"
                params = (f"%{label}%", label, f"%{department}%",
                department, f"%{agent}%", agent, f"%{classifier}%", classifier)
                cursor.execute(query, params)
                rows = cursor.fetchall()
                if len(rows) == 0:
                    print("No Results")
                table = []
                sizes = {key: 0 for key in ['id', 'label', 'date',
                'agents', 'classifiers']}
                # keys = id, label, date, agents, classifiers
                for row in rows:
                    new_row = []
                    # id
                    new_row.append(row[0])
                    sizes['id'] = max(sizes['id'], len(str(row[0])))
                    # label
                    new_row.append(row[1])
                    sizes['label'] = max(sizes['label'], len(str(row[1])))
                    # date
                    new_row.append(row[2])
                    sizes['date'] = max(sizes['date'], len(str(row[2])))
                    # comma separated list of agents
                    query, params = find_agents(row[0])
                    cursor.execute(query, params)
                    agents = cursor.fetchall()[0][0]
                    new_row.append(agents)
                    sizes['agents'] = max(sizes['agents'], len(str(agents)))
                    # comma separated list of classifiers
                    query, params = find_classifiers(row[0])
                    cursor.execute(query, params)
                    classifiers = cursor.fetchall()[0][0]
                    new_row.append(classifiers)
                    sizes['classifiers'] = max(sizes['classifiers'], len(str(classifiers)))
                    table.append(tuple(new_row))
                return table, sizes
    except Exception as err:
        print(err, file=sys.stderr)
        sys.exit(1)

#----------------------------------------------------------#


# the function below returns the label, produced by information,
# classification, and information in a list
# Each query is done separately for clarity
def get_object(obj_id):
    """
    Connect to database and get the objects details
    """
    try:
        with connect("lux.sqlite", isolation_level=None,uri=True) as connection:
            with closing(connection.cursor()) as cursor:

                # Object information query
                object_info_query = "SELECT objects.accession_no, \
                objects.label, objects.date, places.label AS place \
                        FROM objects \
                        LEFT JOIN objects_places ON objects.id = objects_places.obj_id \
                        LEFT JOIN places ON objects_places.pl_id = places.id \
                        WHERE objects.id = ?"

                cursor.execute(object_info_query, (obj_id,))
                object_info = cursor.fetchall()
                # Get the object's produced by details
                produced_by_query = "SELECT part, name, begin_date, end_date, descriptor\
                FROM productions \
                INNER JOIN agents ON productions.agt_id=agents.id \
                INNER JOIN agents_nationalities ON agents_nationalities.agt_id=agents.id \
                INNER JOIN nationalities ON nationalities.id=agents_nationalities.nat_id \
                WHERE obj_id=?"
                cursor.execute(produced_by_query, (obj_id,))
                produced_by_details = cursor.fetchall()

                # Get the object's classification
                classification_query = "SELECT GROUP_CONCAT(DISTINCT classifiers.name)\
                FROM classifiers INNER JOIN objects_classifiers \
                ON classifiers.id=objects_classifiers.cls_id WHERE obj_id=?"
                cursor.execute(classification_query, (obj_id,))
                classification_details = cursor.fetchall()

                # Get information
                information_query = 'SELECT type, content FROM "references" WHERE obj_id=?'
                cursor.execute(information_query, (obj_id,))
                info = cursor.fetchall()
                if len(info) == 0:
                    print("No Results")
                    sys.exit()

                # create a dictionary to store the values, label, produced deetail,
                # classification and info
                # The keys used will be label, produced, class, and info
                # This will make accessing the data easier
                all_info = {}
                all_info["object_info"] = object_info
                all_info["produced"] = produced_by_details
                all_info["class"] = classification_details
                all_info["info"] = info
                return all_info
    except Exception as err:
        print(err, file=sys.stderr)
        sys.exit(1)

def find_classifiers(ob_id):
    """
    Classifiers query
    """
    query = "SELECT GROUP_CONCAT(classifiers.name) FROM classifiers\
            INNER JOIN objects_classifiers ON classifiers.id = objects_classifiers.cls_id\
            WHERE objects_classifiers.obj_id = ?"
    params = (ob_id,)
    return (query, params)

def find_agents(ob_id):
    """
    agents query
    """
    query = "SELECT GROUP_CONCAT(agents.name || ' (' || productions.part || ')') AS agent_part\
    FROM agents\
    INNER JOIN productions ON agents.id = productions.agt_id\
    INNER JOIN objects ON productions.obj_id = objects.id\
    WHERE objects.id = ?\
    ORDER BY agents.name ASC, productions.part ASC"
    params = (ob_id,)
    return (query, params)
