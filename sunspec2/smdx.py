
"""
    Copyright (C) 2020 SunSpec Alliance

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included
    in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
    IN THE SOFTWARE.
"""

import os
import xml.etree.ElementTree as ET

import sunspec2.mdef as mdef

SMDX_ROOT = 'sunSpecModels'
SMDX_MODEL = mdef.MODEL
SMDX_BLOCK = 'block'
SMDX_POINT = 'point'
SMDX_ATTR_VERS = 'v'
SMDX_ATTR_ID = 'id'
SMDX_ATTR_LEN = 'len'
SMDX_ATTR_NAME = mdef.NAME
SMDX_ATTR_TYPE = mdef.TYPE
SMDX_ATTR_COUNT = mdef.COUNT
SMDX_ATTR_VALUE = mdef.VALUE
SMDX_ATTR_TYPE_FIXED = 'fixed'
SMDX_ATTR_TYPE_REPEATING = 'repeating'
SMDX_ATTR_OFFSET = 'offset'
SMDX_ATTR_MANDATORY = mdef.MANDATORY
SMDX_ATTR_ACCESS = mdef.ACCESS
SMDX_ATTR_SF = mdef.SF
SMDX_ATTR_UNITS = mdef.UNITS

SMDX_SYMBOL = 'symbol'
SMDX_COMMENT = 'comment'

SMDX_STRINGS = 'strings'
SMDX_ATTR_LOCALE = 'locale'
SMDX_LABEL = mdef.LABEL
SMDX_DESCRIPTION = 'description'
SMDX_NOTES = 'notes'
SMDX_DETAIL = mdef.DETAIL

SMDX_TYPE_INT16 = mdef.TYPE_INT16
SMDX_TYPE_UINT16 = mdef.TYPE_UINT16
SMDX_TYPE_COUNT = mdef.TYPE_COUNT
SMDX_TYPE_ACC16 = mdef.TYPE_ACC16
SMDX_TYPE_ENUM16 = mdef.TYPE_ENUM16
SMDX_TYPE_BITFIELD16 = mdef.TYPE_BITFIELD16
SMDX_TYPE_PAD = mdef.TYPE_PAD
SMDX_TYPE_INT32 = mdef.TYPE_INT32
SMDX_TYPE_UINT32 = mdef.TYPE_UINT32
SMDX_TYPE_ACC32 = mdef.TYPE_ACC32
SMDX_TYPE_ENUM32 = mdef.TYPE_ENUM32
SMDX_TYPE_BITFIELD32 = mdef.TYPE_BITFIELD32
SMDX_TYPE_IPADDR = mdef.TYPE_IPADDR
SMDX_TYPE_INT64 = mdef.TYPE_INT64
SMDX_TYPE_UINT64 = mdef.TYPE_UINT64
SMDX_TYPE_ACC64 = mdef.TYPE_ACC64
SMDX_TYPE_IPV6ADDR = mdef.TYPE_IPV6ADDR
SMDX_TYPE_FLOAT32 = mdef.TYPE_FLOAT32
SMDX_TYPE_STRING = mdef.TYPE_STRING
SMDX_TYPE_SUNSSF = mdef.TYPE_SUNSSF
SMDX_TYPE_EUI48 = mdef.TYPE_EUI48

SMDX_ACCESS_R = 'r'
SMDX_ACCESS_RW = 'rw'

SMDX_MANDATORY_FALSE = 'false'
SMDX_MANDATORY_TRUE = 'true'

smdx_access_types = {SMDX_ACCESS_R: mdef.ACCESS_R, SMDX_ACCESS_RW: mdef.ACCESS_RW}

smdx_mandatory_types = {SMDX_MANDATORY_FALSE: mdef.MANDATORY_FALSE, SMDX_MANDATORY_TRUE: mdef.MANDATORY_TRUE}

smdx_type_types = [
    SMDX_TYPE_INT16,
    SMDX_TYPE_UINT16,
    SMDX_TYPE_COUNT,
    SMDX_TYPE_ACC16,
    SMDX_TYPE_ENUM16,
    SMDX_TYPE_BITFIELD16,
    SMDX_TYPE_PAD,
    SMDX_TYPE_INT32,
    SMDX_TYPE_UINT32,
    SMDX_TYPE_ACC32,
    SMDX_TYPE_ENUM32,
    SMDX_TYPE_BITFIELD32,
    SMDX_TYPE_IPADDR,
    SMDX_TYPE_INT64,
    SMDX_TYPE_UINT64,
    SMDX_TYPE_ACC64,
    SMDX_TYPE_IPV6ADDR,
    SMDX_TYPE_FLOAT32,
    SMDX_TYPE_STRING,
    SMDX_TYPE_SUNSSF,
    SMDX_TYPE_EUI48
]

SMDX_PREFIX = 'smdx_'
SMDX_EXT = '.xml'


def to_smdx_filename(model_id):
    return '%s%05d%s' % (SMDX_PREFIX, int(model_id), SMDX_EXT)


def model_filename_to_id(filename):
    f = filename
    if '.' in f:
        f = os.path.splitext(f)[0]
    try:
        mid = int(f.rsplit('_', 1)[1])
    except ValueError:
        raise mdef.ModelDefinitionError('Error extracting model id from filename')

    return mid

'''
    smdx to json mapping:
    
      fixed block -> top level group
        model 'name' attribute -> group 'name'
        ID point is created for model ID and 'value' is the model ID value as a number
        L point is created for model len - model len has no value specified in the model definition
        fixed block points are placed in top level group
      repeating block -> group with count = 0 (indicates model len shoud be used to determine number of groups)
        repeating block 'name' -> group 'name', if no 'name' is defined 'name' = 'repeating'
    
      points:
        all type, access, and mandatory attributes are preserved
        point symbol map to the symbol object and placed in the symbols list for the point
          symbol 'name' attribute -> symbol object 'name'
          symbol element content -> symbol object 'value'
        strings 'label', 'description', 'notes' elements map to point attributes 'label', 'desc', 'detail'
'''


def from_smdx_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return(from_smdx(root))


def from_smdx(element):
    """ Sets the model type attributes based on an element tree model type
    element contained in an SMDX model definition.

    Parameters:

        element :
            Element Tree model type element.
    """

    model_def = {}

    m = element.find(SMDX_MODEL)
    if m is None:
        raise mdef.ModelDefinitionError('Model definition not found')
    try:
        mid = mdef.to_number_type(m.attrib.get(SMDX_ATTR_ID))
    except ValueError:
        raise mdef.ModelDefinitionError('Invalid model id: %s' % m.attrib.get(SMDX_ATTR_ID))

    name = m.attrib.get(SMDX_ATTR_NAME)
    if name is None:
        name = 'model_' + str(mid)
    model_def[mdef.NAME] = name

    strings = element.find(SMDX_STRINGS)

    # create top level group with ID and L points
    fixed_def = {mdef.NAME: name,
                 mdef.TYPE: mdef.TYPE_GROUP,
                 mdef.POINTS: [
                     {mdef.NAME: 'ID', mdef.VALUE: mid,
                      mdef.DESCRIPTION: 'Model identifier', mdef.LABEL: 'Model ID',
                      mdef.MANDATORY: mdef.MANDATORY_TRUE, mdef.STATIC: mdef.STATIC_TRUE, mdef.TYPE: mdef.TYPE_UINT16},
                     {mdef.NAME: 'L',
                      mdef.DESCRIPTION: 'Model length', mdef.LABEL: 'Model Length',
                      mdef.MANDATORY: mdef.MANDATORY_TRUE, mdef.STATIC: mdef.STATIC_TRUE, mdef.TYPE: mdef.TYPE_UINT16}
                 ]
                 }

    repeating_def = None

    fixed = None
    repeating = None
    for b in m.findall(SMDX_BLOCK):
        btype = b.attrib.get(SMDX_ATTR_TYPE, SMDX_ATTR_TYPE_FIXED)
        if btype == SMDX_ATTR_TYPE_FIXED:
            if fixed is not None:
                raise mdef.ModelDefinitionError('Duplicate fixed block type definition')
            fixed = b
        elif btype == SMDX_ATTR_TYPE_REPEATING:
            if repeating is not None:
                raise mdef.ModelDefinitionError('Duplicate repeating block type definition')
            repeating = b
        else:
            raise mdef.ModelDefinitionError('Invalid block type: %s' % btype)

    fixed_points_map = {}
    if fixed is not None:
        points = []
        for e in fixed.findall(SMDX_POINT):
            point_def = from_smdx_point(e)
            if point_def[mdef.NAME] not in fixed_points_map:
                fixed_points_map[point_def[mdef.NAME]] = point_def
                points.append(point_def)
            else:
                raise mdef.ModelDefinitionError('Duplicate point definition: %s' % point_def[mdef.NAME])
        if points:
            fixed_def[mdef.POINTS].extend(points)

    repeating_points_map = {}
    if repeating is not None:
        name = repeating.attrib.get(SMDX_ATTR_NAME)
        if name is None:
            name = 'repeating'
        repeating_def = {mdef.NAME: name, mdef.TYPE: mdef.TYPE_GROUP, mdef.COUNT: 0}
        points = []
        for e in repeating.findall(SMDX_POINT):
            point_def = from_smdx_point(e)
            if point_def[mdef.NAME] not in repeating_points_map:
                repeating_points_map[point_def[mdef.NAME]] = point_def
                points.append(point_def)
            else:
                raise mdef.ModelDefinitionError('Duplicate point definition: %s' % point_def[mdef.NAME])
        if points:
            repeating_def[mdef.POINTS] = points
        fixed_def[mdef.GROUPS] = [repeating_def]

    e = element.find(SMDX_STRINGS)
    if e.attrib.get(SMDX_ATTR_ID) == str(mid):
        m = e.find(SMDX_MODEL)
        if m is not None:
            for a in m.findall('*'):
                if a.tag == SMDX_LABEL and a.text:
                    fixed_def[mdef.LABEL] = a.text
                elif a.tag == SMDX_DESCRIPTION and a.text:
                    fixed_def[mdef.DESCRIPTION] = a.text
                elif a.tag == SMDX_NOTES and a.text:
                    fixed_def[mdef.DETAIL] = a.text
        for p in e.findall(SMDX_POINT):
            pid = p.attrib.get(SMDX_ATTR_ID)
            label = desc = notes = None
            for a in p.findall('*'):
                if a.tag == SMDX_LABEL and a.text:
                    label = a.text
                elif a.tag == SMDX_DESCRIPTION and a.text:
                    desc = a.text
                elif a.tag == SMDX_NOTES and a.text:
                    notes = a.text

            point_def = fixed_points_map.get(pid)
            if point_def is not None:
                if label:
                    point_def[mdef.LABEL] = label
                if desc:
                    point_def[mdef.DESCRIPTION] = desc
                if notes:
                    point_def[mdef.DETAIL] = notes
            point_def = repeating_points_map.get(pid)
            if point_def is not None:
                if label:
                    point_def[mdef.LABEL] = label
                if desc:
                    point_def[mdef.DESCRIPTION] = desc
                if notes:
                    point_def[mdef.DETAIL] = notes

    model_def = {'id': mid, 'group': fixed_def}
    return model_def


def from_smdx_point(element):
    """ Sets the point attributes based on an element tree point element
    contained in an SMDX model definition.

    Parameters:

        element :
            Element Tree point type element.

        strings :
            Indicates if *element* is a subelement of the 'strings'
            definintion within the model definition.
    """
    point_def = {}
    pid = element.attrib.get(SMDX_ATTR_ID)
    if pid is None:
        raise mdef.ModelDefinitionError('Missing point id attribute')
    point_def[mdef.NAME] = pid
    ptype = element.attrib.get(SMDX_ATTR_TYPE)
    if ptype is None:
        raise mdef.ModelDefinitionError('Missing type attribute for point: %s' % pid)
    elif ptype not in smdx_type_types:
        raise mdef.ModelDefinitionError('Unknown point type %s for point %s' % (ptype, pid))
    point_def[mdef.TYPE] = ptype
    plen = mdef.to_number_type(element.attrib.get(SMDX_ATTR_LEN))
    if ptype == SMDX_TYPE_STRING:
        if plen is None:
            raise mdef.ModelDefinitionError('Missing len attribute for point: %s' % pid)
        point_def[mdef.SIZE] = plen
    mandatory = element.attrib.get(SMDX_ATTR_MANDATORY, SMDX_MANDATORY_FALSE)
    if mandatory not in smdx_mandatory_types:
        raise mdef.ModelDefinitionError('Unknown mandatory type: %s' % mandatory)
    if mandatory == SMDX_MANDATORY_TRUE:
        point_def[mdef.MANDATORY] = smdx_mandatory_types.get(mandatory)
    access = element.attrib.get(SMDX_ATTR_ACCESS, SMDX_ACCESS_R)
    if access not in smdx_access_types:
        raise mdef.ModelDefinitionError('Unknown access type: %s' % access)
    if access == SMDX_ACCESS_RW:
        point_def[mdef.ACCESS] = smdx_access_types.get(access)
    units = element.attrib.get(SMDX_ATTR_UNITS)
    if units:
        point_def[mdef.UNITS] = units
    # if scale factor is an number, convert to correct type
    sf = mdef.to_number_type(element.attrib.get(SMDX_ATTR_SF))
    if sf is not None:
        point_def[mdef.SF] = sf
    # if scale factor is an number, convert to correct type
    value = mdef.to_number_type(element.attrib.get(SMDX_ATTR_VALUE))
    if value is not None:
        point_def[mdef.VALUE] = value

    symbols = []
    for e in element.findall('*'):
        if e.tag == SMDX_SYMBOL:
            sid = e.attrib.get(SMDX_ATTR_ID)
            value = e.text
            try:
                value = int(value)
            except ValueError:
                pass
            symbols.append({mdef.NAME: sid, mdef.VALUE: value})
    if symbols:
        point_def[mdef.SYMBOLS] = symbols

    return point_def


def indent(elem, level=0):
    i = os.linesep + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
