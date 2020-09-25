import sunspec2.spreadsheet as spreadsheet
import pytest
import csv
import copy
import json


def test_idx():
    row = ['Address Offset', 'Group Offset', 'Name', 'Value', 'Count', 'Type', 'Size', 'Scale Factor',
           'Units', 'RW Access (RW)', 'Mandatory (M)', 'Static (S)', 'Label', 'Description', 'Detailed Description']

    assert spreadsheet.idx(row, 'Address Offset') == 0
    with pytest.raises(ValueError):
        del row[0]
        assert spreadsheet.idx(row, 'Address Offset', mandatory=True)


def test_row_is_empty():
    row = [''] * 10
    assert spreadsheet.row_is_empty(row, 0)
    row[0] = 'abc'
    assert not spreadsheet.row_is_empty(row, 0)


def test_find_name():
    points = [
              {
                "name": "Inclx",
                "type": "int32",
                "mandatory": "M",
                "units": "Degrees",
                "sf": -2,
                "label": "X",
                "desc": "X-Axis inclination"
              },
              {
                "name": "Incly",
                "type": "int32",
                "units": "Degrees",
                "sf": -2,
                "label": "Y",
                "desc": "Y-Axis inclination"
              },
              {
                "name": "Inclz",
                "type": "int32",
                "units": "Degrees",
                "sf": -2,
                "label": "Z",
                "desc": "Z-Axis inclination"
              }
            ]
    assert spreadsheet.find_name(points, 'abc') is None
    assert spreadsheet.find_name(points, 'Incly') == points[1]


def test_element_type():
    pass


def test_from_spreadsheet():
    model_spreadsheet = [
        ['Address Offset', 'Group Offset', 'Name', 'Value', 'Count', 'Type', 'Size', 'Scale Factor', 'Units',
         'RW Access (RW)', 'Mandatory (M)', 'Static (S)', 'Label', 'Description', 'Detailed Description'],
        ['', '', 'inclinometer', '', '', 'group', '', '', '', '', '', '', 'Inclinometer Model', 'Include to support orientation measurements', ''],
        [0, '', 'ID', 304, '', 'uint16', '', '', '', '', 'M', 'S', 'Model ID', 'Model identifier', ''],
        [1, '', 'L', '', '', 'uint16', '', '', '', '', 'M', 'S', 'Model Length', 'Model length', ''],
        ['', '', 'inclinometer.incl', '', 0, 'group', '', '', '', '', '', '', '', '', ''],
        ['', 0, 'Inclx', '', '', 'int32', '', -2, 'Degrees', '', 'M', '', 'X', 'X-Axis inclination', ''],
        ['', 2, 'Incly', '', '', 'int32', '', -2, 'Degrees', '', '', '', 'Y', 'Y-Axis inclination', ''],
        ['', 4, 'Inclz', '', '', 'int32', '', -2, 'Degrees', '', '', '', 'Z', 'Z-Axis inclination', '']
    ]
    model_def = {
      "id": 304,
      "group": {
        "name": "inclinometer",
        "type": "group",
        "points": [
          {
            "name": "ID",
            "value": 304,
            "desc": "Model identifier",
            "label": "Model ID",
            "mandatory": "M",
            "static": "S",
            "type": "uint16"
          },
          {
            "name": "L",
            "desc": "Model length",
            "label": "Model Length",
            "mandatory": "M",
            "static": "S",
            "type": "uint16"
          }
        ],
        "groups": [
          {
            "name": "incl",
            "type": "group",
            "count": 0,
            "points": [
              {
                "name": "Inclx",
                "type": "int32",
                "mandatory": "M",
                "units": "Degrees",
                "sf": -2,
                "label": "X",
                "desc": "X-Axis inclination"
              },
              {
                "name": "Incly",
                "type": "int32",
                "units": "Degrees",
                "sf": -2,
                "label": "Y",
                "desc": "Y-Axis inclination"
              },
              {
                "name": "Inclz",
                "type": "int32",
                "units": "Degrees",
                "sf": -2,
                "label": "Z",
                "desc": "Z-Axis inclination"
              }
            ]
          }
        ],
        "label": "Inclinometer Model",
        "desc": "Include to support orientation measurements"
      }
    }

    assert spreadsheet.from_spreadsheet(model_spreadsheet) == model_def


def test_to_spreadsheet():
    model_spreadsheet = [
        ['Address Offset', 'Group Offset', 'Name', 'Value', 'Count', 'Type', 'Size', 'Scale Factor', 'Units',
         'RW Access (RW)', 'Mandatory (M)', 'Static (S)', 'Label', 'Description'],
        ['', '', 'inclinometer', '', '', 'group', '', '', '', '', '', '', 'Inclinometer Model', 'Include to support orientation measurements'],
        [0, '', 'ID', 304, '', 'uint16', '', '', '', '', 'M', 'S', 'Model ID', 'Model identifier'],
        [1, '', 'L', '', '', 'uint16', '', '', '', '', 'M', 'S', 'Model Length', 'Model length'],
        ['', '', 'inclinometer.incl', '', 0, 'group', '', '', '', '', '', '', '', ''],
        ['', 0, 'Inclx', '', '', 'int32', '', -2, 'Degrees', '', 'M', '', 'X', 'X-Axis inclination'],
        ['', 2, 'Incly', '', '', 'int32', '', -2, 'Degrees', '', '', '', 'Y', 'Y-Axis inclination'],
        ['', 4, 'Inclz', '', '', 'int32', '', -2, 'Degrees', '', '', '', 'Z', 'Z-Axis inclination']
    ]
    model_def = {
      "id": 304,
      "group": {
        "name": "inclinometer",
        "type": "group",
        "points": [
          {
            "name": "ID",
            "value": 304,
            "desc": "Model identifier",
            "label": "Model ID",
            "mandatory": "M",
            "static": "S",
            "type": "uint16"
          },
          {
            "name": "L",
            "desc": "Model length",
            "label": "Model Length",
            "mandatory": "M",
            "static": "S",
            "type": "uint16"
          }
        ],
        "groups": [
          {
            "name": "incl",
            "type": "group",
            "count": 0,
            "points": [
              {
                "name": "Inclx",
                "type": "int32",
                "mandatory": "M",
                "units": "Degrees",
                "sf": -2,
                "label": "X",
                "desc": "X-Axis inclination"
              },
              {
                "name": "Incly",
                "type": "int32",
                "units": "Degrees",
                "sf": -2,
                "label": "Y",
                "desc": "Y-Axis inclination"
              },
              {
                "name": "Inclz",
                "type": "int32",
                "units": "Degrees",
                "sf": -2,
                "label": "Z",
                "desc": "Z-Axis inclination"
              }
            ]
          }
        ],
        "label": "Inclinometer Model",
        "desc": "Include to support orientation measurements"
      }
    }
    assert spreadsheet.to_spreadsheet(model_def) == model_spreadsheet


def test_to_spreadsheet_group():
    model_def = {
                    "group": {
                        "desc": "DER capacity model.",
                        "label": "DER Capacity",
                        "name": "DERCapacity",
                        "points": [
                            {
                                "access": "R",
                                "desc": "DER capacity model id.",
                                "label": "DER Capacity Model ID",
                                "mandatory": "M",
                                "name": "ID",
                                "static": "S",
                                "type": "uint16",
                                "value": 702
                            },
                            {
                                "access": "R",
                                "desc": "DER capacity name  model length.",
                                "label": "DER Capacity Model Length",
                                "mandatory": "M",
                                "name": "L",
                                "static": "S",
                                "type": "uint16"
                            },
                            {
                                "access": "R",
                                "comments": [
                                    "Nameplate Ratings - Specifies capacity ratings"
                                ],
                                "desc": "Maximum active power rating at unity power factor in watts.",
                                "label": "Active Power Max Rating",
                                "mandatory": "O",
                                "name": "WMaxRtg",
                                "sf": "W_SF",
                                "type": "uint16",
                                "units": "W",
                                "symbols": [
                                    {
                                        "name": "CAT_A",
                                        "value": 1
                                    },
                                    {
                                        "name": "CAT_B",
                                        "value": 2
                                    }
                                ]
                            }
                        ],
                        "type": "group"
                    },
                    "id": 702
                }
    ss = []
    spreadsheet.to_spreadsheet_group(ss, model_def['group'], has_notes=False)
    assert ss == [
        ['', '', 'DERCapacity', '', '', 'group', '', '', '', '', '', '', 'DER Capacity', 'DER capacity model.'],
        ['', 0, 'ID', 702, '', 'uint16', '', '', '', '', 'M', 'S', 'DER Capacity Model ID',
         'DER capacity model id.'],
        ['', 1, 'L', '', '', 'uint16', '', '', '', '', 'M', 'S', 'DER Capacity Model Length',
         'DER capacity name  model length.'],
        ['Nameplate Ratings - Specifies capacity ratings', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', 2, 'WMaxRtg', '', '', 'uint16', '', 'W_SF', 'W', '', '', '', 'Active Power Max Rating',
         'Maximum active power rating at unity power factor in watts.'],
        ['', '', 'CAT_A', 1, '', '', '', '', '', '', '', '', '', ''],
        ['', '', 'CAT_B', 2, '', '', '', '', '', '', '', '', '', '']]

def test_to_spreadsheet_point():
    point = {
                "access": "R",
                "desc": "Abnormal operating performance category as specified in IEEE 1547-2018.",
                "label": "Abnormal Operating Category",
                "mandatory": "O",
                "name": "AbnOpCatRtg",
                "symbols": [
                    {
                        "name": "CAT_1",
                        "value": 1
                    },
                    {
                        "name": "CAT_2",
                        "value": 2
                    },
                    {
                        "name": "CAT_3",
                        "value": 3
                    }
                ],
                "type": "enum16"
            }
    ss = []
    assert spreadsheet.to_spreadsheet_point(ss, point, has_notes=False) == 1

    missing_name_p = copy.deepcopy(point)
    del missing_name_p['name']
    with pytest.raises(Exception) as exc1:
        spreadsheet.to_spreadsheet_point(ss, missing_name_p, has_notes=False)
    assert 'Point missing name attribute' in str(exc1.value)

    missing_type_p = copy.deepcopy(point)
    del missing_type_p['type']
    with pytest.raises(Exception) as exc2:
        spreadsheet.to_spreadsheet_point(ss, missing_type_p, has_notes=False)
    assert 'Point AbnOpCatRtg missing type' in str(exc2.value)

    unk_p_type = copy.deepcopy(point)
    unk_p_type['type'] = 'abc'
    with pytest.raises(Exception) as exc3:
        spreadsheet.to_spreadsheet_point(ss, unk_p_type, has_notes=False)
    assert 'Unknown point type' in str(exc3.value)

    p_size_not_int = copy.deepcopy(point)
    p_size_not_int['type'] = 'string'
    p_size_not_int['size'] = 'abc'
    with pytest.raises(Exception) as exc4:
        spreadsheet.to_spreadsheet_point(ss, p_size_not_int, has_notes=False)
    assert 'Point size is for point AbnOpCatRtg not an iteger value' in str(exc4.value)


def test_to_spreadsheet_symbol():
    symbol = {"name": "MAX_W", "value": 0}
    ss = []
    spreadsheet.to_spreadsheet_symbol(ss, symbol, has_notes=False)
    assert ss[0][2] == 'MAX_W' and ss[0][3] == 0

    ss = []
    del symbol['value']
    with pytest.raises(Exception) as exc1:
        spreadsheet.to_spreadsheet_symbol(ss, symbol, has_notes=False)
    assert 'Symbol MAX_W missing value' in str(exc1.value)

    ss = []
    del symbol['name']
    with pytest.raises(Exception) as exc2:
        spreadsheet.to_spreadsheet_symbol(ss, symbol, has_notes=False)
    assert 'Symbol missing name attribute' in str(exc2.value)


def test_to_spreadsheet_comment():
    ss = []
    spreadsheet.to_spreadsheet_comment(ss, 'Scaling Factors', has_notes=False)
    assert ss[0][0] == 'Scaling Factors'


def test_spreadsheet_equal():
    spreadsheet_smdx_304 = [
        ['Address Offset', 'Group Offset', 'Name', 'Value', 'Count', 'Type', 'Size', 'Scale Factor', 'Units',
         'RW Access (RW)', 'Mandatory (M)', 'Static (S)', 'Label', 'Description', 'Detailed Description'],
        ['', '', 'inclinometer', '', '', 'group', '', '', '', '', '', '', 'Inclinometer Model',
         'Include to support orientation measurements', ''],
        ['', '', 'ID', 304, '', 'uint16', '', '', '', '', 'M', 'S', 'Model ID', 'Model identifier', ''],
        ['', '', 'L', '', '', 'uint16', '', '', '', '', 'M', 'S', 'Model Length', 'Model length', ''],
        ['', '', 'inclinometer.incl', '', 0, 'group', '', '', '', '', '', '', '', '', ''],
        ['', '', 'Inclx', '', '', 'int32', '', -2, 'Degrees', '', 'M', '', 'X', 'X-Axis inclination', ''],
        ['', '', 'Incly', '', '', 'int32', '', -2, 'Degrees', '', '', '', 'Y', 'Y-Axis inclination', ''],
        ['', '', 'Inclz', '', '', 'int32', '', -2, 'Degrees', '', '', '', 'Z', 'Z-Axis inclination', '']
    ]
    ss_copy = copy.deepcopy(spreadsheet_smdx_304)

    assert spreadsheet.spreadsheet_equal(spreadsheet_smdx_304, ss_copy)

    with pytest.raises(Exception) as exc1:
        ss_copy[0][0] = 'abc'
        spreadsheet.spreadsheet_equal(spreadsheet_smdx_304, ss_copy)
    assert 'Line 1 different' in str(exc1.value)

    with pytest.raises(Exception) as exc2:
        del ss_copy[0]
        spreadsheet.spreadsheet_equal(spreadsheet_smdx_304, ss_copy)
    assert 'Different length' in str(exc2.value)


def test_from_csv():
    model_def = {
      "id": 304,
      "group": {
        "name": "inclinometer",
        "type": "group",
        "points": [
          {
            "name": "ID",
            "value": 304,
            "desc": "Model identifier",
            "label": "Model ID",
            "mandatory": "M",
            "static": "S",
            "type": "uint16"
          },
          {
            "name": "L",
            "desc": "Model length",
            "label": "Model Length",
            "mandatory": "M",
            "static": "S",
            "type": "uint16"
          }
        ],
        "groups": [
          {
            "name": "incl",
            "type": "group",
            "count": 0,
            "points": [
              {
                "name": "Inclx",
                "type": "int32",
                "mandatory": "M",
                "units": "Degrees",
                "sf": -2,
                "label": "X",
                "desc": "X-Axis inclination"
              },
              {
                "name": "Incly",
                "type": "int32",
                "units": "Degrees",
                "sf": -2,
                "label": "Y",
                "desc": "Y-Axis inclination"
              },
              {
                "name": "Inclz",
                "type": "int32",
                "units": "Degrees",
                "sf": -2,
                "label": "Z",
                "desc": "Z-Axis inclination"
              }
            ]
          }
        ],
        "label": "Inclinometer Model",
        "desc": "Include to support orientation measurements"
      }
    }
    assert model_def == spreadsheet.from_csv('sunspec2/tests/test_data/smdx_304.csv')


def test_to_csv(tmp_path):
    model_def = {
      "id": 304,
      "group": {
        "name": "inclinometer",
        "type": "group",
        "points": [
          {
            "name": "ID",
            "value": 304,
            "desc": "Model identifier",
            "label": "Model ID",
            "mandatory": "M",
            "static": "S",
            "type": "uint16"
          },
          {
            "name": "L",
            "desc": "Model length",
            "label": "Model Length",
            "mandatory": "M",
            "static": "S",
            "type": "uint16"
          }
        ],
        "groups": [
          {
            "name": "incl",
            "type": "group",
            "count": 0,
            "points": [
              {
                "name": "Inclx",
                "type": "int32",
                "mandatory": "M",
                "units": "Degrees",
                "sf": -2,
                "label": "X",
                "desc": "X-Axis inclination"
              },
              {
                "name": "Incly",
                "type": "int32",
                "units": "Degrees",
                "sf": -2,
                "label": "Y",
                "desc": "Y-Axis inclination"
              },
              {
                "name": "Inclz",
                "type": "int32",
                "units": "Degrees",
                "sf": -2,
                "label": "Z",
                "desc": "Z-Axis inclination"
              }
            ]
          }
        ],
        "label": "Inclinometer Model",
        "desc": "Include to support orientation measurements"
      }
    }
    ss = spreadsheet.to_spreadsheet(model_def)
    spreadsheet.to_csv(model_def, filename=tmp_path / 'smdx_304.csv')

    same_data = True
    row_num = 0
    idx = 0
    with open(tmp_path / 'smdx_304.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            idx = 0
            for i in row:
                if str(ss[row_num][idx]) != str(i):
                    same_data = False
                idx += 1
            row_num += 1
    assert same_data


def test_spreadsheet_from_csv():
    spreadsheet_smdx_304 = [
        ['Address Offset', 'Group Offset', 'Name', 'Value', 'Count', 'Type', 'Size', 'Scale Factor', 'Units',
         'RW Access (RW)', 'Mandatory (M)', 'Static (S)', 'Label', 'Description', 'Detailed Description'],
        ['', '', 'inclinometer', '', '', 'group', '', '', '', '', '', '', 'Inclinometer Model',
         'Include to support orientation measurements', ''],
        ['', '', 'ID', 304, '', 'uint16', '', '', '', '', 'M', 'S', 'Model ID', 'Model identifier', ''],
        ['', '', 'L', '', '', 'uint16', '', '', '', '', 'M', 'S', 'Model Length', 'Model length', ''],
        ['', '', 'inclinometer.incl', '', 0, 'group', '', '', '', '', '', '', '', '', ''],
        ['', '', 'Inclx', '', '', 'int32', '', -2, 'Degrees', '', 'M', '', 'X', 'X-Axis inclination', ''],
        ['', '', 'Incly', '', '', 'int32', '', -2, 'Degrees', '', '', '', 'Y', 'Y-Axis inclination', ''],
        ['', '', 'Inclz', '', '', 'int32', '', -2, 'Degrees', '', '', '', 'Z', 'Z-Axis inclination', '']
    ]

    counter = 0
    for row in spreadsheet.spreadsheet_from_csv('sunspec2/tests/test_data/smdx_304.csv'):
        same = True
        counter2 = 0
        for i in row:
            if i != spreadsheet_smdx_304[counter][counter2]:
                same = False
            counter2 += 1
        counter += 1
    assert same


def test_spreadsheet_to_csv(tmp_path):
    spreadsheet_smdx_304 = [
        ['Address Offset', 'Group Offset', 'Name', 'Value', 'Count', 'Type', 'Size', 'Scale Factor', 'Units',
         'RW Access (RW)', 'Mandatory (M)', 'Static (S)', 'Label', 'Description', 'Detailed Description'],
        ['', '', 'inclinometer', '', '', 'group', '', '', '', '', '', '', 'Inclinometer Model',
         'Include to support orientation measurements', ''],
        [0, '', 'ID', 304, '', 'uint16', '', '', '', '', 'M', 'S', 'Model ID', 'Model identifier', ''],
        [1, '', 'L', '', '', 'uint16', '', '', '', '', 'M', 'S', 'Model Length', 'Model length', ''],
        ['', '', 'inclinometer.incl', '', 0, 'group', '', '', '', '', '', '', '', '', ''],
        ['', 0, 'Inclx', '', '', 'int32', '', -2, 'Degrees', '', 'M', '', 'X', 'X-Axis inclination', ''],
        ['', 2, 'Incly', '', '', 'int32', '', -2, 'Degrees', '', '', '', 'Y', 'Y-Axis inclination', ''],
        ['', 4, 'Inclz', '', '', 'int32', '', -2, 'Degrees', '', '', '', 'Z', 'Z-Axis inclination', '']
    ]
    spreadsheet.spreadsheet_to_csv(spreadsheet_smdx_304, filename=tmp_path / 'smdx_304.csv')

    same_data = True
    rowNum = 0
    idx = 0
    with open(tmp_path / 'smdx_304.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            idx = 0
            for i in row:
                if str(spreadsheet_smdx_304[rowNum][idx]) != str(i):
                    same_data = False
                idx += 1
            rowNum += 1
    assert same_data


