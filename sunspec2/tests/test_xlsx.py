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
    from_xlsx_output = {'group': {'desc': 'DER AC controls model.',
                                  'groups': [{'comments': ['Power Factor Settings'],
                                              'desc': ' ',
                                              'label': ' ',
                                              'name': 'PFWInj',
                                              'points': [{'access': 'RW',
                                                          'desc': 'Power factor setpoint when injecting active power.',
                                                          'label': 'Power Factor (W Inj) ',
                                                          'name': 'PF',
                                                          'sf': 'PF_SF',
                                                          'size': 1,
                                                          'type': 'uint16'},
                                                         {'access': 'RW',
                                                          'desc': 'Power factor excitation setpoint when injecting active power.',
                                                          'label': 'Power Factor Excitation (W Inj)',
                                                          'name': 'Ext',
                                                          'size': 1,
                                                          'symbols': [{'desc': 'Power factor over-excited excitation.',
                                                                       'label': 'Over-excited',
                                                                       'name': 'OVER_EXCITED',
                                                                       'value': 0},
                                                                      {'desc': 'Power factor under-excited excitation.',
                                                                       'label': 'Under-excited',
                                                                       'name': 'UNDER_EXCITED',
                                                                       'value': 1}],
                                                          'type': 'enum16'}],
                                              'type': 'sync'},
                                             {'desc': ' ',
                                              'label': ' ',
                                              'name': 'PFWInjRvrt',
                                              'points': [{'access': 'RW',
                                                          'desc': 'Reversion power factor setpoint when injecting active power.',
                                                          'label': 'Reversion Power Factor (W Inj) ',
                                                          'name': 'PF',
                                                          'sf': 'PF_SF',
                                                          'size': 1,
                                                          'type': 'uint16'},
                                                         {'access': 'RW',
                                                          'desc': 'Reversion power factor excitation setpoint when injecting active power.',
                                                          'label': 'Reversion PF Excitation (W Inj)',
                                                          'name': 'Ext',
                                                          'size': 1,
                                                          'symbols': [{'desc': 'Power factor over-excited excitation.',
                                                                       'label': 'Over-excited',
                                                                       'name': 'OVER_EXCITED',
                                                                       'value': 0},
                                                                      {'desc': 'Power factor under-excited excitation.',
                                                                       'label': 'Under-excited',
                                                                       'name': 'UNDER_EXCITED',
                                                                       'value': 1}],
                                                          'type': 'enum16'}],
                                              'type': 'sync'},
                                             {'desc': ' ',
                                              'label': ' ',
                                              'name': 'PFWAbs',
                                              'points': [{'access': 'RW',
                                                          'desc': 'Power factor setpoint when absorbing active power.',
                                                          'label': 'Power Factor (W Abs) ',
                                                          'name': 'PF',
                                                          'sf': 'PF_SF',
                                                          'size': 1,
                                                          'type': 'uint16'},
                                                         {'access': 'RW',
                                                          'desc': 'Power factor excitation setpoint when absorbing active power.',
                                                          'label': 'Power Factor Excitation (W Abs)',
                                                          'name': 'Ext',
                                                          'size': 1,
                                                          'symbols': [{'desc': 'Power factor over-excited excitation.',
                                                                       'label': 'Over-excited',
                                                                       'name': 'OVER_EXCITED',
                                                                       'value': 0},
                                                                      {'desc': 'Power factor under-excited excitation.',
                                                                       'label': 'Under-excited',
                                                                       'name': 'UNDER_EXCITED',
                                                                       'value': 1}],
                                                          'type': 'enum16'}],
                                              'type': 'sync'},
                                             {'desc': ' ',
                                              'label': ' ',
                                              'name': 'PFWAbsRvrt',
                                              'points': [{'access': 'RW',
                                                          'desc': 'Reversion power factor setpoint when absorbing active power.',
                                                          'label': 'Reversion Power Factor (W Abs) ',
                                                          'name': 'PF',
                                                          'sf': 'PF_SF',
                                                          'size': 1,
                                                          'type': 'uint16'},
                                                         {'access': 'RW',
                                                          'desc': 'Reversion power factor excitation setpoint when absorbing active power.',
                                                          'label': 'Reversion PF Excitation (W Abs)',
                                                          'name': 'Ext',
                                                          'size': 1,
                                                          'symbols': [{'desc': 'Power factor over-excited excitation.',
                                                                       'label': 'Over-excited',
                                                                       'name': 'OVER_EXCITED',
                                                                       'value': 0},
                                                                      {'desc': 'Power factor under-excited excitation.',
                                                                       'label': 'Under-excited',
                                                                       'name': 'UNDER_EXCITED',
                                                                       'value': 1}],
                                                          'type': 'enum16'}],
                                              'type': 'sync'}],
                                  'label': 'DER AC Controls',
                                  'name': 'DERCtlAC',
                                  'points': [{'desc': 'Model name model id.',
                                              'label': 'Model ID',
                                              'mandatory': 'M',
                                              'name': 'ID',
                                              'size': 1,
                                              'static': 'S',
                                              'type': 'uint16',
                                              'value': 704},
                                             {'desc': 'Model name  model length.',
                                              'label': 'Model Length',
                                              'mandatory': 'M',
                                              'name': 'L',
                                              'size': 1,
                                              'static': 'S',
                                              'type': 'uint16'},
                                             {'access': 'RW',
                                              'comments': ['Set Power Factor (when injecting active power)'],
                                              'desc': 'Power factor enable when injecting active power.',
                                              'label': 'Power Factor Enable (W Inj) Enable',
                                              'name': 'PFWInjEna',
                                              'size': 1,
                                              'symbols': [{'desc': 'Function is disabled.',
                                                           'label': 'Disabled',
                                                           'name': 'DISABLED',
                                                           'value': 0},
                                                          {'desc': 'Function is enabled.',
                                                           'label': 'Enabled',
                                                           'name': 'ENABLED',
                                                           'value': 1}],
                                              'type': 'enum16'},
                                             {'name': 'PFWInjEnaRvrt',
                                              'size': 1,
                                              'symbols': [{'desc': 'Function is disabled.',
                                                           'label': 'Disabled',
                                                           'name': 'DISABLED',
                                                           'value': 0},
                                                          {'desc': 'Function is enabled.',
                                                           'label': 'Enabled',
                                                           'name': 'ENABLED',
                                                           'value': 1}],
                                              'type': 'enum16'},
                                             {'access': 'RW',
                                              'desc': 'Power factor reversion timer when injecting active power.',
                                              'label': 'PF Reversion Time (W Inj)',
                                              'name': 'PFWInjRvrtTms',
                                              'size': 2,
                                              'type': 'uint32',
                                              'units': 'Secs'},
                                             {'desc': 'Power factor reversion time remaining when injecting active power.',
                                              'label': 'PF Reversion Time Rem (W Inj)',
                                              'name': 'PFWInjRvrtRem',
                                              'size': 2,
                                              'type': 'uint32',
                                              'units': 'Secs'},
                                             {'access': 'RW',
                                              'comments': ['Set Power Factor (when absorbing active power)'],
                                              'desc': 'Power factor enable when absorbing active power.',
                                              'label': 'Power Factor Enable (W Abs) Enable',
                                              'name': 'PFWAbsEna',
                                              'size': 1,
                                              'symbols': [{'desc': 'Function is disabled.',
                                                           'label': 'Disabled',
                                                           'name': 'DISABLED',
                                                           'value': 0},
                                                          {'desc': 'Function is enabled.',
                                                           'label': 'Enabled',
                                                           'name': 'ENABLED',
                                                           'value': 1}],
                                              'type': 'enum16'},
                                             {'name': 'PFWAbsEnaRvrt',
                                              'size': 1,
                                              'symbols': [{'desc': 'Function is disabled.',
                                                           'label': 'Disabled',
                                                           'name': 'DISABLED',
                                                           'value': 0},
                                                          {'desc': 'Function is enabled.',
                                                           'label': 'Enabled',
                                                           'name': 'ENABLED',
                                                           'value': 1}],
                                              'type': 'enum16'},
                                             {'access': 'RW',
                                              'desc': 'Power factor reversion timer when absorbing active power.',
                                              'label': 'PF Reversion Time (W Abs)',
                                              'name': 'PFWAbsRvrtTms',
                                              'size': 2,
                                              'type': 'uint32',
                                              'units': 'Secs'},
                                             {'desc': 'Power factor reversion time remaining when absorbing active power.',
                                              'label': 'PF Reversion Time Rem (W Abs)',
                                              'name': 'PFWAbsRvrtRem',
                                              'size': 2,
                                              'type': 'uint32',
                                              'units': 'Secs'},
                                             {'access': 'RW',
                                              'comments': ['Limit Maximum Active Power Generation'],
                                              'desc': 'Limit maximum active power enable.',
                                              'label': 'Limit Max Active Power Enable',
                                              'name': 'WMaxLimEna',
                                              'size': 1,
                                              'symbols': [{'desc': 'Function is disabled.',
                                                           'label': 'Disabled',
                                                           'name': 'DISABLED',
                                                           'value': 0},
                                                          {'desc': 'Function is enabled.',
                                                           'label': 'Enabled',
                                                           'name': 'ENABLED',
                                                           'value': 1}],
                                              'type': 'enum16'},
                                             {'access': 'RW',
                                              'desc': 'Limit maximum active power value.',
                                              'label': 'Limit Max Power Setpoint',
                                              'name': 'WMaxLim',
                                              'sf': 'WMaxLim_SF',
                                              'size': 1,
                                              'type': 'uint16',
                                              'units': 'Pct'},
                                             {'access': 'RW',
                                              'desc': 'Reversion limit maximum active power value.',
                                              'label': 'Reversion Limit Max Power',
                                              'name': 'WMaxLimRvrt',
                                              'sf': 'WMaxLim_SF',
                                              'size': 1,
                                              'type': 'uint16',
                                              'units': 'Pct'},
                                             {'name': 'WMaxLimEnaRvrt',
                                              'size': 1,
                                              'symbols': [{'desc': 'Function is disabled.',
                                                           'label': 'Disabled',
                                                           'name': 'DISABLED',
                                                           'value': 0},
                                                          {'desc': 'Function is enabled.',
                                                           'label': 'Enabled',
                                                           'name': 'ENABLED',
                                                           'value': 1}],
                                              'type': 'enum16'},
                                             {'access': 'RW',
                                              'desc': 'Limit maximum active power reversion time.',
                                              'label': 'Limit Max Power Reversion Time',
                                              'name': 'WMaxLimRvrtTms',
                                              'size': 2,
                                              'type': 'uint32',
                                              'units': 'Secs'},
                                             {'desc': 'Limit maximum active power reversion time remaining.',
                                              'label': 'Limit Max Power Rev Time Rem',
                                              'name': 'WMaxLimRvrtRem',
                                              'size': 2,
                                              'type': 'uint32',
                                              'units': 'Secs'},
                                             {'access': 'RW',
                                              'comments': ['Set Active Power Level (may be negative for charging)'],
                                              'desc': 'Set active power enable.',
                                              'label': 'Set Active Power Enable',
                                              'name': 'WSetEna',
                                              'size': 1,
                                              'symbols': [{'desc': 'Function is disabled.',
                                                           'label': 'Disabled',
                                                           'name': 'DISABLED',
                                                           'value': 0},
                                                          {'desc': 'Function is enabled.',
                                                           'label': 'Enabled',
                                                           'name': 'ENABLED',
                                                           'value': 1}],
                                              'type': 'enum16'},
                                             {'access': 'RW',
                                              'desc': 'Set active power mode.',
                                              'label': 'Set Active Power Mode',
                                              'name': 'WSetMod',
                                              'size': 1,
                                              'symbols': [{'desc': 'Active power setting is percentage of maximum active power.',
                                                           'label': 'Active Power As Max Percent',
                                                           'name': 'W_MAX_PCT',
                                                           'value': 1},
                                                          {'desc': 'Active power setting is in watts.',
                                                           'label': 'Active Power As Watts',
                                                           'name': 'WATTS',
                                                           'value': 2}],
                                              'type': 'enum16'},
                                             {'access': 'RW',
                                              'desc': 'Active power setting value in watts.',
                                              'label': 'Active Power Setpoint (W)',
                                              'name': 'WSet',
                                              'sf': 'WSet_SF',
                                              'size': 2,
                                              'type': 'int32',
                                              'units': 'W'},
                                             {'access': 'RW',
                                              'desc': 'Reversion active power setting value in watts.',
                                              'label': 'Reversion Active Power (W)',
                                              'name': 'WSetRvrt',
                                              'sf': 'WSet_SF',
                                              'size': 2,
                                              'type': 'int32',
                                              'units': 'W'},
                                             {'access': 'RW',
                                              'desc': 'Active power setting value as percent.',
                                              'label': 'Active Power Setpoint (Pct)',
                                              'name': 'WSetPct',
                                              'sf': 'WSetPct_SF',
                                              'size': 2,
                                              'type': 'int32',
                                              'units': 'Pct'},
                                             {'access': 'RW',
                                              'desc': 'Reversion active power setting value as percent.',
                                              'label': 'Reversion Active Power (Pct)',
                                              'name': 'WSetPctRvrt',
                                              'sf': 'WSetPct_SF',
                                              'size': 2,
                                              'type': 'int32',
                                              'units': 'Pct'},
                                             {'name': 'WSetEnaRvrt',
                                              'size': 1,
                                              'symbols': [{'desc': 'Function is disabled.',
                                                           'label': 'Disabled',
                                                           'name': 'DISABLED',
                                                           'value': 0},
                                                          {'desc': 'Function is enabled.',
                                                           'label': 'Enabled',
                                                           'name': 'ENABLED',
                                                           'value': 1}],
                                              'type': 'enum16'},
                                             {'access': 'RW',
                                              'desc': 'Set active power reversion time.',
                                              'label': 'Active Power Reversion Time',
                                              'name': 'WSetRvrtTms',
                                              'size': 2,
                                              'type': 'uint32',
                                              'units': 'Secs'},
                                             {'desc': 'Set active power reversion time remaining.',
                                              'label': 'Active Power Rev Time Rem',
                                              'name': 'WSetRvrtRem',
                                              'size': 2,
                                              'type': 'uint32',
                                              'units': 'Secs'},
                                             {'access': 'RW',
                                              'comments': ['Set Reacitve Power Level'],
                                              'desc': 'Set reactive power enable.',
                                              'label': 'Set Reactive Power Enable',
                                              'name': 'VarSetEna',
                                              'size': 1,
                                              'symbols': [{'desc': 'Function is disabled.',
                                                           'label': 'Disabled',
                                                           'name': 'DISABLED',
                                                           'value': 0},
                                                          {'desc': 'Function is enabled.',
                                                           'label': 'Enabled',
                                                           'name': 'ENABLED',
                                                           'value': 1}],
                                              'type': 'enum16'},
                                             {'access': 'RW',
                                              'desc': 'Set reactive power mode.',
                                              'label': 'Set Reactive Power Mode',
                                              'name': 'VarSetMod',
                                              'size': 1,
                                              'symbols': [{'desc': 'Reactive power setting is percent of maximum active power.',
                                                           'label': 'Reactive Power as Watt Max Pct',
                                                           'name': 'W_MAX_PCT',
                                                           'value': 1},
                                                          {'desc': 'Reactive power setting is percent of maximum reactive power.',
                                                           'label': 'Reactive Power as Var Max Pct',
                                                           'name': 'VAR_MAX_PCT',
                                                           'value': 2},
                                                          {'desc': 'Reactive power setting is percent of available reactive  power.',
                                                           'label': 'Reactive Power as Var Avail Pct',
                                                           'name': 'VAR_AVAIL_PCT',
                                                           'value': 3},
                                                          {'desc': 'Reactive power is in vars.',
                                                           'label': 'Reactive Power as Vars',
                                                           'name': 'VARS',
                                                           'value': 4}],
                                              'type': 'enum16'},
                                             {'name': 'VarSetPri',
                                              'size': 1,
                                              'symbols': [{'desc': 'Active power priority.',
                                                           'label': 'Active Power Priority',
                                                           'name': 'ACTIVE',
                                                           'value': 1},
                                                          {'desc': 'Reactive power priority.',
                                                           'label': 'Reactive Power Priority',
                                                           'name': 'REACTIVE',
                                                           'value': 2},
                                                          {'desc': 'IEEE 1547-2018 power priority mode.',
                                                           'label': 'IEEE 1547 Power Priority',
                                                           'name': 'IEEE_1547',
                                                           'value': 3},
                                                          {'desc': 'Track PF setting derived from current active and reactive power settings.',
                                                           'label': 'PF Power Priority',
                                                           'name': 'PF',
                                                           'value': 4},
                                                          {'desc': 'Power priority is vendor specific mode.',
                                                           'label': 'Vendor Power Priority',
                                                           'name': 'VENDOR',
                                                           'value': 5}],
                                              'type': 'enum16'},
                                             {'access': 'RW',
                                              'desc': 'Reactive power setting value in vars.',
                                              'label': 'Reactive Power Setpoint (Vars)',
                                              'name': 'VarSet',
                                              'sf': 'VarSet_SF',
                                              'size': 2,
                                              'type': 'int32',
                                              'units': 'Var'},
                                             {'access': 'RW',
                                              'desc': 'Reversion reactive power setting value in vars.',
                                              'label': 'Reversion Reactive Power (Vars)',
                                              'name': 'VarSetRvrt',
                                              'sf': 'VarSet_SF',
                                              'size': 2,
                                              'type': 'int32',
                                              'units': 'Var'},
                                             {'access': 'RW',
                                              'desc': 'Reactive power setting value as percent.',
                                              'label': 'Reactive Power Setpoint (Pct)',
                                              'name': 'VarSetPct',
                                              'sf': 'VarSetPct_SF',
                                              'size': 2,
                                              'type': 'int32',
                                              'units': 'Pct'},
                                             {'access': 'RW',
                                              'desc': 'Reversion reactive power setting value as percent.',
                                              'label': 'Reversion Reactive Power (Pct)',
                                              'name': 'VarSetPctRvrt',
                                              'sf': 'VarSetPct_SF',
                                              'size': 1,
                                              'symbols': [{'desc': 'Function is disabled.',
                                                           'label': 'Disabled',
                                                           'name': 'DISABLED',
                                                           'value': 0},
                                                          {'desc': 'Function is enabled.',
                                                           'label': 'Enabled',
                                                           'name': 'ENABLED',
                                                           'value': 1}],
                                              'type': 'enum16',
                                              'units': 'Pct'},
                                             {'access': 'RW',
                                              'desc': 'Set reactive power reversion time.',
                                              'label': 'Reactive Power Reversion Time',
                                              'name': 'VarSetRvrtTms',
                                              'size': 2,
                                              'type': 'uint32',
                                              'units': 'Secs'},
                                             {'desc': 'Set reactive power reversion time remaining.',
                                              'label': 'Reactive Power Rev Time Rem',
                                              'name': 'VarSetRvrtRem',
                                              'size': 2,
                                              'type': 'uint32',
                                              'units': 'Secs'},
                                             {'access': 'RW',
                                              'comments': ['Ramp Rate'],
                                              'desc': 'Ramp rate for increases in active power during normal generation.',
                                              'label': 'Normal Ramp Rate',
                                              'name': 'RGra',
                                              'size': 2,
                                              'symbols': [{'desc': 'Ramp based on percent of max current per second.',
                                                           'label': 'Max Current Ramp',
                                                           'name': 'A_MAX',
                                                           'value': 1},
                                                          {'desc': 'Ramp based on percent of max active power per second.',
                                                           'label': 'Max Active Power Ramp',
                                                           'name': 'W_MAX',
                                                           'value': 2}],
                                              'type': 'uint32',
                                              'units': '%WMax/Sec'},
                                             {'comments': ['Scale Factors'],
                                              'desc': 'Power factor scale factor.',
                                              'label': 'Power Factor Scale Factor',
                                              'name': 'PF_SF',
                                              'size': 1,
                                              'static': 'S',
                                              'type': 'sunssf'},
                                             {'desc': 'Limit maximum power scale factor.',
                                              'label': 'Limit Max Power Scale Factor',
                                              'name': 'WMaxLim_SF',
                                              'size': 1,
                                              'static': 'S',
                                              'type': 'sunssf'},
                                             {'desc': 'Active power scale factor.',
                                              'label': 'Active Power Scale Factor',
                                              'name': 'WSet_SF',
                                              'size': 1,
                                              'static': 'S',
                                              'type': 'sunssf'},
                                             {'desc': 'Active power pct scale factor.',
                                              'label': 'Active Power Pct Scale Factor',
                                              'name': 'WSetPct_SF',
                                              'size': 1,
                                              'static': 'S',
                                              'type': 'sunssf'},
                                             {'desc': 'Reactive power scale factor.',
                                              'label': 'Reactive Power Scale Factor',
                                              'name': 'VarSet_SF',
                                              'size': 1,
                                              'static': 'S',
                                              'type': 'sunssf'},
                                             {'desc': 'Reactive power pct scale factor.',
                                              'label': 'Reactive Power Pct Scale Factor',
                                              'name': 'VarSetPct_SF',
                                              'size': 1,
                                              'static': 'S',
                                              'type': 'sunssf'}],
                                  'type': 'group'},
                        'id': 704}
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
    assert next(iter_rows) == ['addr_offset', 'group_offset', 'name', 'value', 'count', 'type', '',
                               'sf', 'units', 'access', 'mandatory', 'static', '', '', '']


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
