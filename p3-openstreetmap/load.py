# Adapted from Case Study Lesson "Preparing for the Database"

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
import sqlite3

import cerberus

import schema #as in "schema.py", NOT the schema module

OSM_PATH = "M:\data\UdacityOSM\denver_sample.osm"
FULL_OSM_PATH = "M:\data\UdacityOSM\denver-boulder_colorado.osm"
DB_PATH = "denver_sample.db"
FULL_DB_PATH = "M:\data\UdacityOSM\denver.db"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

CSV_PATHS = [NODES_PATH, NODE_TAGS_PATH, WAYS_PATH, WAY_NODES_PATH, WAY_TAGS_PATH]

SCHEMA = schema.schema #references schema.py as well as sheham

LOWER = re.compile(r'^([a-z]|_)*$')
LOWER_COLON = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODES_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAYS_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_node_tag(node_id, tag_el):
    '''create and return a dictionary with node information'''
    tag_key = tag_el.attrib['k']
    tag_type = 'regular'
    if PROBLEMCHARS.search(tag_key):
        return None
    if LOWER_COLON.search(tag_key):
        tag_type, tag_key = tag_key.split(':', 1)
    tag_val = tag_el.attrib['v']

    if tag_type == 'addr' and tag_key == 'postcode':
        tag_val = fix_postcode(tag_val)
    if tag_type == 'addr' and tag_key == 'state':
        tag_val = fix_state(tag_val)

    d = {'id': node_id, 'key': tag_key, 'value': tag_val, 'type': tag_type}
    return d
    


def shape_element(element, node_attr_fields=NODES_FIELDS, way_attr_fields=WAYS_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    if element.tag == 'node':
        node_dict = {}
        node_dict['id'] = element.attrib['id']
        node_dict['user'] = element.attrib['user']
        node_dict['uid'] = element.attrib['uid']
        node_dict['version'] = element.attrib['version']
        node_dict['lat'] = element.attrib['lat']
        node_dict['lon'] = element.attrib['lon']
        node_dict['timestamp'] = element.attrib['timestamp']
        node_dict['changeset'] = element.attrib['changeset']

        node_tags = []
        for child in element:
            if child.tag == 'tag':
                child_info = shape_node_tag(element.attrib['id'], child)
                if child_info:
                    node_tags.append(child_info)

        return {'node': node_dict, 'node_tags': node_tags}


    elif element.tag == 'way':
        way_dict = {}
        way_dict['id'] = element.attrib['id']
        way_dict['user'] = element.attrib['user']
        way_dict['uid'] = element.attrib['uid']
        way_dict['version'] = element.attrib['version']
        way_dict['timestamp'] = element.attrib['timestamp']
        way_dict['changeset'] = element.attrib['changeset']

        way_tags = []
        way_nodes = []
        position = 0
        for child in element:
            if child.tag == 'tag':
                child_info = shape_node_tag(element.attrib['id'], child)
                if child_info:
                    way_tags.append(child_info)
            elif child.tag == 'nd':
                nd_dict = {}
                nd_dict['id'] = element.attrib['id']
                nd_dict['node_id'] = child.attrib['ref']
                nd_dict['position'] = position
                way_nodes.append(nd_dict)
                position += 1

        return {'way': way_dict, 'way_nodes': way_nodes, 'way_tags': way_tags}

def is_denver_postcode(zip):
    zip = int(zip)
    if (zip > 80000) and (zip < 80700):
        return True
    return False

def fix_postcode(tag_val):
    ZIP = re.compile((r'^[0-9]{5}$'))
    ZIPPLUSFOUR = re.compile((r'^([0-9]{5})-[0-9]{4}$'))
    COZIP = re.compile((r'^CO\s*([0-9]{5})$'))
    if ZIP.search(tag_val):
        if is_denver_postcode(tag_val):
            return tag_val
        else:
            print "Unexpected ZIP:", tag_val
            return tag_val
    elif ZIPPLUSFOUR.search(tag_val):
        zip = ZIPPLUSFOUR.search(tag_val).group(1)
        if is_denver_postcode(zip):
            return zip
        else:
            print "Unexpected ZIP:", tag_val
            return zip
    elif COZIP.search(tag_val):
        zip = COZIP.search(tag_val).group(1)
        if is_denver_postcode(zip):
            return zip
        else:
            print "Unexpected ZIP:", tag_val
            return zip
    else:
        print "Invalid ZIP:", tag_val
        return tag_val

def fix_state(tag_val):
    if tag_val != 'CO':
        return 'CO'
    return tag_val


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)

        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODES_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAYS_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


def load_db(osm_file, db_file, validate=False):
    '''New for Project
    Runs process_map() to create csv files with the osm data
    Deletes all tables from the database and rebuilds using the new csv files'''
    process_map(osm_file, validate)
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Drop all tables
    tables = c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in tables.fetchall():
        command = "DROP TABLE IF EXISTS {};".format(table[0])
        print command
        c.execute(command)
    conn.commit()

    # Create tables according to schema.sql
    with open('schema.sql', 'r') as createtables:
        c.executescript(createtables.read())
    conn.commit()

    # Populate the tables
    tables = c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in tables.fetchall():
        data_fn = eval(table[0].upper()+"_PATH")
        print "Loading data from: ", data_fn
        with open(data_fn, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                command = "INSERT INTO {} VALUES (".format(table[0]) + "?,"*len(row) 
                command = command[:-1] + ");"
                values = []
                for k in eval(table[0].upper()+"_FIELDS"):
                    values.append(unicode(row[k], 'utf-8'))
                values = tuple(values)
                c.execute(command, values)
        conn.commit()


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    # process_map(OSM_PATH, validate=False)

    # load_db(OSM_PATH, DB_PATH)

    load_db(FULL_OSM_PATH, FULL_DB_PATH)