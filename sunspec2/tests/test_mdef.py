import sunspec2.mdef as mdef
import json
import copy
import pytest


def test_to_int():
    assert mdef.to_int('4') == 4
    assert isinstance(mdef.to_int('4'), int)
    assert isinstance(mdef.to_int(4.0), int)


def test_to_str():
    assert mdef.to_str(4) == '4'
    assert isinstance(mdef.to_str('4'), str)


def test_to_float():
    assert mdef.to_float('4') == 4.0
    assert isinstance(mdef.to_float('4'), float)
    assert mdef.to_float('z') is None


def test_to_number_type():
    assert mdef.to_number_type('4') == 4
    assert mdef.to_number_type('4.0') == 4.0
    assert mdef.to_number_type('z') == 'z'


def test_validate_find_point():
    with open('sunspec2/models/json/model_702.json') as f:
        model_json = json.load(f)

    assert mdef.validate_find_point(model_json['group'], 'ID') == model_json['group']['points'][0]
    assert mdef.validate_find_point(model_json['group'], 'abc') is None


def test_validate_attrs():
    with open('sunspec2/models/json/model_701.json') as f:
        model_json = json.load(f)

    # model
    assert mdef.validate_attrs(model_json, mdef.model_attr) == ''

    model_unexp_attr_err = copy.deepcopy(model_json)
    model_unexp_attr_err['abc'] = 'def'
    assert mdef.validate_attrs(model_unexp_attr_err, mdef.model_attr)[0:37] == 'Unexpected model definition attribute'

    model_unexp_type_err = copy.deepcopy(model_json)
    model_unexp_type_err['id'] = '701'
    assert mdef.validate_attrs(model_unexp_type_err, mdef.model_attr)[0:15] == 'Unexpected type'

    model_attr_missing = copy.deepcopy(model_json)
    del model_attr_missing['id']
    assert mdef.validate_attrs(model_attr_missing, mdef.model_attr)[0:27] == 'Mandatory attribute missing'

    # group
    assert mdef.validate_attrs(model_json['group'], mdef.group_attr) == ''
    group_unexp_attr_err = copy.deepcopy(model_json)['group']
    group_unexp_attr_err['abc'] = 'def'
    assert mdef.validate_attrs(group_unexp_attr_err, mdef.group_attr)[0:37] == 'Unexpected model definition attribute'

    group_unexp_type_err = copy.deepcopy(model_json)['group']
    group_unexp_type_err['name'] = 1
    assert mdef.validate_attrs(group_unexp_type_err, mdef.group_attr)[0:15] == 'Unexpected type'

    group_attr_missing = copy.deepcopy(model_json)['group']
    del group_attr_missing['name']
    assert mdef.validate_attrs(group_attr_missing, mdef.group_attr)[0:27] == 'Mandatory attribute missing'

    # point
    assert mdef.validate_attrs(model_json['group']['points'][0], mdef.point_attr) == ''

    point_unexp_attr_err = copy.deepcopy(model_json)['group']['points'][0]
    point_unexp_attr_err['abc'] = 'def'
    assert mdef.validate_attrs(point_unexp_attr_err, mdef.point_attr)[0:37] == 'Unexpected model definition attribute'

    point_unexp_type_err = copy.deepcopy(model_json)['group']['points'][0]
    point_unexp_type_err['name'] = 1
    assert mdef.validate_attrs(point_unexp_type_err, mdef.point_attr)[0:15] == 'Unexpected type'

    point_unexp_value_err = copy.deepcopy(model_json)['group']['points'][1]
    point_unexp_value_err['access'] = 'z'
    assert mdef.validate_attrs(point_unexp_value_err, mdef.point_attr)[0:16] == 'Unexpected value'

    point_attr_missing = copy.deepcopy(model_json)['group']['points'][0]
    del point_attr_missing['name']
    assert mdef.validate_attrs(point_attr_missing, mdef.point_attr)[0:27] == 'Mandatory attribute missing'

    # symbol
    assert mdef.validate_attrs(model_json['group']['points'][2]['symbols'][0], mdef.symbol_attr) == ''

    symbol_unexp_attr_err = copy.deepcopy(model_json)['group']['points'][2]['symbols'][0]
    symbol_unexp_attr_err['abc'] = 'def'
    assert mdef.validate_attrs(symbol_unexp_attr_err, mdef.symbol_attr)[0:37] == 'Unexpected model definition attribute'

    symbol_unexp_type_err = copy.deepcopy(model_json)['group']['points'][2]['symbols'][0]
    symbol_unexp_type_err['name'] = 1
    assert mdef.validate_attrs(symbol_unexp_type_err, mdef.symbol_attr)[0:15] == 'Unexpected type'

    symbol_attr_missing = copy.deepcopy(model_json)['group']['points'][2]['symbols'][0]
    del symbol_attr_missing['name']
    assert mdef.validate_attrs(symbol_attr_missing, mdef.symbol_attr)[0:27] == 'Mandatory attribute missing'


def test_validate_group_point_dup():
    with open('sunspec2/models/json/model_704.json') as f:
        model_json = json.load(f)

    assert mdef.validate_group_point_dup(model_json['group']) == ''

    dup_group_id_model = copy.deepcopy(model_json)
    dup_group_id_group = dup_group_id_model['group']
    dup_group_id_group['groups'][0]['name'] = 'PFWInjRvrt'
    assert mdef.validate_group_point_dup(dup_group_id_group)[0:18] == 'Duplicate group id'

    dup_group_point_id_model = copy.deepcopy(model_json)
    dup_group_point_id_group = dup_group_point_id_model['group']
    dup_group_point_id_group['groups'][0]['name'] = 'PFWInjEna'
    assert mdef.validate_group_point_dup(dup_group_point_id_group)[0:28] == 'Duplicate group and point id'

    mand_attr_miss_model = copy.deepcopy(model_json)
    mand_attr_miss_group = mand_attr_miss_model['group']
    del mand_attr_miss_group['groups'][0]['name']
    assert mdef.validate_group_point_dup(mand_attr_miss_group)[0:32] == 'Mandatory name attribute missing'

    dup_point_id_model = copy.deepcopy(model_json)
    dup_point_id_group = dup_point_id_model['group']
    dup_point_id_group['points'][1]['name'] = 'ID'
    assert mdef.validate_group_point_dup(dup_point_id_group)[0:30] == 'Duplicate point id ID in group'

    mand_attr_miss_point_model = copy.deepcopy(model_json)
    mand_attr_miss_point_group = mand_attr_miss_point_model['group']
    del mand_attr_miss_point_group['points'][1]['name']
    assert mdef.validate_group_point_dup(mand_attr_miss_point_group)[0:55] == 'Mandatory attribute missing in point ' \
                                                                              'definition element'


def test_validate_symbols():
    symbols = [
        {'name': 'CAT_A', 'value': 1},
        {'name': 'CAT_B', 'value': 2}
    ]
    assert mdef.validate_symbols(symbols, mdef.symbol_attr) == ''


def test_validate_sf():
    with open('sunspec2/models/json/model_702.json') as f:
        model_json = json.load(f)

    model_point = model_json['group']['points'][2]
    model_group = model_json['group']
    model_group_arr = [model_group, model_group]
    assert mdef.validate_sf(model_point, 'W_SF', model_group_arr) == ''

    not_sf_type_model = copy.deepcopy(model_json)
    not_sf_type_point = not_sf_type_model['group']['points'][2]
    not_sf_type_group = not_sf_type_model['group']
    not_sf_type_group_arr = [not_sf_type_group, not_sf_type_group]
    for point in not_sf_type_model['group']['points']:
        if point['name'] == 'W_SF':
            point['type'] = 'abc'
    assert mdef.validate_sf(not_sf_type_point, 'W_SF', not_sf_type_group_arr)[0:60] == 'Scale factor W_SF for point ' \
                                                                                       'WMaxRtg is not scale factor ' \
                                                                                       'type'

    sf_not_found_model = copy.deepcopy(model_json)
    sf_not_found_point = sf_not_found_model['group']['points'][2]
    sf_not_found_group = sf_not_found_model['group']
    sf_not_found_group_arr = [sf_not_found_group, sf_not_found_group]
    assert mdef.validate_sf(sf_not_found_point, 'ABC', sf_not_found_group_arr)[0:44] == 'Scale factor ABC for point ' \
                                                                                        'WMaxRtg not found'

    sf_out_range_model = copy.deepcopy(model_json)
    sf_out_range_point = sf_out_range_model['group']['points'][2]
    sf_out_range_group = sf_out_range_model['group']
    sf_out_range_group_arr = [sf_out_range_group, sf_out_range_group]
    assert mdef.validate_sf(sf_out_range_point, 11, sf_out_range_group_arr)[0:46] == 'Scale factor 11 for point ' \
                                                                                     'WMaxRtg out of range'

    sf_invalid_type_model = copy.deepcopy(model_json)
    sf_invalid_type_point = sf_invalid_type_model['group']['points'][2]
    sf_invalid_type_group = sf_invalid_type_model['group']
    sf_invalid_type_group_arr = [sf_invalid_type_group, sf_invalid_type_group]
    assert mdef.validate_sf(sf_invalid_type_point, 4.0, sf_invalid_type_group_arr)[0:51] == 'Scale factor 4.0 for' \
                                                                                            ' point WMaxRtg has ' \
                                                                                            'invalid type'


def test_validate_point_def():
    with open('sunspec2/models/json/model_702.json') as f:
        model_json = json.load(f)

    model_group = model_json['group']
    group = model_json['group']
    point = model_json['group']['points'][0]
    assert mdef.validate_point_def(point, model_group, group) == ''

    unk_point_type_model = copy.deepcopy(model_json)
    unk_point_type_model_group = unk_point_type_model['group']
    unk_point_type_group = unk_point_type_model['group']
    unk_point_type_point = unk_point_type_model['group']['points'][0]
    unk_point_type_point['type'] = 'abc'
    assert mdef.validate_point_def(unk_point_type_point, unk_point_type_model_group,
                                   unk_point_type_group)[0:35] == 'Unknown point type abc for point ID'

    dup_symbol_model = copy.deepcopy(model_json)
    dup_symbol_model_group = dup_symbol_model['group']
    dup_symbol_group = dup_symbol_model['group']
    dup_symbol_point = dup_symbol_model['group']['points'][21]
    dup_symbol_point['symbols'][0]['name'] = 'CAT_B'
    assert mdef.validate_point_def(dup_symbol_point, dup_symbol_model_group,
                                   dup_symbol_group)[0:19] == 'Duplicate symbol id'

    mand_attr_missing = copy.deepcopy(model_json)
    mand_attr_missing_model_group = mand_attr_missing['group']
    mand_attr_missing_group = mand_attr_missing['group']
    mand_attr_missing_point = mand_attr_missing['group']['points'][0]
    del mand_attr_missing_point['name']
    assert mdef.validate_point_def(mand_attr_missing_point, mand_attr_missing_model_group,
                                   mand_attr_missing_group)[0:27] == 'Mandatory attribute missing'


def test_validate_group_def():
    with open('sunspec2/models/json/model_702.json') as f:
        model_json = json.load(f)

    assert mdef.validate_group_def(model_json['group'], model_json['group']) == ''


def test_validate_model_group_def():
    with open('sunspec2/models/json/model_702.json') as f:
        model_json = json.load(f)

    assert mdef.validate_model_group_def(model_json, model_json['group']) == ''

    missing_id_model = copy.deepcopy(model_json)
    missing_id_group = missing_id_model['group']
    missing_id_group['points'][0]['name'] = 'abc'
    assert mdef.validate_model_group_def(missing_id_model, missing_id_group)[0:41] == 'First point in top-level' \
                                                                                      ' group must be ID'

    wrong_model_id_model = copy.deepcopy(model_json)
    wrong_model_id_group = wrong_model_id_model['group']
    wrong_model_id_group['points'][0]['value'] = 0
    assert mdef.validate_model_group_def(wrong_model_id_model, wrong_model_id_group)[0:42] == 'Model ID does not ' \
                                                                                              'match top-level group ID'

    missing_len_model = copy.deepcopy(model_json)
    missing_len_group = missing_len_model['group']
    missing_len_group['points'][1]['name'] = 'abc'
    assert mdef.validate_model_group_def(missing_len_model, missing_len_group)[0:41] == 'Second point in top-level ' \
                                                                                        'group must be L'

    missing_two_p_model = copy.deepcopy(model_json)
    missing_two_p_group = missing_two_p_model['group']
    missing_two_p_point = missing_two_p_group['points'][0]
    del missing_two_p_group['points']
    missing_two_p_group['points'] = [missing_two_p_point]
    assert mdef.validate_model_group_def(missing_two_p_model, missing_two_p_group)[0:48] == 'Top-level group must' \
                                                                                            ' contain at least two ' \
                                                                                            'points'

    missing_p_def_model = copy.deepcopy(model_json)
    missing_p_def_group = missing_p_def_model['group']
    del missing_p_def_group['points']
    assert mdef.validate_model_group_def(missing_p_def_model, missing_p_def_group)[0:41] == 'Top-level group' \
                                                                                            ' missing point definitions'


def test_validate_model_def():
    with open('sunspec2/models/json/model_702.json') as f:
        model_json = json.load(f)

    assert mdef.validate_model_def(model_json) == ''


def test_from_json_str():
    with open('sunspec2/models/json/model_63001.json') as f:
        model_json = json.load(f)
        model_json_str = json.dumps(model_json)
        assert isinstance(mdef.from_json_str(model_json_str), dict)


def test_from_json_file():
    assert isinstance(mdef.from_json_file('sunspec2/models/json/model_63001.json'), dict)


def test_to_json_str():
    with open('sunspec2/models/json/model_63001.json') as f:
        model_json = json.load(f)
        assert isinstance(mdef.to_json_str(model_json), str)


def test_to_json_filename():
    assert mdef.to_json_filename('63001') == 'model_63001.json'


def test_to_json_file(tmp_path):
    with open('sunspec2/models/json/model_63001.json') as f:
        model_json = json.load(f)
        mdef.to_json_file(model_json, filedir=tmp_path)

    with open(tmp_path / 'model_63001.json') as f:
        model_json = json.load(f)
        assert isinstance(model_json, dict)


def test_model_filename_to_id():
    assert mdef.model_filename_to_id('model_00077.json') == 77
    with pytest.raises(Exception) as exc:
        mdef.model_filename_to_id('model_abc.json')
    assert 'Error extracting model id from filename' in str(exc.value)
