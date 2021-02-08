
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

import csv
import json
import copy

import sunspec2.mdef as mdef

ADDRESS_OFFSET = 'Address Offset'
GROUP_OFFSET = 'Group Offset'
NAME = 'Name'
VALUE = 'Value'
COUNT = 'Count'
TYPE = 'Type'
SIZE = 'Size'
SCALE_FACTOR = 'Scale Factor'
UNITS = 'Units'
ACCESS = 'RW Access (RW)'
MANDATORY = 'Mandatory (M)'
STATIC = 'Static (S)'
LABEL = 'Label'
DESCRIPTION = 'Description'
NOTES = 'Notes'

columns = [ADDRESS_OFFSET, GROUP_OFFSET, NAME, VALUE, COUNT, TYPE, SIZE, SCALE_FACTOR,
           UNITS, ACCESS, MANDATORY, STATIC, LABEL, DESCRIPTION, NOTES]

empty_row = [''] * len(columns)

ADDRESS_OFFSET_IDX = columns.index(ADDRESS_OFFSET)
GROUP_OFFSET_IDX = columns.index(GROUP_OFFSET)
NAME_IDX = columns.index(NAME)
VALUE_IDX = columns.index(VALUE)
COUNT_IDX = columns.index(COUNT)
TYPE_IDX = columns.index(TYPE)
SIZE_IDX = columns.index(SIZE)
SCALE_FACTOR_IDX = columns.index(SCALE_FACTOR)
UNITS_IDX = columns.index(UNITS)
ACCESS_IDX = columns.index(ACCESS)
MANDATORY_IDX = columns.index(MANDATORY)
STATIC_IDX = columns.index(STATIC)
LABEL_IDX = columns.index(LABEL)
DESCRIPTION_IDX = columns.index(DESCRIPTION)
NOTES_IDX = columns.index(NOTES)


def idx(row, attr, mandatory=False):
    try:
        return row.index(attr)
    except:
        if mandatory:
            raise ValueError('Missing required attribute column: %s' % (attr))


def row_is_empty(row, idx):
    for e in row[idx:]:
        if e is not None and e != '':
            return False
    return True


def find_name(entities, name):
    for e in entities:
        if e[mdef.NAME] == name:
            return e


def element_type(row):
    type_idx = idx(row, TYPE, mandatory=True)


def from_spreadsheet(spreadsheet):
    model_def = {}
    row = spreadsheet[0]
    address_offset_idx = idx(row, ADDRESS_OFFSET)
    group_offset_idx = idx(row, GROUP_OFFSET)
    name_idx = idx(row, NAME, mandatory=True)
    value_idx = mdef.to_number_type(idx(row, VALUE, mandatory=True))
    count_idx = mdef.to_number_type(idx(row, COUNT, mandatory=True))
    type_idx = idx(row, TYPE, mandatory=True)
    size_idx = mdef.to_number_type(idx(row, SIZE, mandatory=True))
    scale_factor_idx = mdef.to_number_type(idx(row, SCALE_FACTOR, mandatory=True))
    units_idx = idx(row, UNITS, mandatory=True)
    access_idx = idx(row, ACCESS, mandatory=True)
    mandatory_idx = idx(row, MANDATORY, mandatory=True)
    static_idx = idx(row, STATIC, mandatory=True)
    label_idx = idx(row, LABEL)
    description_idx = idx(row, DESCRIPTION)
    has_notes = False
    # if notes col not present, notes_idx will be None
    notes_idx = idx(row, NOTES)
    if notes_idx and row[notes_idx] == 'Notes':
        has_notes = True
    row_num = 1

    group = None
    point = None
    comments = []
    parent = ''

    for row in spreadsheet[1:]:
        row_num += 1
        name = row[name_idx]
        value = mdef.to_number_type(row[value_idx])
        etype = row[type_idx]

        label = description = notes = ''
        if len(row) > label_idx:
            label = row[label_idx]
        if len(row) > description_idx:
            description = row[description_idx]
        if has_notes:
            notes = row[notes_idx]
            if notes is None:
                notes = ''

        # point
        if etype in mdef.point_type_info:
            # point
            if group:
                if not group.get(mdef.POINTS):
                    group[mdef.POINTS] = []
                if find_name(group[mdef.POINTS], name) is not None:
                    raise Exception('Duplicate point definition in group %s: %s' % (group[mdef.NAME], name))
            else:
                raise Exception('Point %s defined outside of group' % name)
            if etype == mdef.TYPE_STRING:
                size = mdef.to_number_type(row[size_idx])
            else:
                size = mdef.point_type_info[etype]['len']
            sf = mdef.to_number_type(row[scale_factor_idx])
            units = row[units_idx]
            access = row[access_idx]
            mandatory = row[mandatory_idx]
            static = row[static_idx]
            point = {mdef.NAME: name}
            if etype:
                point[mdef.TYPE] = etype
            if size is not None and size != '':
                point[mdef.SIZE] = size
            if sf:
                point[mdef.SF] = sf
            if units:
                point[mdef.UNITS] = units
            if access:
                point[mdef.ACCESS] = access
            if mandatory:
                point[mdef.MANDATORY] = mandatory
            if static:
                point[mdef.STATIC] = static
            if label:
                point[mdef.LABEL] = label
            if description:
                point[mdef.DESCRIPTION] = description
            if has_notes:
                point[mdef.NOTES] = notes
            if value is not None and value != '':
                point[mdef.VALUE] = value
            if comments:
                point[mdef.COMMENTS] = list(comments)
            group[mdef.POINTS].append(point)

            # set the model id
            if not parent and name == mdef.MODEL_ID_POINT_NAME:
                model_def[mdef.ID] = value
            comments = []
        # group
        elif etype in mdef.group_types:
            path = name.split('.')
            group = model_def.get(mdef.GROUP)
            parent = ''
            if len(path) > 1:
                parent = group[mdef.NAME]
                for g in path[1:-1]:
                    group = find_name(group[mdef.GROUPS], g)
                    if group is None:
                        raise Exception('Unknown parent group id %s in group id %s' % (g, group))
                    parent += '.%s' % group[mdef.NAME]
            else:
                if group is not None:
                    raise Exception('Redefintion of top-level group %s with %s' % (group[mdef.ID], name))
            if parent:
                name = '%s.%s' % (parent, path[-1])
            else:
                name = path[-1]
            new_group = {mdef.NAME: path[-1], mdef.TYPE: etype}
            if label:
                new_group[mdef.LABEL] = label
            if description:
                new_group[mdef.DESCRIPTION] = description
            if has_notes:
                new_group[mdef.NOTES] = notes
            if comments:
                new_group[mdef.COMMENTS] = list(comments)
            comments = []
            count = mdef.to_number_type(row[count_idx])
            if count is not None and count != '':
                new_group[mdef.COUNT] = count
            if group is None:
                model_def[mdef.GROUP] = new_group
            else:
                if not group.get(mdef.GROUPS):
                    group[mdef.GROUPS] = []
                group[mdef.GROUPS].append(new_group)
            group = new_group
        # symbol - has name and value with no type
        elif name and value is not None and value != '':
            if point is None:
                raise Exception('Unknown point for symbol %s' % name)
            if not point.get(mdef.SYMBOLS):
                point[mdef.SYMBOLS] = []
            if find_name(point[mdef.SYMBOLS], name) is not None:
                raise Exception('Duplicate symbol definition in point %s: %s' % (point[mdef.ID], name))
            symbol = {mdef.NAME: name, mdef.VALUE: value}
            point[mdef.SYMBOLS].append(symbol)
            if label:
                symbol[mdef.LABEL] = label
            if description:
                symbol[mdef.DESCRIPTION] = description
            if has_notes:
                symbol[mdef.NOTES] = notes
            if comments:
                symbol[mdef.COMMENTS] = list(comments)
            comments = []
        elif not row_is_empty(row, 1):
            raise ValueError('Invalid spreadsheet entry row %s: %s' % (row_num, row))
        # comment - no name, value, or type
        elif row[0]:
            comments.append(row[0])
        # blank line - comment with nothing in column 1
    return model_def


def to_spreadsheet(model_def):
    # check if model_def has notes attr by searching string
    mdef_str = json.dumps(model_def)
    has_notes = '\"notes\"' in mdef_str
    c_columns = copy.deepcopy(columns)
    if has_notes:
        spreadsheet = [columns]
    else:
        c_columns.remove('Notes')
        spreadsheet = [c_columns]
    to_spreadsheet_group(spreadsheet, model_def[mdef.GROUP], has_notes, addr_offset=0)
    return(spreadsheet)


def to_spreadsheet_group(ss, group, has_notes, parent='', addr_offset=None):
    # process comments
    for c in group.get(mdef.COMMENTS, []):
        to_spreadsheet_comment(ss, c, has_notes=has_notes)
    # add group info
    row = None
    if has_notes:
        row = [''] * len(columns)
    else:
        row = [''] * (len(columns) - 1)

    name = group.get(mdef.NAME, '')
    if name:
        if parent:
            name = '%s.%s' % (parent, name)
        row[NAME_IDX] = name
    else:
        raise Exception('Group missing name attribute')
    row[TYPE_IDX] = group.get(mdef.TYPE, '')
    row[COUNT_IDX] = group.get(mdef.COUNT, '')
    row[LABEL_IDX] = group.get(mdef.LABEL, '')
    row[DESCRIPTION_IDX] = group.get(mdef.DESCRIPTION, '')
    if has_notes:
        row[NOTES_IDX] = group.get(mdef.NOTES, '')
    ss.append(row)
    # process points
    group_offset = 0
    for p in group.get(mdef.POINTS, []):
        plen = to_spreadsheet_point(ss, p, has_notes=has_notes, addr_offset=addr_offset, group_offset=group_offset)
        if addr_offset is not None:
            addr_offset += plen
        if group_offset is not None:
            group_offset += plen
    # process groups
    addr_offset = None
    for g in group.get(mdef.GROUPS, []):
        to_spreadsheet_group(ss, g, has_notes=has_notes, parent=name,  addr_offset=addr_offset)


def to_spreadsheet_point(ss, point, has_notes, addr_offset=None, group_offset=None):
    # process comments
    for c in point.get(mdef.COMMENTS, []):
        to_spreadsheet_comment(ss, c, has_notes=has_notes)
    # add point info
    row = None
    if has_notes:
        row = [''] * len(columns)
    else:
        row = [''] * (len(columns) - 1)
    name = point.get(mdef.NAME, '')
    if name:
        row[NAME_IDX] = name
    else:
        raise Exception('Point missing name attribute')
    ptype = point.get(mdef.TYPE, '')
    if ptype != '':
        row[TYPE_IDX] = ptype
    else:
        raise Exception('Point %s missing type attribute' % name)
    if addr_offset is not None:
        row[ADDRESS_OFFSET_IDX] = addr_offset
    elif group_offset is not None:
        row[GROUP_OFFSET_IDX] = group_offset
    access = point.get(mdef.ACCESS, '')
    if access != mdef.ACCESS_RW:
        access = ''
    row[ACCESS_IDX] = access
    mandatory = point.get(mdef.MANDATORY, '')
    if mandatory != mdef.MANDATORY_TRUE:
        mandatory = ''
    row[MANDATORY_IDX] = mandatory
    static = point.get(mdef.STATIC, '')
    if static != mdef.STATIC_TRUE:
        static = ''
    row[STATIC_IDX] = static
    row[UNITS_IDX] = point.get(mdef.UNITS, '')
    row[SCALE_FACTOR_IDX] = mdef.to_number_type(point.get(mdef.SF, ''))

    if ptype == mdef.TYPE_STRING:
        row[SIZE_IDX] = mdef.to_number_type(point.get(mdef.SIZE, ''))
    else:
        row[SIZE_IDX] = mdef.point_type_info[ptype]['len']

    row[VALUE_IDX] = mdef.to_number_type(point.get(mdef.VALUE, ''))
    row[LABEL_IDX] = point.get(mdef.LABEL, '')
    row[DESCRIPTION_IDX] = point.get(mdef.DESCRIPTION, '')
    if has_notes:
        row[NOTES_IDX] = point.get(mdef.NOTES, '')
    ss.append(row)
    # process symbols
    symbols = point.get(mdef.SYMBOLS, [])
    if symbols:
        symbols = sorted(symbols, key=lambda sy: sy['value'])
        for s in symbols:
            to_spreadsheet_symbol(ss, s, has_notes=has_notes)
    # return point length
    try:
        plen = mdef.point_type_info[ptype]['len']
    except KeyError:
        raise Exception('Unknown point type %s for point %s' % (ptype, name))
    if not plen:
        try:
            plen = int(row[SIZE_IDX])
        except ValueError:
            raise Exception('Point size is for point %s not an iteger value: %s' % (name, row[SIZE_IDX]))
    return plen


def to_spreadsheet_symbol(ss, symbol, has_notes):
    # process comments
    for c in symbol.get(mdef.COMMENTS, []):
        to_spreadsheet_comment(ss, c, has_notes=has_notes)
    # add symbol info
    row = None
    if has_notes:
        row = [''] * len(columns)
    else:
        row = [''] * (len(columns) - 1)
    name = symbol.get(mdef.NAME, '')
    if name:
        row[NAME_IDX] = name
    else:
        raise Exception('Symbol missing name attribute')
    value = symbol.get(mdef.VALUE, '')
    if value != '':
        row[VALUE_IDX] = value
    else:
        raise Exception('Symbol %s missing value' % name)
    row[LABEL_IDX] = symbol.get(mdef.LABEL, '')
    row[DESCRIPTION_IDX] = symbol.get(mdef.DESCRIPTION, '')
    if has_notes:
        row[NOTES_IDX] = symbol.get(mdef.NOTES, '')
    ss.append(row)


def to_spreadsheet_comment(ss, comment, has_notes):
    # add comment info
    row = None
    if has_notes:
        row = [''] * len(columns)
    else:
        row = [''] * (len(columns) - 1)
    row[0] = comment
    ss.append(row)


def spreadsheet_equal(ss1, ss2):
    count = len(ss1)
    if count != len(ss2):
        raise Exception('Different length: %s %s' % (count, len(ss2)))
    for i in range(count):
        if ss1[i] != ss2[i]:
            raise Exception('Line %s different: %s %s' % (i + 1, ss1[i], ss2[i]))
    return True


def from_csv(filename=None, csv_str=None):
    return from_spreadsheet(spreadsheet_from_csv(filename=filename, csv_str=csv_str))


def to_csv(model_def, filename=None, csv_str=None):
    spreadsheet_to_csv(to_spreadsheet(model_def), filename=filename, csv_str=csv_str)


def spreadsheet_from_csv(filename=None, csv_str=None):
    spreadsheet = []
    file = ''

    if filename:
        import sys
        file = open(filename)
    if file:
        for row in csv.reader(file):
            if len(row) > 0:
                # filter out informative offset information from the normative model definition
                if row[TYPE_IDX] and row[TYPE_IDX] != TYPE:
                    row[ADDRESS_OFFSET_IDX] = ''
                    row[GROUP_OFFSET_IDX] = ''
                if row[VALUE_IDX]:
                    row[VALUE_IDX] = mdef.to_number_type(row[VALUE_IDX])
                if row[COUNT_IDX]:
                    row[COUNT_IDX] = mdef.to_number_type(row[COUNT_IDX])
                if row[SIZE_IDX]:
                    row[SIZE_IDX] = mdef.to_number_type(row[SIZE_IDX])
                if row[SCALE_FACTOR_IDX]:
                    row[SCALE_FACTOR_IDX] = mdef.to_number_type(row[SCALE_FACTOR_IDX])
                spreadsheet.append(row)

    return spreadsheet


def spreadsheet_to_csv(spreadsheet, filename=None, csv_str=None):
    file = None
    if filename:
        file = open(filename, 'w')
    writer = csv.writer(file, lineterminator='\n')
    for row in spreadsheet:
        writer.writerow(row)
    file.close()
