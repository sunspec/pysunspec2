import json
import os

'''
1. JSON is used for the native encoding of information model definitions.
2. JSON can be used to represent the values associated with information model points at a specific point in time.

Python support for information models:
- Python model support is based on dictionaries and their afinity with JSON objects.

Model instance notes:

- If a model contains repeating groups, the group counts must be known to fully initialized the model. If fields are
  accessed that depend on group counts that have not been initialized, a ModelError exception is generated.
- Points that have not been read or written contain a value of None.
- If a point that can not be changed from the initialized value is changed, a ModelError exception is generated.

A model definition is represented as a dictionary using the constants defined in this file as the entry keys.

A model definition is required to have a single top level group.

A model dict
  - must contain: 'id' and 'group'

A group dict
  - must contain: 'name', 'type', 'points'
  - may contain: 'count', 'groups', 'label', 'description', 'notes', 'comments'

A point dict
  - must contain: 'name', 'type'
  - may contain: 'count', 'size', 'sf', 'units', 'mandatory', 'access', 'symbols', 'label', 'description', 'notes',
                 'comments'

A symbol dict
  - must contain: 'name', 'value'
  - may contain: 'label', 'description', 'notes', 'comments'

Example:
  model_def = {
    'id': 123,
    'group': {
      'id': model_name,
      'groups': [],
      'points': []
  }
'''

DEVICE = 'device'            # device (device dict) ### currently not in the spec
MODEL = 'model'              # model (model dict) ### currently not in the spec
GROUP = 'group'              # top level model group (group dict)
GROUPS = 'groups'            # groups in group (list of group dicts)
POINTS = 'points'            # points in group (list of point dicts)

ID = 'id'                    # id (int or str)
NAME = 'name'                # name (str)
VALUE = 'value'              # value (int, float, str)
COUNT = 'count'              # instance count (int or str)

TYPE = 'type'                # point type (str of TYPE_XXX)
MANDATORY = 'mandatory'      # point mandatory (str of MANDATORY_XXX)
ACCESS = 'access'            # point access (str of ACCESS_XXX)
STATIC = 'static'            # point value is static (str of STATIC_XXX)
SF = 'sf'                    # point scale factor (int)
UNITS = 'units'              # point units (str)
SIZE = 'size'                # point string length (int)

LABEL = 'label'              # label (str)
DESCRIPTION = 'desc'         # description (str)
NOTES = 'notes'              # notes (str)
DETAIL = 'detail'            # detailed description (str)
SYMBOLS = 'symbols'          # symbols (list of symbol dicts)
COMMENTS = 'comments'        # comments (list of str)

TYPE_GROUP = 'group'
TYPE_SYNC_GROUP = 'sync'

TYPE_INT16 = 'int16'
TYPE_UINT16 = 'uint16'
TYPE_COUNT = 'count'
TYPE_ACC16 = 'acc16'
TYPE_ENUM16 = 'enum16'
TYPE_BITFIELD16 = 'bitfield16'
TYPE_PAD = 'pad'
TYPE_INT32 = 'int32'
TYPE_UINT32 = 'uint32'
TYPE_ACC32 = 'acc32'
TYPE_ENUM32 = 'enum32'
TYPE_BITFIELD32 = 'bitfield32'
TYPE_IPADDR = 'ipaddr'
TYPE_INT64 = 'int64'
TYPE_UINT64 = 'uint64'
TYPE_ACC64 = 'acc64'
TYPE_IPV6ADDR = 'ipv6addr'
TYPE_FLOAT32 = 'float32'
TYPE_FLOAT64 = 'float64'
TYPE_STRING = 'string'
TYPE_SUNSSF = 'sunssf'
TYPE_EUI48 = 'eui48'

ACCESS_R = 'R'
ACCESS_RW = 'RW'

MANDATORY_FALSE = 'O'
MANDATORY_TRUE = 'M'

STATIC_FALSE = 'D'
STATIC_TRUE = 'S'

MODEL_ID_POINT_NAME = 'ID'
MODEL_LEN_POINT_NAME = 'L'

END_MODEL_ID = 65535

MODEL_DEF_EXT = '.json'


def to_int(x):
    try:
        return int(x, 0)
    except TypeError:
        return int(x)


def to_str(s):
    return str(s)


def to_float(f):
    try:
        return float(f)
    except ValueError:
        return None


# valid model attributes
model_attr = {ID: {'type': int, 'mand': True}, GROUP: {'mand': True}, COMMENTS: {}}

# valid group attributes
group_attr = {NAME: {'type': str, 'mand': True}, COUNT: {'type': [int, str]}, TYPE: {'mand': True},
              GROUPS: {}, POINTS: {'mand': True}, LABEL: {'type': str},
              DESCRIPTION: {'type': str}, NOTES: {'type': str}, COMMENTS: {}, DETAIL: {'type': str}}

# valid point attributes
point_attr = {NAME: {'type': str, 'mand': True}, COUNT: {'type': int}, VALUE: {}, TYPE: {'mand': True},
              SIZE: {'type': int}, SF: {}, UNITS: {'type': str},
              ACCESS: {'type': str, 'values': ['R', 'RW'], 'default': 'R'},
              MANDATORY: {'type': str, 'values': ['O', 'M'], 'default': 'O'},
              STATIC: {'type': str, 'values': ['D', 'S'], 'default': 'D'},
              LABEL: {'type': str}, DESCRIPTION: {'type': str}, NOTES: {'type': str}, SYMBOLS: {}, COMMENTS: {},
              DETAIL: {'type': str}}

# valid symbol attributes
symbol_attr = {NAME: {'type': str, 'mand': True}, VALUE: {'mand': True}, LABEL: {'type': str},
               DESCRIPTION: {'type': str}, NOTES: {'type': str}, COMMENTS: {}, DETAIL: {'type': str}}

group_types = [TYPE_GROUP, TYPE_SYNC_GROUP]

point_type_info = {
    TYPE_INT16: {'len': 1, 'to_type': to_int, 'default': 0},
    TYPE_UINT16: {'len': 1, 'to_type': to_int, 'default': 0},
    TYPE_COUNT: {'len': 1, 'to_type': to_int, 'default': 0},
    TYPE_ACC16: {'len': 1, 'to_type': to_int, 'default': 0},
    TYPE_ENUM16: {'len': 1, 'to_type': to_int, 'default': 0},
    TYPE_BITFIELD16: {'len': 1, 'to_type': to_int, 'default': 0},
    TYPE_PAD: {'len': 1, 'to_type': to_int, 'default': 0},
    TYPE_INT32: {'len': 2, 'to_type': to_int, 'default': 0},
    TYPE_UINT32: {'len': 2, 'to_type': to_int, 'default': 0},
    TYPE_ACC32: {'len': 2, 'to_type': to_int, 'default': 0},
    TYPE_ENUM32: {'len': 2, 'to_type': to_int, 'default': 0},
    TYPE_BITFIELD32: {'len': 2, 'to_type': to_int, 'default': 0},
    TYPE_IPADDR: {'len': 2, 'to_type': to_int, 'default': 0},
    TYPE_INT64: {'len': 4, 'to_type': to_int, 'default': 0},
    TYPE_UINT64: {'len': 4, 'to_type': to_int, 'default': 0},
    TYPE_ACC64: {'len': 4, 'to_type': to_int, 'default': 0},
    TYPE_IPV6ADDR: {'len': 8, 'to_type': to_str, 'default': 0},
    TYPE_FLOAT32: {'len': 2, 'to_type': to_float, 'default': 0},
    TYPE_FLOAT64: {'len': 4, 'to_type': to_float, 'default': 0},
    TYPE_STRING: {'len': None, 'to_type': to_str, 'default': ''},
    TYPE_SUNSSF: {'len': 1, 'to_type': to_int, 'default': 0},
    TYPE_EUI48: {'len': 4, 'to_type': to_str, 'default': 0}
}


class ModelDefinitionError(Exception):
    pass


def to_number_type(n):
    if isinstance(n, str):
        try:
            n = int(n)
        except ValueError:
            try:
                n = float(n)
            except ValueError:
                pass
    return n


def validate_find_point(group, pname):
    points = group.get(POINTS, list())
    for p in points:
        pxname = p.get(NAME)
        if pxname:
            if p[NAME] == pname:
                return p


def validate_attrs(element, attrs, result=''):
    # check for unexpected attributes
    for k in element:
        if k not in attrs:
            result += 'Unexpected model definition attribute: %s in %s\n' % (k, element.get(NAME))
    # check for missing attributes
    for k, a in attrs.items():
        if k in element and element[k] is not None:
            # check type if specified
            t = a.get('type')
            if isinstance(t, list):
                if t and type(element[k]) not in t:
                    result += 'Unexpected type for model attribute %s, expected %s, found %s\n' % \
                              (k, t, type(element[k]))
            else:
                if t and type(element[k]) != t:
                    result += 'Unexpected type for model attribute %s, expected %s, found %s\n' % (k, t, type(element[k]))
            values = a.get('values')
            if values and element[k] not in values:
                result += 'Unexpected value for model attribute %s: %s\n' % (k, element[k])
        elif a.get('mand', False):
            result += 'Mandatory attribute missing from model definition: %s\n' % k
    return result


def validate_group_point_dup(group, result=''):
    groups = group.get(GROUPS, list())
    for g in groups:
        gname = g.get(NAME)
        if gname:
            count = 0
            for gx in groups:
                gxname = gx.get(NAME)
                if gxname:
                    if gx[NAME] == gname:
                        count += 1
            if count > 1:
                result += 'Duplicate group id %s in group %s' % (gname, group[NAME])
            if validate_find_point(group, gname):
                result += 'Duplicate group and point id %s in group %s' % (gname, group[NAME])
        else:
            result += 'Mandatory %s attribute missing in group definition element\n' % (NAME)
    points = group.get(POINTS, list())
    for p in points:
        pname = p.get(NAME)
        if pname:
            count = 0
            for px in points:
                pxname = px.get(NAME)
                if pxname:
                    if px[NAME] == pname:
                        count += 1
            if count > 1:
                result += 'Duplicate point id %s in group %s' % (pname, group[NAME])
        else:
            result += 'Mandatory attribute missing in point definition element: %s\n' % (NAME)
    return result


def validate_symbols(symbols, model_group, result=''):
    for symbol in symbols:
        result = validate_attrs(symbol, model_group, result)
    return result


def validate_sf(point, sf, sf_groups, result=''):
    found = False
    if type(sf) == str:
        for group in sf_groups:
            p = validate_find_point(group, sf)
            if p:
                found = True
                if p[TYPE] != TYPE_SUNSSF:
                    result += 'Scale factor %s for point %s is not scale factor type: %s\n' % (sf, point[NAME], p[TYPE])
                break
        if not found:
            result += 'Scale factor %s for point %s not found\n' % (sf, point[NAME])
    elif type(sf) == int:
        if sf < - 10 or sf > 10:
            result += 'Scale factor %s for point %s out of range\n' % (sf, point[NAME])
    else:
        result += 'Scale factor %s for point %s has invalid type %s\n' % (sf, point[NAME], type(sf))
    return result


def validate_point_def(point, model_group, group, result=''):
    # validate general point attributes
    result = validate_attrs(point, point_attr, result)
    # validate point type
    ptype = point.get(TYPE)
    if ptype not in point_type_info:
        result += 'Unknown point type %s for point %s\n' % (ptype, point[NAME])
    # validate scale foctor, if present
    sf = point.get(SF)
    if sf:
        result = validate_sf(point, sf, [model_group, group], result)
    # validate symbols
    symbols = point.get(SYMBOLS, list())
    result = validate_symbols(symbols, symbol_attr, result)
    # check for duplicate symbols
    for s in symbols:
        sname = s.get(NAME)
        if sname:
            count = 0
            for sx in symbols:
                if sx[NAME] == sname:
                    count += 1
            if count > 1:
                result += 'Duplicate symbol id %s in point %s\n' % (sname, point[NAME])
        else:
            result += 'Mandatory attribute missing in symbol definition element: %s\n' % (NAME)
    return result


def validate_group_def(group, model_group, result=''):
    # validate general group attributes
    result = validate_attrs(group, group_attr, result)
    # validate points
    points = group.get(POINTS, list())
    for p in points:
        result = validate_point_def(p, model_group, group, result)
    # validate groups
    groups = group.get(GROUPS, list())
    for g in groups:
        result = validate_group_def(g, model_group, result)
    # check for group and point duplicates
    result = validate_group_point_dup(group, result)
    return result


def validate_model_group_def(model_def, group, result=''):
    # must contain ID and length points
    points = group.get(POINTS)
    if points:
        if len(points) >= 2:
            pname = points[0].get(NAME)
            if pname != MODEL_ID_POINT_NAME:
                result += "First point in top-level group must be %s, found: %s\n" % (MODEL_ID_POINT_NAME, pname)
            if points[0].get(VALUE) != model_def.get(ID):
                result += 'Model ID does not match top-level group ID: %s %s %s %s\n' % (
                    model_def.get(ID), type(model_def.get(ID)), points[0].get(VALUE), type(points[0].get(VALUE)))
            pname = points[1].get(NAME)
            if pname != MODEL_LEN_POINT_NAME:
                result += "Second point in top-level group must be %s, found: %s\n" % (MODEL_LEN_POINT_NAME, pname)
        else:
            result += "Top-level group must contain at least two points: %s and %s\n" % (MODEL_ID_POINT_NAME,
                                                                                         MODEL_LEN_POINT_NAME)
    else:
        result += 'Top-level group missing point definitions\n'
    # perform normal group validation
    result = validate_group_def(group, group, result)
    return result


def validate_model_def(model_def, result=''):
    result = validate_attrs(model_def, model_attr, result)
    group = model_def.get(GROUP)
    result = validate_model_group_def(model_def, group, result)
    return result


def from_json_str(s):
    return json.loads(s)


def from_json_file(filename):
    f = open(filename)
    model_def = json.load(f)
    f.close()
    return(model_def)


def to_json_str(model_def, indent=4):
    return json.dumps(model_def, indent=indent, sort_keys=True)


def to_json_filename(model_id):
    return 'model_%s%s' % (model_id, MODEL_DEF_EXT)


def model_filename_to_id(filename):
    f = filename
    if '.' in f:
        f = os.path.splitext(f)[0]
    try:
        mid = int(f.rsplit('_', 1)[1])
    except ValueError:
        raise ModelDefinitionError('Error extracting model id from filename')

    return mid


def to_json_file(model_def, filename=None, filedir=None, indent=4):
    if filename is None:
        filename = to_json_filename(model_def[ID])
        if filedir is not None:
            filename = os.path.join(filedir, filename)
    f = open(filename, 'w')
    json.dump(model_def, f, indent=indent, sort_keys=True)


def get_group_len_points(group_def, points=None):
    if points is None:
        points = []
    groups = group_def.get(GROUPS)
    if groups:
        for g in groups:
            count = g.get(COUNT)
            if count:
                try:
                    count = int(count)
                except:
                    if count not in points:
                        points.append(count)
            points = get_group_len_points(g, points)
    return points


def get_group_len_points_index(group_def):
    index = pindex = 0
    if group_def:
        len_points = get_group_len_points(group_def)
        if len_points:
            points = group_def.get(POINTS, list())
            for p in points:
                name = p.get(NAME)
                plen = point_type_info.get(p.get(TYPE)).get('len')
                if plen is None:
                    plen = point_type_info.get(p.get(SIZE))
                if not plen:
                    ModelDefinitionError('Unable to get size of point %s' % name)
                pindex += plen
                if name in len_points:
                    index = pindex
                    len_points.remove(name)
                if not len_points:
                    break
            if len_points:
                raise ModelDefinitionError('Expected points not found in group definition: %s' % len_points)
    return index



if __name__ == "__main__":

    model_def = from_json_file('./models/json/model_711.json')
    print(get_group_len_points_index(model_def.get(GROUP)))
