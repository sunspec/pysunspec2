import sunspec2.xlsx as xlsx
import pytest
import openpyxl
import openpyxl.styles as styles
import json


def test___init__():
    wb = xlsx.ModelWorkbook(filename='sunspec2/tests/test_data/wb_701-705.xlsx')
    assert wb.filename == 'sunspec2/tests/test_data/wb_701-705.xlsx'
    assert wb.params == {}

    wb2 = xlsx.ModelWorkbook()
    assert wb2.filename is None
    assert wb2.params == {}


def test_get_models():
    wb = xlsx.ModelWorkbook(filename='sunspec2/tests/test_data/wb_701-705.xlsx')
    assert wb.get_models() == [701, 702, 703, 704, 705]
    wb2 = xlsx.ModelWorkbook()
    assert wb2.get_models() == []


def test_save(tmp_path):
    wb = xlsx.ModelWorkbook()
    wb.save(tmp_path / 'test.xlsx')
    wb2 = xlsx.ModelWorkbook(filename=tmp_path / 'test.xlsx')
    iter_rows = wb2.xlsx_iter_rows(wb.wb['Index'])
    assert next(iter_rows) == ['Model', 'Label', 'Description']


def test_xlsx_iter_rows():
    wb = xlsx.ModelWorkbook(filename='sunspec2/tests/test_data/wb_701-705.xlsx')
    iter_rows = wb.xlsx_iter_rows(wb.wb['704'])
    assert next(iter_rows) == ['Address Offset', 'Group Offset', 'Name',
                               'Value', 'Count', 'Type', 'Size', 'Scale Factor',
                               'Units', 'RW Access (RW)', 'Mandatory (M)', 'Static (S)',
                               'Label', 'Description', 'Detailed Description']
    assert next(iter_rows) == [None, None, 'DERCtlAC', None, None, 'group',
                               None, None, None, None, None, None, 'DER AC Controls',
                               'DER AC controls model.', None]


def test_spreadsheet_from_xlsx():
    wb = xlsx.ModelWorkbook(filename='sunspec2/tests/test_data/wb_701-705.xlsx')
    assert wb.spreadsheet_from_xlsx(704)[0:2] == [['Address Offset', 'Group Offset', 'Name', 'Value', 'Count',
                                                   'Type', 'Size', 'Scale Factor', 'Units', 'RW Access (RW)',
                                                   'Mandatory (M)', 'Static (S)', 'Label', 'Description',
                                                   'Detailed Description'],
                                                  ['', '', 'DERCtlAC', None, None, 'group', None, None, None,
                                                   None, None, None, 'DER AC Controls', 'DER AC controls model.', None]]


# need deep diff to compare from_xlsx to json file, right now just compares with its own output
def test_from_xlsx():
    wb = xlsx.ModelWorkbook(filename='sunspec2/tests/test_data/wb_701-705.xlsx')
    with open('sunspec2/models/json/model_704.json') as f:
        model_json_704 = json.load(f)
    from_xlsx_output = {
      "group": {
        "name": "DERCtlAC",
        "type": "group",
        "label": "DER AC Controls",
        "desc": "DER AC controls model.",
        "points": [
          {
            "name": "ID",
            "type": "uint16",
            "mandatory": "M",
            "static": "S",
            "label": "Model ID",
            "desc": "Model name model id.",
            "value": 704
          },
          {
            "name": "L",
            "type": "uint16",
            "mandatory": "M",
            "static": "S",
            "label": "Model Length",
            "desc": "Model name  model length."
          },
          {
            "name": "PFWInjEna",
            "type": "enum16",
            "access": "RW",
            "label": "Power Factor Enable (W Inj) Enable",
            "desc": "Power factor enable when injecting active power.",
            "comments": [
              "Set Power Factor (when injecting active power)"
            ],
            "symbols": [
              {
                "name": "DISABLED",
                "value": 0,
                "label": "Disabled",
                "desc": "Function is disabled."
              },
              {
                "name": "ENABLED",
                "value": 1,
                "label": "Enabled",
                "desc": "Function is enabled."
              }
            ]
          },
          {
            "name": "PFWInjEnaRvrt",
            "type": "enum16",
            "symbols": [
              {
                "name": "DISABLED",
                "value": 0,
                "label": "Disabled",
                "desc": "Function is disabled."
              },
              {
                "name": "ENABLED",
                "value": 1,
                "label": "Enabled",
                "desc": "Function is enabled."
              }
            ]
          },
          {
            "name": "PFWInjRvrtTms",
            "type": "uint32",
            "units": "Secs",
            "access": "RW",
            "label": "PF Reversion Time (W Inj)",
            "desc": "Power factor reversion timer when injecting active power."
          },
          {
            "name": "PFWInjRvrtRem",
            "type": "uint32",
            "units": "Secs",
            "label": "PF Reversion Time Rem (W Inj)",
            "desc": "Power factor reversion time remaining when injecting active power."
          },
          {
            "name": "PFWAbsEna",
            "type": "enum16",
            "access": "RW",
            "label": "Power Factor Enable (W Abs) Enable",
            "desc": "Power factor enable when absorbing active power.",
            "comments": [
              "Set Power Factor (when absorbing active power)"
            ],
            "symbols": [
              {
                "name": "DISABLED",
                "value": 0,
                "label": "Disabled",
                "desc": "Function is disabled."
              },
              {
                "name": "ENABLED",
                "value": 1,
                "label": "Enabled",
                "desc": "Function is enabled."
              }
            ]
          },
          {
            "name": "PFWAbsEnaRvrt",
            "type": "enum16",
            "symbols": [
              {
                "name": "DISABLED",
                "value": 0,
                "label": "Disabled",
                "desc": "Function is disabled."
              },
              {
                "name": "ENABLED",
                "value": 1,
                "label": "Enabled",
                "desc": "Function is enabled."
              }
            ]
          },
          {
            "name": "PFWAbsRvrtTms",
            "type": "uint32",
            "units": "Secs",
            "access": "RW",
            "label": "PF Reversion Time (W Abs)",
            "desc": "Power factor reversion timer when absorbing active power."
          },
          {
            "name": "PFWAbsRvrtRem",
            "type": "uint32",
            "units": "Secs",
            "label": "PF Reversion Time Rem (W Abs)",
            "desc": "Power factor reversion time remaining when absorbing active power."
          },
          {
            "name": "WMaxLimEna",
            "type": "enum16",
            "access": "RW",
            "label": "Limit Max Active Power Enable",
            "desc": "Limit maximum active power enable.",
            "comments": [
              "Limit Maximum Active Power Generation"
            ],
            "symbols": [
              {
                "name": "DISABLED",
                "value": 0,
                "label": "Disabled",
                "desc": "Function is disabled."
              },
              {
                "name": "ENABLED",
                "value": 1,
                "label": "Enabled",
                "desc": "Function is enabled."
              }
            ]
          },
          {
            "name": "WMaxLim",
            "type": "uint16",
            "sf": "WMaxLim_SF",
            "units": "Pct",
            "access": "RW",
            "label": "Limit Max Power Setpoint",
            "desc": "Limit maximum active power value."
          },
          {
            "name": "WMaxLimRvrt",
            "type": "uint16",
            "sf": "WMaxLim_SF",
            "units": "Pct",
            "access": "RW",
            "label": "Reversion Limit Max Power",
            "desc": "Reversion limit maximum active power value."
          },
          {
            "name": "WMaxLimEnaRvrt",
            "type": "enum16",
            "symbols": [
              {
                "name": "DISABLED",
                "value": 0,
                "label": "Disabled",
                "desc": "Function is disabled."
              },
              {
                "name": "ENABLED",
                "value": 1,
                "label": "Enabled",
                "desc": "Function is enabled."
              }
            ]
          },
          {
            "name": "WMaxLimRvrtTms",
            "type": "uint32",
            "units": "Secs",
            "access": "RW",
            "label": "Limit Max Power Reversion Time",
            "desc": "Limit maximum active power reversion time."
          },
          {
            "name": "WMaxLimRvrtRem",
            "type": "uint32",
            "units": "Secs",
            "label": "Limit Max Power Rev Time Rem",
            "desc": "Limit maximum active power reversion time remaining."
          },
          {
            "name": "WSetEna",
            "type": "enum16",
            "access": "RW",
            "label": "Set Active Power Enable",
            "desc": "Set active power enable.",
            "comments": [
              "Set Active Power Level (may be negative for charging)"
            ],
            "symbols": [
              {
                "name": "DISABLED",
                "value": 0,
                "label": "Disabled",
                "desc": "Function is disabled."
              },
              {
                "name": "ENABLED",
                "value": 1,
                "label": "Enabled",
                "desc": "Function is enabled."
              }
            ]
          },
          {
            "name": "WSetMod",
            "type": "enum16",
            "access": "RW",
            "label": "Set Active Power Mode",
            "desc": "Set active power mode.",
            "symbols": [
              {
                "name": "W_MAX_PCT",
                "value": 1,
                "label": "Active Power As Max Percent",
                "desc": "Active power setting is percentage of maximum active power."
              },
              {
                "name": "WATTS",
                "value": 2,
                "label": "Active Power As Watts",
                "desc": "Active power setting is in watts."
              }
            ]
          },
          {
            "name": "WSet",
            "type": "int32",
            "sf": "WSet_SF",
            "units": "W",
            "access": "RW",
            "label": "Active Power Setpoint (W)",
            "desc": "Active power setting value in watts."
          },
          {
            "name": "WSetRvrt",
            "type": "int32",
            "sf": "WSet_SF",
            "units": "W",
            "access": "RW",
            "label": "Reversion Active Power (W)",
            "desc": "Reversion active power setting value in watts."
          },
          {
            "name": "WSetPct",
            "type": "int32",
            "sf": "WSetPct_SF",
            "units": "Pct",
            "access": "RW",
            "label": "Active Power Setpoint (Pct)",
            "desc": "Active power setting value as percent."
          },
          {
            "name": "WSetPctRvrt",
            "type": "int32",
            "sf": "WSetPct_SF",
            "units": "Pct",
            "access": "RW",
            "label": "Reversion Active Power (Pct)",
            "desc": "Reversion active power setting value as percent."
          },
          {
            "name": "WSetEnaRvrt",
            "type": "enum16",
            "symbols": [
              {
                "name": "DISABLED",
                "value": 0,
                "label": "Disabled",
                "desc": "Function is disabled."
              },
              {
                "name": "ENABLED",
                "value": 1,
                "label": "Enabled",
                "desc": "Function is enabled."
              }
            ]
          },
          {
            "name": "WSetRvrtTms",
            "type": "uint32",
            "units": "Secs",
            "access": "RW",
            "label": "Active Power Reversion Time",
            "desc": "Set active power reversion time."
          },
          {
            "name": "WSetRvrtRem",
            "type": "uint32",
            "units": "Secs",
            "label": "Active Power Rev Time Rem",
            "desc": "Set active power reversion time remaining."
          },
          {
            "name": "VarSetEna",
            "type": "enum16",
            "access": "RW",
            "label": "Set Reactive Power Enable",
            "desc": "Set reactive power enable.",
            "comments": [
              "Set Reacitve Power Level"
            ],
            "symbols": [
              {
                "name": "DISABLED",
                "value": 0,
                "label": "Disabled",
                "desc": "Function is disabled."
              },
              {
                "name": "ENABLED",
                "value": 1,
                "label": "Enabled",
                "desc": "Function is enabled."
              }
            ]
          },
          {
            "name": "VarSetMod",
            "type": "enum16",
            "access": "RW",
            "label": "Set Reactive Power Mode",
            "desc": "Set reactive power mode.",
            "symbols": [
              {
                "name": "W_MAX_PCT",
                "value": 1,
                "label": "Reactive Power as Watt Max Pct",
                "desc": "Reactive power setting is percent of maximum active power."
              },
              {
                "name": "VAR_MAX_PCT",
                "value": 2,
                "label": "Reactive Power as Var Max Pct",
                "desc": "Reactive power setting is percent of maximum reactive power."
              },
              {
                "name": "VAR_AVAIL_PCT",
                "value": 3,
                "label": "Reactive Power as Var Avail Pct",
                "desc": "Reactive power setting is percent of available reactive  power."
              },
              {
                "name": "VARS",
                "value": 4,
                "label": "Reactive Power as Vars",
                "desc": "Reactive power is in vars."
              }
            ]
          },
          {
            "name": "VarSetPri",
            "type": "enum16",
            "symbols": [
              {
                "name": "ACTIVE",
                "value": 1,
                "label": "Active Power Priority",
                "desc": "Active power priority."
              },
              {
                "name": "REACTIVE",
                "value": 2,
                "label": "Reactive Power Priority",
                "desc": "Reactive power priority."
              },
              {
                "name": "IEEE_1547",
                "value": 3,
                "label": "IEEE 1547 Power Priority",
                "desc": "IEEE 1547-2018 power priority mode."
              },
              {
                "name": "PF",
                "value": 4,
                "label": "PF Power Priority",
                "desc": "Track PF setting derived from current active and reactive power settings."
              },
              {
                "name": "VENDOR",
                "value": 5,
                "label": "Vendor Power Priority",
                "desc": "Power priority is vendor specific mode."
              }
            ]
          },
          {
            "name": "VarSet",
            "type": "int32",
            "sf": "VarSet_SF",
            "units": "Var",
            "access": "RW",
            "label": "Reactive Power Setpoint (Vars)",
            "desc": "Reactive power setting value in vars."
          },
          {
            "name": "VarSetRvrt",
            "type": "int32",
            "sf": "VarSet_SF",
            "units": "Var",
            "access": "RW",
            "label": "Reversion Reactive Power (Vars)",
            "desc": "Reversion reactive power setting value in vars."
          },
          {
            "name": "VarSetPct",
            "type": "int32",
            "sf": "VarSetPct_SF",
            "units": "Pct",
            "access": "RW",
            "label": "Reactive Power Setpoint (Pct)",
            "desc": "Reactive power setting value as percent."
          },
          {
            "name": "VarSetPctRvrt",
            "type": "enum16",
            "sf": "VarSetPct_SF",
            "units": "Pct",
            "access": "RW",
            "label": "Reversion Reactive Power (Pct)",
            "desc": "Reversion reactive power setting value as percent.",
            "symbols": [
              {
                "name": "DISABLED",
                "value": 0,
                "label": "Disabled",
                "desc": "Function is disabled."
              },
              {
                "name": "ENABLED",
                "value": 1,
                "label": "Enabled",
                "desc": "Function is enabled."
              }
            ]
          },
          {
            "name": "VarSetRvrtTms",
            "type": "uint32",
            "units": "Secs",
            "access": "RW",
            "label": "Reactive Power Reversion Time",
            "desc": "Set reactive power reversion time."
          },
          {
            "name": "VarSetRvrtRem",
            "type": "uint32",
            "units": "Secs",
            "label": "Reactive Power Rev Time Rem",
            "desc": "Set reactive power reversion time remaining."
          },
          {
            "name": "RGra",
            "type": "uint32",
            "units": "%WMax/Sec",
            "access": "RW",
            "label": "Normal Ramp Rate",
            "desc": "Ramp rate for increases in active power during normal generation.",
            "comments": [
              "Ramp Rate"
            ],
            "symbols": [
              {
                "name": "A_MAX",
                "value": 1,
                "label": "Max Current Ramp",
                "desc": "Ramp based on percent of max current per second."
              },
              {
                "name": "W_MAX",
                "value": 2,
                "label": "Max Active Power Ramp",
                "desc": "Ramp based on percent of max active power per second."
              }
            ]
          },
          {
            "name": "PF_SF",
            "type": "sunssf",
            "static": "S",
            "label": "Power Factor Scale Factor",
            "desc": "Power factor scale factor.",
            "comments": [
              "Scale Factors"
            ]
          },
          {
            "name": "WMaxLim_SF",
            "type": "sunssf",
            "static": "S",
            "label": "Limit Max Power Scale Factor",
            "desc": "Limit maximum power scale factor."
          },
          {
            "name": "WSet_SF",
            "type": "sunssf",
            "static": "S",
            "label": "Active Power Scale Factor",
            "desc": "Active power scale factor."
          },
          {
            "name": "WSetPct_SF",
            "type": "sunssf",
            "static": "S",
            "label": "Active Power Pct Scale Factor",
            "desc": "Active power pct scale factor."
          },
          {
            "name": "VarSet_SF",
            "type": "sunssf",
            "static": "S",
            "label": "Reactive Power Scale Factor",
            "desc": "Reactive power scale factor."
          },
          {
            "name": "VarSetPct_SF",
            "type": "sunssf",
            "static": "S",
            "label": "Reactive Power Pct Scale Factor",
            "desc": "Reactive power pct scale factor."
          }
        ],
        "groups": [
          {
            "name": "PFWInj",
            "type": "sync",
            "label": " ",
            "desc": " ",
            "comments": [
              "Power Factor Settings"
            ],
            "points": [
              {
                "name": "PF",
                "type": "uint16",
                "sf": "PF_SF",
                "access": "RW",
                "label": "Power Factor (W Inj) ",
                "desc": "Power factor setpoint when injecting active power."
              },
              {
                "name": "Ext",
                "type": "enum16",
                "access": "RW",
                "label": "Power Factor Excitation (W Inj)",
                "desc": "Power factor excitation setpoint when injecting active power.",
                "symbols": [
                  {
                    "name": "OVER_EXCITED",
                    "value": 0,
                    "label": "Over-excited",
                    "desc": "Power factor over-excited excitation."
                  },
                  {
                    "name": "UNDER_EXCITED",
                    "value": 1,
                    "label": "Under-excited",
                    "desc": "Power factor under-excited excitation."
                  }
                ]
              }
            ]
          },
          {
            "name": "PFWInjRvrt",
            "type": "sync",
            "label": " ",
            "desc": " ",
            "points": [
              {
                "name": "PF",
                "type": "uint16",
                "sf": "PF_SF",
                "access": "RW",
                "label": "Reversion Power Factor (W Inj) ",
                "desc": "Reversion power factor setpoint when injecting active power."
              },
              {
                "name": "Ext",
                "type": "enum16",
                "access": "RW",
                "label": "Reversion PF Excitation (W Inj)",
                "desc": "Reversion power factor excitation setpoint when injecting active power.",
                "symbols": [
                  {
                    "name": "OVER_EXCITED",
                    "value": 0,
                    "label": "Over-excited",
                    "desc": "Power factor over-excited excitation."
                  },
                  {
                    "name": "UNDER_EXCITED",
                    "value": 1,
                    "label": "Under-excited",
                    "desc": "Power factor under-excited excitation."
                  }
                ]
              }
            ]
          },
          {
            "name": "PFWAbs",
            "type": "sync",
            "label": " ",
            "desc": " ",
            "points": [
              {
                "name": "PF",
                "type": "uint16",
                "sf": "PF_SF",
                "access": "RW",
                "label": "Power Factor (W Abs) ",
                "desc": "Power factor setpoint when absorbing active power."
              },
              {
                "name": "Ext",
                "type": "enum16",
                "access": "RW",
                "label": "Power Factor Excitation (W Abs)",
                "desc": "Power factor excitation setpoint when absorbing active power.",
                "symbols": [
                  {
                    "name": "OVER_EXCITED",
                    "value": 0,
                    "label": "Over-excited",
                    "desc": "Power factor over-excited excitation."
                  },
                  {
                    "name": "UNDER_EXCITED",
                    "value": 1,
                    "label": "Under-excited",
                    "desc": "Power factor under-excited excitation."
                  }
                ]
              }
            ]
          },
          {
            "name": "PFWAbsRvrt",
            "type": "sync",
            "label": " ",
            "desc": " ",
            "points": [
              {
                "name": "PF",
                "type": "uint16",
                "sf": "PF_SF",
                "access": "RW",
                "label": "Reversion Power Factor (W Abs) ",
                "desc": "Reversion power factor setpoint when absorbing active power."
              },
              {
                "name": "Ext",
                "type": "enum16",
                "access": "RW",
                "label": "Reversion PF Excitation (W Abs)",
                "desc": "Reversion power factor excitation setpoint when absorbing active power.",
                "symbols": [
                  {
                    "name": "OVER_EXCITED",
                    "value": 0,
                    "label": "Over-excited",
                    "desc": "Power factor over-excited excitation."
                  },
                  {
                    "name": "UNDER_EXCITED",
                    "value": 1,
                    "label": "Under-excited",
                    "desc": "Power factor under-excited excitation."
                  }
                ]
              }
            ]
          }
        ]
      },
      "id": 704
    }
    assert wb.from_xlsx(704) == from_xlsx_output


def test_set_cell():
    wb = xlsx.ModelWorkbook(filename='sunspec2/tests/test_data/wb_701-705.xlsx')
    with pytest.raises(ValueError) as exc:
        wb.set_cell(wb.wb['704'], 1, 2, 3)
    assert 'Workbooks opened with existing file are read only' in str(exc.value)

    wb2 = xlsx.ModelWorkbook()
    assert wb2.set_cell(wb2.wb['Index'], 2, 1, 3, style='suns_comment').value == 3


def test_set_info():
    wb = xlsx.ModelWorkbook()
    values = [''] * 15
    values[14] = 'detail'
    values[13] = 'description'
    values[12] = 'label'
    wb.set_info(wb.wb['Index'], 2, values)
    iter_rows = wb.xlsx_iter_rows(wb.wb['Index'])
    next(iter_rows)
    assert next(iter_rows) == [None, None, None, None, None, None,
                               None, None, None, None, None, None, 'label', 'description', 'detail']


def test_set_group():
    wb = xlsx.ModelWorkbook()
    values = [''] * 15
    values[2] = 'name'
    values[5] = 'type'
    values[4] = 'count'
    values[14] = 'detail'
    values[13] = 'description'
    values[12] = 'label'
    wb.set_group(wb.wb['Index'], 2, values, 2)
    iter_rows = wb.xlsx_iter_rows(wb.wb['Index'])
    next(iter_rows)
    assert next(iter_rows) == ['', '', 'name', '', 'count', 'type', '', '', '', '', '', '',
                               'label', 'description', 'detail']


def test_set_point():
    wb = xlsx.ModelWorkbook()
    values = [''] * 15
    values[0] = 'addr_offset'
    values[1] = 'group_offset'
    values[2] = 'name'
    values[3] = 'value'
    values[4] = 'count'
    values[5] = 'type'
    values[6] = 'size'
    values[7] = 'sf'
    values[8] = 'units'
    values[9] = 'access'
    values[10] = 'mandatory'
    values[11] = 'static'
    wb.set_point(wb.wb['Index'], 2, values, 1)
    iter_rows = wb.xlsx_iter_rows(wb.wb['Index'])
    next(iter_rows)
    assert next(iter_rows) == ['addr_offset', 'group_offset', 'name', 'value', 'count',
                               'type', 'size', 'sf', 'units', 'access', 'mandatory', 'static', '', '', '']


def test_set_symbol():
    wb = xlsx.ModelWorkbook()
    values = [''] * 15
    values[2] = 'name'
    values[3] = 'value'
    values[14] = 'detail'
    values[13] = 'description'
    values[12] = 'label'
    wb.set_symbol(wb.wb['Index'], 2, values)
    iter_rows = wb.xlsx_iter_rows(wb.wb['Index'])
    next(iter_rows)
    assert next(iter_rows) == ['', '', 'name', 'value', '', '', '',
                               '', '', '', '', '', 'label', 'description', 'detail']


def test_set_comment():
    wb = xlsx.ModelWorkbook()
    wb.set_comment(wb.wb['Index'], 2, ['This is a comment'])
    iter_rows = wb.xlsx_iter_rows(wb.wb['Index'])
    next(iter_rows)
    assert next(iter_rows)[0] == 'This is a comment'


def test_set_hdr():
    wb = xlsx.ModelWorkbook()
    wb.set_hdr(wb.wb['Index'], ['This', 'is', 'a', 'test', 'header'])
    iter_rows = wb.xlsx_iter_rows(wb.wb['Index'])
    assert next(iter_rows) == ['This', 'is', 'a', 'test', 'header']


def test_spreadsheet_to_xlsx():
    wb = xlsx.ModelWorkbook(filename='sunspec2/tests/test_data/wb_701-705.xlsx')
    with pytest.raises(ValueError) as exc:
        wb.spreadsheet_to_xlsx(702, [])
    assert 'Workbooks opened with existing file are read only' in str(exc.value)

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
    wb2 = xlsx.ModelWorkbook()
    wb2.spreadsheet_to_xlsx(304, spreadsheet_smdx_304)
    iter_rows = wb2.xlsx_iter_rows(wb2.wb['304'])
    for row in spreadsheet_smdx_304:
        assert next(iter_rows) == row


def test_to_xlsx(tmp_path):
    spreadsheet_smdx_304 = [
        ['Address Offset', 'Group Offset', 'Name', 'Value', 'Count', 'Type', 'Size', 'Scale Factor', 'Units',
         'RW Access (RW)', 'Mandatory (M)', 'Static (S)', 'Label', 'Description'],
        ['', '', 'inclinometer', '', '', 'group', '', '', '', '', '', '', 'Inclinometer Model',
         'Include to support orientation measurements'],
        [0, '', 'ID', 304, '', 'uint16', '', '', '', '', 'M', 'S', 'Model ID', 'Model identifier'],
        [1, '', 'L', '', '', 'uint16', '', '', '', '', 'M', 'S', 'Model Length', 'Model length'],
        ['', '', 'inclinometer.incl', '', 0, 'group', '', '', '', '', '', '', '', ''],
        ['', 0, 'Inclx', '', '', 'int32', '', -2, 'Degrees', '', 'M', '', 'X', 'X-Axis inclination'],
        ['', 2, 'Incly', '', '', 'int32', '', -2, 'Degrees', '', '', '', 'Y', 'Y-Axis inclination'],
        ['', 4, 'Inclz', '', '', 'int32', '', -2, 'Degrees', '', '', '', 'Z', 'Z-Axis inclination']
    ]
    with open('sunspec2/models/json/model_304.json') as f:
        m_703 = json.load(f)
    wb = xlsx.ModelWorkbook()
    wb.to_xlsx(m_703)
    iter_rows = wb.xlsx_iter_rows(wb.wb['304'])
    for row in spreadsheet_smdx_304:
        assert next(iter_rows) == row
