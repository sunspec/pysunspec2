import sunspec2.smdx as smdx
import sunspec2.mdef as mdef
import xml.etree.ElementTree as ET
import pytest
import copy


def test_to_smdx_filename():
    assert smdx.to_smdx_filename(77) == 'smdx_00077.xml'


def test_model_filename_to_id():
    assert smdx.model_filename_to_id('smdx_00077.xml') == 77
    with pytest.raises(Exception) as exc:
        smdx.model_filename_to_id('smdx_abc.xml')
    assert 'Error extracting model id from filename' in str(exc.value)


def test_from_smdx_file():
    smdx_304 = {
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
    assert smdx.from_smdx_file('sunspec2/models/smdx/smdx_00304.xml') == smdx_304


def test_from_smdx():
    tree = ET.parse('sunspec2/models/smdx/smdx_00304.xml')
    root = tree.getroot()

    mdef_not_found = copy.deepcopy(root)
    mdef_not_found.remove(mdef_not_found.find('model'))
    with pytest.raises(mdef.ModelDefinitionError):
        smdx.from_smdx(mdef_not_found)

    duplicate_fixed_btype_str = '''
        <sunSpecModels v="1">

          <model id="63001" len="13">
            <block len="4">
              <point id="sunssf_1" offset="0" type="sunssf" />
              <point id="sunssf_2" offset="1" type="sunssf" />
              <point id="sunssf_3" offset="2" type="sunssf" />
              <point id="sunssf_4" offset="3" type="sunssf" />
            </block>
            <block len="6">
              <point id="int16_1" offset="0" type="int16" sf="sunssf_1" />
              <point id="int16_2" offset="1" type="int16" sf="sunssf_2" />
              <point id="int16_3" offset="2" type="int16" sf="sunssf_3" />
              <point id="int16_4" offset="3" type="int16" sf="sunssf_4" access="rw" />
              <point id="int16_5" offset="4" type="int16" />
              <point id="int16_u" offset="5" type="int16" />
            </block>
            <block type="repeating" len="3">
              <point id="sunssf_8" offset="0" type="sunssf" />
              <point id="int16_11" offset="1" type="int16" sf="sunssf_8" access="rw" />
              <point id="int16_12" offset="2" type="int16" sf="sunssf_9" />
            </block>
          </model>
          <strings id="63001" locale="en">
            <model>
              <label>SunSpec Test Model 1</label>
            </model>
          </strings>
        </sunSpecModels>
    '''
    duplicate_fixed_btype_xml = ET.fromstring(duplicate_fixed_btype_str)
    with pytest.raises(mdef.ModelDefinitionError):
        smdx.from_smdx(duplicate_fixed_btype_xml)

    dup_repeating_btype_str = '''
        <sunSpecModels v="1">
          <model id="63001" len="12">
            <block len="4">
              <point id="sunssf_1" offset="0" type="sunssf" />
              <point id="sunssf_2" offset="1" type="sunssf" />
              <point id="sunssf_3" offset="2" type="sunssf" />
              <point id="sunssf_4" offset="3" type="sunssf" />
            </block>
            <block type="repeating" len="3">
              <point id="sunssf_8" offset="0" type="sunssf" />
              <point id="int16_11" offset="1" type="int16" sf="sunssf_8" access="rw" />
              <point id="int16_12" offset="2" type="int16" sf="sunssf_9" />
            </block>
            <block type="repeating" len="5">
              <point id="int32_u"       offset="0"   type="int32" />
              <point id="uint32"        offset="1"   type="uint32"  sf="sunssf_9"  access="rw"/>
              <point id="uint32_u"      offset="2"   type="uint32" />
              <point id="sunssf_9"      offset="3"   type="sunssf" />
              <point id="pad_2"         offset="4"   type="pad" />
            </block>
          </model>
          <strings id="63001" locale="en">
            <model>
              <label>SunSpec Test Model 1</label>
            </model>
          </strings>
        </sunSpecModels>
    '''
    dup_repeating_btype_xml = ET.fromstring(dup_repeating_btype_str)
    with pytest.raises(mdef.ModelDefinitionError):
        smdx.from_smdx(dup_repeating_btype_xml)

    invalid_btype_root = copy.deepcopy(root)
    invalid_btype_root.find('model').find('block').set('type', 'abc')
    with pytest.raises(mdef.ModelDefinitionError):
        smdx.from_smdx(invalid_btype_root)

    dup_fixed_p_def_str = '''
        <sunSpecModels v="1">
          <model id="63001" len="4">
            <block len="4">
              <point id="sunssf_1" offset="0" type="sunssf" />
              <point id="sunssf_2" offset="1" type="sunssf" />
              <point id="sunssf_1" offset="2" type="sunssf" />
              <point id="sunssf_4" offset="3" type="sunssf" />
            </block>
          </model>
          <strings id="63001" locale="en">
            <model>
              <label>SunSpec Test Model 1</label>
            </model>
          </strings>
        </sunSpecModels>
    '''
    dup_fixed_p_def_xml = ET.fromstring(dup_fixed_p_def_str)
    with pytest.raises(mdef.ModelDefinitionError):
        smdx.from_smdx(dup_fixed_p_def_xml)

    dup_repeating_p_def_str = '''
        <sunSpecModels v="1">
          <model id="63001" len="7">
            <block len="4">
              <point id="sunssf_1" offset="0" type="sunssf" />
              <point id="sunssf_2" offset="1" type="sunssf" />
              <point id="sunssf_3" offset="2" type="sunssf" />
              <point id="sunssf_4" offset="3" type="sunssf" />
            </block>
            <block type="repeating" len="3">
              <point id="sunssf_8" offset="0" type="sunssf" />
              <point id="sunssf_8" offset="1" type="int16" sf="sunssf_8" access="rw" />
              <point id="int16_12" offset="2" type="int16" sf="sunssf_9" />
            </block>
          </model>
          <strings id="63001" locale="en">
            <model>
              <label>SunSpec Test Model 1</label>
            </model>
          </strings>
        </sunSpecModels>
    '''
    dup_repeating_p_def_xml = ET.fromstring(dup_repeating_p_def_str)
    with pytest.raises(mdef.ModelDefinitionError):
        smdx.from_smdx(dup_repeating_p_def_xml)


def test_from_smdx_point():
    smdx_point_str = """<point id="Mn" offset="0" type="string" len="16" mandatory="true" />"""
    smdx_point_xml = ET.fromstring(smdx_point_str)
    assert smdx.from_smdx_point(smdx_point_xml) == {'name': 'Mn', 'type': 'string', 'size': 16, 'mandatory': 'M'}

    missing_pid_xml = copy.deepcopy(smdx_point_xml)
    del missing_pid_xml.attrib['id']
    with pytest.raises(mdef.ModelDefinitionError):
        smdx.from_smdx_point(missing_pid_xml)

    missing_ptype = copy.deepcopy(smdx_point_xml)
    del missing_ptype.attrib['type']
    with pytest.raises(mdef.ModelDefinitionError):
        smdx.from_smdx_point(missing_ptype)

    unk_ptype = copy.deepcopy(smdx_point_xml)
    unk_ptype.attrib['type'] = 'abc'
    with pytest.raises(mdef.ModelDefinitionError):
        smdx.from_smdx_point(unk_ptype)

    missing_len = copy.deepcopy(smdx_point_xml)
    del missing_len.attrib['len']
    with pytest.raises(mdef.ModelDefinitionError):
        smdx.from_smdx_point(missing_len)

    unk_mand_type = copy.deepcopy(smdx_point_xml)
    unk_mand_type.attrib['mandatory'] = 'abc'
    with pytest.raises(mdef.ModelDefinitionError):
        smdx.from_smdx_point(unk_mand_type)

    unk_access_type = copy.deepcopy(smdx_point_xml)
    unk_access_type.attrib['access'] = 'abc'
    with pytest.raises(mdef.ModelDefinitionError):
        smdx.from_smdx_point(unk_access_type)


def test_indent():
    pass
