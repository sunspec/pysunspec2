import sunspec2.device as device
import sunspec2.mdef as mdef
import sunspec2.mb as mb
import pytest


def test_get_model_info():
    model_info = device.get_model_info(705)
    assert model_info[0]['id'] == 705
    assert model_info[1]
    assert model_info[2] == 15


def test_check_group_count():
    gdef = {'count': 'NPt'}
    gdef2 = {'groups': [{'test': 'test'}, {'count': 'NPt'}]}
    gdef3 = {'test1': 'test2', 'groups': [{'test3': 'test3'}, {'test4': 'test4'}]}
    assert device.check_group_count(gdef) is True
    assert device.check_group_count(gdef2) is True
    assert device.check_group_count(gdef3) is False


def test_get_model_def():

    with pytest.raises(mdef.ModelDefinitionError) as exc1:
        device.get_model_def('z')
    assert 'Invalid model id' in str(exc1.value)

    with pytest.raises(Exception) as exc2:
        device.get_model_def('000')
    assert 'Model definition not found for model' in str(exc2.value)

    assert device.get_model_def(704)['id'] == 704


def test_add_mappings():
    group_def = {
        "group": {
            "groups": [
                {
                    "name": "PFWInj",
                    "points": [
                        {
                            "access": "RW",
                            "desc": "Power factor setpoint when injecting active power.",
                            "label": "Power Factor (W Inj) ",
                            "mandatory": "O",
                            "name": "PF",
                            "sf": "PF_SF",
                            "type": "uint16"
                        },
                    ],
                    "type": "sync"
                },
                {
                    "name": "PFWInjRvrt",
                    "points": [
                        {
                            "access": "RW",
                            "desc": "Reversion power factor setpoint when injecting active power.",
                            "label": "Reversion Power Factor (W Inj) ",
                            "mandatory": "O",
                            "name": "PF",
                            "sf": "PF_SF",
                            "type": "uint16"
                        }
                    ],
                    "type": "sync"
                }
            ],
            "name": "DERCtlAC",
            "points": [
                {
                    "name": "ID",
                    "static": "S",
                    "type": "uint16",
                    "value": 704
                }
            ],
            "type": "group"
        },
        "id": 704
    }

    group_def_w_mappings = {
                "group": {
                    "groups": [
                        {
                            "name": "PFWInj",
                            "points": [
                                {
                                    "access": "RW",
                                    "desc": "Power factor setpoint when injecting active power.",
                                    "label": "Power Factor (W Inj) ",
                                    "mandatory": "O",
                                    "name": "PF",
                                    "sf": "PF_SF",
                                    "type": "uint16"
                                }
                            ],
                            "type": "sync",
                            "point_defs": {
                                "PF": {
                                    "access": "RW",
                                    "desc": "Power factor setpoint when injecting active power.",
                                    "label": "Power Factor (W Inj) ",
                                    "mandatory": "O",
                                    "name": "PF",
                                    "sf": "PF_SF",
                                    "type": "uint16"
                                }
                            },
                            "group_defs": {}
                        },
                        {
                            "name": "PFWInjRvrt",
                            "points": [
                                {
                                    "access": "RW",
                                    "desc": "Reversion power factor setpoint when injecting active power.",
                                    "label": "Reversion Power Factor (W Inj) ",
                                    "mandatory": "O",
                                    "name": "PF",
                                    "sf": "PF_SF",
                                    "type": "uint16"
                                }
                            ],
                            "type": "sync",
                            "point_defs": {
                                "PF": {
                                    "access": "RW",
                                    "desc": "Reversion power factor setpoint when injecting active power.",
                                    "label": "Reversion Power Factor (W Inj) ",
                                    "mandatory": "O",
                                    "name": "PF",
                                    "sf": "PF_SF",
                                    "type": "uint16"
                                }
                            },
                            "group_defs": {}
                        }
                    ],
                    "name": "DERCtlAC",
                    "points": [
                        {
                            "name": "ID",
                            "static": "S",
                            "type": "uint16",
                            "value": 704
                        }
                    ],
                    "type": "group",
                    "point_defs": {
                        "ID": {
                            "name": "ID",
                            "static": "S",
                            "type": "uint16",
                            "value": 704
                        }
                    },
                    "group_defs": {
                        "PFWInj": {
                            "name": "PFWInj",
                            "points": [
                                {
                                    "access": "RW",
                                    "desc": "Power factor setpoint when injecting active power.",
                                    "label": "Power Factor (W Inj) ",
                                    "mandatory": "O",
                                    "name": "PF",
                                    "sf": "PF_SF",
                                    "type": "uint16"
                                }
                            ],
                            "type": "sync",
                            "point_defs": {
                                "PF": {
                                    "access": "RW",
                                    "desc": "Power factor setpoint when injecting active power.",
                                    "label": "Power Factor (W Inj) ",
                                    "mandatory": "O",
                                    "name": "PF",
                                    "sf": "PF_SF",
                                    "type": "uint16"
                                }
                            },
                            "group_defs": {}
                        },
                        "PFWInjRvrt": {
                            "name": "PFWInjRvrt",
                            "points": [
                                {
                                    "access": "RW",
                                    "desc": "Reversion power factor setpoint when injecting active power.",
                                    "label": "Reversion Power Factor (W Inj) ",
                                    "mandatory": "O",
                                    "name": "PF",
                                    "sf": "PF_SF",
                                    "type": "uint16"
                                }
                            ],
                            "type": "sync",
                            "point_defs": {
                                "PF": {
                                    "access": "RW",
                                    "desc": "Reversion power factor setpoint when injecting active power.",
                                    "label": "Reversion Power Factor (W Inj) ",
                                    "mandatory": "O",
                                    "name": "PF",
                                    "sf": "PF_SF",
                                    "type": "uint16"
                                }
                            },
                            "group_defs": {}
                        }
                    }
                },
                "id": 704
            }
    device.add_mappings(group_def['group'])
    assert group_def == group_def_w_mappings


class TestPoint:
    def test___init__(self):
        p_def = {
                    "name": "Ena",
                    "type": "enum16",
                    "sf": 'test sf'
                }

        p = device.Point(p_def)
        assert p.model is None
        assert p.pdef == p_def
        assert p.info == mb.point_type_info[mdef.TYPE_ENUM16]
        assert p.len == 1
        assert p.offset == 0
        assert p.value is None
        assert p.dirty is False
        assert p.sf == 'test sf'
        assert p.sf_required is True
        assert p.sf_value is None

    def test__set_data(self):
        p_def = {
            "name": 'TestPoint',
            "type": "uint16"
        }

        # bytes
        p = device.Point(p_def)
        p._set_data(b'\x00\x03')
        assert p.value == 3
        assert not p.dirty

        # dict
        data = {"TestPoint": 3}
        p2 = device.Point(p_def)
        p2._set_data(data)
        assert p2.value == 3

    def test_value_getter(self):
        p_def = {
            "name": "TestPoint",
            "type": "uint16",
        }
        p = device.Point(p_def)
        p.value = 4
        assert p.value == 4

    def test_value_setter(self):
        p_def = {
            "name": "TestPoint",
            "type": "uint16",
        }
        p = device.Point(p_def)
        p.value = 4
        assert p.value == 4

    def test_cvalue_getter(self):
        p_def = {
            "name": "TestPoint",
            "type": "uint16",
            "sf": "TestSF"
        }
        p = device.Point(p_def)
        p.sf_required = True
        p.sf_value = 3
        p.value = 4
        assert p.cvalue == 4000.0

        p_sf = device.Point()
        points = {'TestSF': p_sf}
        m = device.Model()
        setattr(m, 'points', points)
        p2 = device.Point(p_def, model=m)
        p2.sf_value = -2
        p2.cvalue = 1.16
        assert p2.cvalue == 1.16
        assert p2.value == 116

    def test_cvalue_setter(self):
        p_def = {
            "name": "TestPoint",
            "type": "uint16"
        }
        p = device.Point(p_def)
        p.sf_required = True
        p.sf_value = 3
        p.cvalue = 3000
        assert p.value == 3

        p_sf = device.Point()
        points = {'TestSF': p_sf}
        m = device.Model()
        setattr(m, 'points', points)
        p2 = device.Point(p_def, model=m)
        p2.sf_value = -2
        p2.cvalue = 1.16
        assert p2.cvalue == 1.16
        assert p2.value == 116

    def test_get_value(self):
        p_def = {
            "access": "RW",
            "desc": "Power factor setpoint when injecting active power.",
            "label": "Power Factor (W Inj) ",
            "name": "PF",
            "type": "uint16",
        }
        p = device.Point(p_def)
        p.value = 3
        assert p.get_value() == 3

        p2 = device.Point(p_def)
        assert p2.get_value() is None

        # pdef w/ sf
        pdef_sf = {
            "name": "TestPoint",
            "type": "uint16",
            "sf": "TestSF"
        }
        # sf point
        sf_p = {
            "name": "TestSF",
            "value": 3,
            "type": "sunssf"
        }

        # computed
        p_sf = device.Point(sf_p)
        p_sf.value = 3
        points = {}
        points['TestSF'] = p_sf
        m2 = device.Model()
        setattr(m2, 'points', points)

        g = device.Group()
        setattr(g, 'points', points)

        p9 = device.Point(pdef_sf, model=m2)
        p9.group = g
        p9.value = 2020
        assert p9.get_value(computed=True) == 2020000.0

        p9.sf_value = -2
        p9.cvalue = 1.16
        assert p9.get_value(computed=True) == 1.16
        assert p9.get_value() == 116


        # computed exception
        m3 = device.Model()
        points2 = {}
        setattr(m3, 'points', points2)

        p10 = device.Point(pdef_sf, model=m3)
        g2 = device.Group()
        setattr(g2, 'points', {})
        p10.group = g2
        p10.value = 2020
        with pytest.raises(device.ModelError) as exc:
            p10.get_value(computed=True)
        assert 'Scale factor TestSF for point TestPoint not found' in str(exc.value)

    def test_set_value(self):
        p_def = {
                "access": "RW",
                "desc": "Power factor setpoint when injecting active power.",
                "label": "Power Factor (W Inj) ",
                "name": "PF",
                "type": "uint16"
                }
        p = device.Point(p_def)
        p.set_value(3)
        assert p.value == 3

        # test computed
        pdef_computed = {
            "name": "TestingComputed",
            "type": "uint16",
            "sf": "TestSF"
        }
        p_SF = device.Point()
        p_SF.value = 2

        points = {}
        points['TestSF'] = p_SF
        m = device.Model()
        setattr(m, 'points', points)

        p3 = device.Point(pdef_computed, model=m)
        g = device.Group
        setattr(g, 'points', {})
        p3.group = g
        p3.set_value(1000, computed=True, dirty=True)
        assert p3.value == 10
        assert p3.dirty

        # test exceptions
        p2_sf = device.Point()
        m2 = device.Model()
        points2 = {}
        points2['TestSF'] = p2_sf
        setattr(m2, 'points', points2)

        p4 = device.Point(pdef_computed, model=m2)
        p4.group = g
        with pytest.raises(device.ModelError) as exc:
            p4.set_value(1000, computed=True)
        assert 'SF field TestSF value not initialized for point TestingComputed' in str(exc.value)

        # test computed float rounding
        p5 = device.Point(pdef_computed, model=m2)
        p5.sf_value = -2
        p5.set_value(1.16, computed=True)
        assert p5.get_value(computed=True) == 1.16
        assert p5.get_value() == 116

    def test_get_mb(self):
        p_def = {
            "name": "ESVLo",
            "type": "uint16",
            "sf": "TestSF"
        }
        p = device.Point(p_def)
        p.value = 3
        assert p.get_mb() == b'\x00\x03'
        p.value = None
        assert p.get_mb() == b'\xff\xff'
        assert p.get_mb(computed=True) == b'\xff\xff'

        # computed
        p.value = 3
        p.sf_required = True
        p.sf_value = 4
        assert p.get_mb(computed=True) == b'\x75\x30'

    def test_set_mb(self):
        p_def = {
            "name": "ESVLo",
            "type": "uint16",
        }
        m = device.Model()
        g = device.Group()
        g.points = {}
        p3 = device.Point(p_def, m)
        p3.group = g
        p3.set_mb(None)
        assert p3.model.error_info == "Error setting value for ESVLo: object of type 'NoneType' has no len()\n"

        # exceptions
        p_def2 = {
            "name": "ESVLo",
            "type": "uint16",
            "sf": "TestSF"
        }
        p_sf = device.Point()
        points = {}
        points['TestSF'] = p_sf
        setattr(m, 'points', points)

        m.error_info = ''
        p4 = device.Point(p_def2, model=m)
        p4.group = g
        p4.set_mb(b'\x00\x03', computed=True)
        assert m.error_info == 'Error setting value for ESVLo: SF field TestSF value not initialized for point ESVLo\n'

        del m.points['TestSF']
        m.error_info = ''
        p5 = device.Point(p_def2, model=m)
        p5.group = g
        p5.set_mb(b'\x00\x04', computed=True)
        assert m.error_info == 'Error setting value for ESVLo: Scale factor TestSF for point ESVLo not found\n'

        # test computed
        pdef_computed = {
            "name": "TestingComputed",
            "type": "uint16",
            "sf": "TestSF"
        }
        p_SF = device.Point()
        p_SF.value = 2

        points = {}
        points['TestSF'] = p_SF
        m = device.Model()
        setattr(m, 'points', points)

        p6 = device.Point(pdef_computed, model=m)
        p6.group = g
        p6.set_mb(b'\x0b\xb8', computed=True, dirty=True)
        assert p6.value == 30
        assert p6.dirty


class TestGroup:
    def test___init__(self):
        g_704 = {
            "group": {
                "groups": [
                    {
                        "name": "PFWInj",
                        "points": [
                            {
                                "name": "PF",
                                "sf": "PF_SF",
                                "type": "uint16"
                            },
                        ],
                        "type": "sync"
                    },
                    {
                        "name": "PFWInjRvrt",
                        "points": [
                            {
                                "name": "Ext",
                                "type": "enum16"
                            }
                        ],
                        "type": "sync"
                    },
                ],
                "name": "DERCtlAC",
                "points": [
                    {
                        "name": "ID",
                        "type": "uint16",
                        "value": 704
                    },
                    {
                        "name": "L",
                        "static": "S",
                        "type": "uint16"
                    },

                    {
                        "name": "PFWInjRvrtTms",
                        "type": "uint32",
                    },
                    {
                        "name": "PFWInjRvrtRem",
                        "type": "uint32",
                    },
                    {
                        "name": "PFWAbsEna",
                        "type": "enum16"
                    },
                    {
                        "name": "PF_SF",
                        "type": "sunssf"
                    }
                ],
                "type": "group"
            },
            "id": 704
        }
        g = device.Group(g_704['group'])

        assert g.gdef == g_704['group']
        assert g.model is None
        assert g.gname == 'DERCtlAC'
        assert g.offset == 0
        assert g.len == 10
        assert len(g.points) == 6
        assert len(g.groups) == 2
        assert g.points_len == 8
        assert g.group_class == device.Group

    def test___getattr__(self):
        g_704 = {
            "group": {
                "groups": [
                    {
                        "name": "PFWInj",
                        "points": [
                            {
                                "name": "PF",
                                "sf": "PF_SF",
                                "type": "uint16"
                            },
                        ],
                        "type": "sync"
                    },
                    {
                        "name": "PFWInjRvrt",
                        "points": [
                            {
                                "name": "Ext",
                                "type": "enum16"
                            }
                        ],
                        "type": "sync"
                    },
                ],
                "name": "DERCtlAC",
                "points": [
                    {
                        "name": "ID",
                        "type": "uint16",
                        "value": 704
                    },
                    {
                        "name": "L",
                        "static": "S",
                        "type": "uint16"
                    },

                    {
                        "name": "PFWInjRvrtTms",
                        "type": "uint32",
                    },
                    {
                        "name": "PFWInjRvrtRem",
                        "type": "uint32",
                    },
                    {
                        "name": "PFWAbsEna",
                        "type": "enum16"
                    },
                    {
                        "name": "PF_SF",
                        "type": "sunssf"
                    }
                ],
                "type": "group"
            },
            "id": 704
        }
        g = device.Group(g_704['group'])
        with pytest.raises(AttributeError) as exc:
            g.qwerty
        assert "Group object has no attribute qwerty" in str(exc.value)
        assert g.ID
        assert g.PFWAbsEna

    def test__group_data(self):
        gdef_705 = {
            "group": {
                "groups": [
                    {
                        "count": "NCrv",
                        "groups": [
                            {
                                "count": "NPt",
                                "name": "Pt",
                                "points": [
                                    {
                                        "name": "V",
                                        "sf": "V_SF",
                                        "type": "uint16",
                                    },
                                    {
                                        "name": "Var",
                                        "sf": "DeptRef_SF",
                                        "type": "int16",
                                        "units": "VarPct"
                                    }
                                ],
                                "type": "group"
                            }
                        ],
                        "name": "Crv",
                        "points": [
                            {
                                "name": "ActPt",
                                "type": "uint16"
                            },
                            {
                                "name": "DeptRef",
                                "symbols": [
                                    {
                                        "name": "W_MAX_PCT",
                                        "value": 1
                                    },
                                    {
                                        "name": "VAR_MAX_PCT",
                                        "value": 2
                                    },
                                    {
                                        "name": "VAR_AVAL_PCT",
                                        "value": 3
                                    }
                                ],
                                "type": "enum16"
                            },
                            {
                                "name": "Pri",
                                "symbols": [
                                    {
                                        "name": "ACTIVE",
                                        "value": 1
                                    },
                                    {
                                        "name": "REACTIVE",
                                        "value": 2
                                    },
                                    {
                                        "name": "IEEE_1547",
                                        "value": 3
                                    },
                                    {
                                        "name": "PF",
                                        "value": 4
                                    },
                                    {
                                        "name": "VENDOR",
                                        "value": 5
                                    }
                                ],
                                "type": "enum16"
                            },
                            {
                                "name": "VRef",
                                "type": "uint16"
                            },
                            {
                                "name": "VRefAuto",
                                "symbols": [
                                    {
                                        "name": "DISABLED",
                                        "value": 0
                                    },
                                    {
                                        "name": "ENABLED",
                                        "value": 1
                                    }
                                ],
                                "type": "enum16"
                            },
                            {
                                "name": "VRefTms",
                                "type": "uint16"
                            },
                            {
                                "name": "RspTms",
                                "type": "uint16"
                            },
                            {
                                "name": "ReadOnly",
                                "symbols": [
                                    {
                                        "name": "RW",
                                        "value": 0
                                    },
                                    {
                                        "name": "R",
                                        "value": 1
                                    }
                                ],
                                "type": "enum16"
                            }
                        ],
                        "type": "group"
                    }
                ],
                "name": "DERVoltVar",
                "points": [
                    {
                        "name": "ID",
                        "type": "uint16",
                        "value": 705
                    },
                    {
                        "name": "L",
                        "type": "uint16"
                    },
                    {
                        "name": "Ena",
                        "symbols": [
                            {
                                "name": "DISABLED",
                                "value": 0
                            },
                            {
                                "name": "ENABLED",
                                "value": 1
                            }
                        ],
                        "type": "enum16"
                    },
                    {
                        "name": "CrvSt",
                        "symbols": [
                            {
                                "name": "INACTIVE",
                                "value": 0
                            },
                            {
                                "name": "ACTIVE",
                                "value": 1
                            }
                        ],
                        "type": "enum16"
                    },
                    {
                        "name": "AdptCrvReq",
                        "type": "uint16"
                    },
                    {
                        "name": "AdptCrvRslt",
                        "symbols": [
                            {
                                "name": "IN_PROGRESS",
                                "value": 0
                            },
                            {
                                "name": "COMPLETED",
                                "value": 1
                            },
                            {
                                "name": "FAILED",
                                "value": 2
                            }
                        ],
                        "type": "enum16"
                    },
                    {
                        "name": "NPt",
                        "type": "uint16"
                    },
                    {
                        "name": "NCrv",
                        "type": "uint16"
                    },
                    {
                        "name": "RvrtTms",
                        "type": "uint32"
                    },
                    {
                        "name": "RvrtRem",
                        "type": "uint32"
                    },
                    {
                        "name": "RvrtCrv",
                        "type": "uint16"
                    },
                    {
                        "name": "V_SF",
                        "type": "sunssf"
                    },
                    {
                        "name": "DeptRef_SF",
                        "type": "sunssf"
                    }
                ],
                "type": "group"
            },
            "id": 705
        }
        gdata_705 = {
              "ID": 705,
              "Ena": 1,
              "CrvSt": 1,
              "AdptCrvReq": 0,
              "AdptCrvRslt": 0,
              "NPt": 4,
              "NCrv": 3,
              "RvrtTms": 0,
              "RvrtRem": 0,
              "RvrtCrv": 0,
              "V_SF": -2,
              "DeptRef_SF": -2,
              "Crv": [
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 1,
                  "Pt": [
                    {
                      "V": 9200,
                      "Var": 3000
                    },
                    {
                      "V": 9670,
                      "Var": 0
                    },
                    {
                      "V": 10300,
                      "Var": 0
                    },
                    {
                      "V": 10700,
                      "Var": -3000
                    }
                  ]
                },
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 0,
                  "Pt": [
                    {
                      "V": 9300,
                      "Var": 3000
                    },
                    {
                      "V": 9570,
                      "Var": 0
                    },
                    {
                      "V": 10200,
                      "Var": 0
                    },
                    {
                      "V": 10600,
                      "Var": -4000
                    }
                  ]
                },
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 0,
                  "Pt": [
                    {
                      "V": 9400,
                      "Var": 2000
                    },
                    {
                      "V": 9570,
                      "Var": 0
                    },
                    {
                      "V": 10500,
                      "Var": 0
                    },
                    {
                      "V": 10800,
                      "Var": -2000
                    }
                  ]
                }
              ]
            }
        g = device.Group()
        assert g._group_data(gdata_705, 'Crv') == [{'ActPt': 4, 'DeptRef': 1, 'Pri': 1, 'VRef': 1, 'VRefAuto': 0,
                                                    'VRefTms': 5, 'RspTms': 6, 'ReadOnly': 1,
                                                    'Pt': [{'V': 9200, 'Var': 3000}, {'V': 9670, 'Var': 0},
                                                           {'V': 10300, 'Var': 0}, {'V': 10700, 'Var': -3000}]},
                                                   {'ActPt': 4, 'DeptRef': 1, 'Pri': 1, 'VRef': 1, 'VRefAuto': 0,
                                                    'VRefTms': 5, 'RspTms': 6, 'ReadOnly': 0,
                                                    'Pt': [{'V': 9300, 'Var': 3000}, {'V': 9570, 'Var': 0},
                                                           {'V': 10200, 'Var': 0}, {'V': 10600, 'Var': -4000}]},
                                                   {'ActPt': 4, 'DeptRef': 1, 'Pri': 1, 'VRef': 1, 'VRefAuto': 0,
                                                    'VRefTms': 5, 'RspTms': 6, 'ReadOnly': 0,
                                                    'Pt': [{'V': 9400, 'Var': 2000}, {'V': 9570, 'Var': 0},
                                                           {'V': 10500, 'Var': 0}, {'V': 10800, 'Var': -2000}]}]

        assert g._group_data(gdata_705['Crv'], index=0) == {'ActPt': 4, 'DeptRef': 1, 'Pri': 1, 'VRef': 1,
                                                            'VRefAuto': 0, 'VRefTms': 5, 'RspTms': 6, 'ReadOnly': 1,
                                                            'Pt': [{'V': 9200, 'Var': 3000}, {'V': 9670, 'Var': 0},
                                                                   {'V': 10300, 'Var': 0}, {'V': 10700, 'Var': -3000}]}

    def test__get_data_group_count(self):
        gdata_705 = {
              "ID": 705,
              "Ena": 1,
              "CrvSt": 1,
              "AdptCrvReq": 0,
              "AdptCrvRslt": 0,
              "NPt": 4,
              "NCrv": 3,
              "RvrtTms": 0,
              "RvrtRem": 0,
              "RvrtCrv": 0,
              "V_SF": -2,
              "DeptRef_SF": -2,
              "Crv": [
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 1,
                  "Pt": [
                    {
                      "V": 9200,
                      "Var": 3000
                    },
                    {
                      "V": 9670,
                      "Var": 0
                    },
                    {
                      "V": 10300,
                      "Var": 0
                    },
                    {
                      "V": 10700,
                      "Var": -3000
                    }
                  ]
                },
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 0,
                  "Pt": [
                    {
                      "V": 9300,
                      "Var": 3000
                    },
                    {
                      "V": 9570,
                      "Var": 0
                    },
                    {
                      "V": 10200,
                      "Var": 0
                    },
                    {
                      "V": 10600,
                      "Var": -4000
                    }
                  ]
                },
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 0,
                  "Pt": [
                    {
                      "V": 9400,
                      "Var": 2000
                    },
                    {
                      "V": 9570,
                      "Var": 0
                    },
                    {
                      "V": 10500,
                      "Var": 0
                    },
                    {
                      "V": 10800,
                      "Var": -2000
                    }
                  ]
                }
              ]
            }
        g = device.Group()
        assert g._get_data_group_count(gdata_705['Crv']) == 3

    def test__init_repeating_group(self):
        gdef_705 = {
            "group": {
                "groups": [
                    {
                        "count": "NCrv",
                        "groups": [
                            {
                                "count": "NPt",
                                "name": "Pt",
                                "points": [
                                    {
                                        "name": "V",
                                        "sf": "V_SF",
                                        "type": "uint16",
                                    },
                                    {
                                        "name": "Var",
                                        "sf": "DeptRef_SF",
                                        "type": "int16",
                                        "units": "VarPct"
                                    }
                                ],
                                "type": "group"
                            }
                        ],
                        "name": "Crv",
                        "points": [
                            {
                                "name": "ActPt",
                                "type": "uint16"
                            },
                            {
                                "name": "DeptRef",
                                "symbols": [
                                    {
                                        "name": "W_MAX_PCT",
                                        "value": 1
                                    },
                                    {
                                        "name": "VAR_MAX_PCT",
                                        "value": 2
                                    },
                                    {
                                        "name": "VAR_AVAL_PCT",
                                        "value": 3
                                    }
                                ],
                                "type": "enum16"
                            },
                            {
                                "name": "Pri",
                                "symbols": [
                                    {
                                        "name": "ACTIVE",
                                        "value": 1
                                    },
                                    {
                                        "name": "REACTIVE",
                                        "value": 2
                                    },
                                    {
                                        "name": "IEEE_1547",
                                        "value": 3
                                    },
                                    {
                                        "name": "PF",
                                        "value": 4
                                    },
                                    {
                                        "name": "VENDOR",
                                        "value": 5
                                    }
                                ],
                                "type": "enum16"
                            },
                            {
                                "name": "VRef",
                                "type": "uint16"
                            },
                            {
                                "name": "VRefAuto",
                                "symbols": [
                                    {
                                        "name": "DISABLED",
                                        "value": 0
                                    },
                                    {
                                        "name": "ENABLED",
                                        "value": 1
                                    }
                                ],
                                "type": "enum16"
                            },
                            {
                                "name": "VRefTms",
                                "type": "uint16"
                            },
                            {
                                "name": "RspTms",
                                "type": "uint16"
                            },
                            {
                                "name": "ReadOnly",
                                "symbols": [
                                    {
                                        "name": "RW",
                                        "value": 0
                                    },
                                    {
                                        "name": "R",
                                        "value": 1
                                    }
                                ],
                                "type": "enum16"
                            }
                        ],
                        "type": "group"
                    }
                ],
                "name": "DERVoltVar",
                "points": [
                    {
                        "name": "ID",
                        "type": "uint16",
                        "value": 705
                    },
                    {
                        "name": "L",
                        "type": "uint16"
                    },
                    {
                        "name": "Ena",
                        "symbols": [
                            {
                                "name": "DISABLED",
                                "value": 0
                            },
                            {
                                "name": "ENABLED",
                                "value": 1
                            }
                        ],
                        "type": "enum16"
                    },
                    {
                        "name": "CrvSt",
                        "symbols": [
                            {
                                "name": "INACTIVE",
                                "value": 0
                            },
                            {
                                "name": "ACTIVE",
                                "value": 1
                            }
                        ],
                        "type": "enum16"
                    },
                    {
                        "name": "AdptCrvReq",
                        "type": "uint16"
                    },
                    {
                        "name": "AdptCrvRslt",
                        "symbols": [
                            {
                                "name": "IN_PROGRESS",
                                "value": 0
                            },
                            {
                                "name": "COMPLETED",
                                "value": 1
                            },
                            {
                                "name": "FAILED",
                                "value": 2
                            }
                        ],
                        "type": "enum16"
                    },
                    {
                        "name": "NPt",
                        "type": "uint16"
                    },
                    {
                        "name": "NCrv",
                        "type": "uint16"
                    },
                    {
                        "name": "RvrtTms",
                        "type": "uint32"
                    },
                    {
                        "name": "RvrtRem",
                        "type": "uint32"
                    },
                    {
                        "name": "RvrtCrv",
                        "type": "uint16"
                    },
                    {
                        "name": "V_SF",
                        "type": "sunssf"
                    },
                    {
                        "name": "DeptRef_SF",
                        "type": "sunssf"
                    }
                ],
                "type": "group"
            },
            "id": 705
        }
        gdata_705 = {
              "ID": 705,
              "Ena": 1,
              "CrvSt": 1,
              "AdptCrvReq": 0,
              "AdptCrvRslt": 0,
              "NPt": 4,
              "NCrv": 3,
              "RvrtTms": 0,
              "RvrtRem": 0,
              "RvrtCrv": 0,
              "V_SF": -2,
              "DeptRef_SF": -2,
              "Crv": [
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 1,
                  "Pt": [
                    {
                      "V": 9200,
                      "Var": 3000
                    },
                    {
                      "V": 9670,
                      "Var": 0
                    },
                    {
                      "V": 10300,
                      "Var": 0
                    },
                    {
                      "V": 10700,
                      "Var": -3000
                    }
                  ]
                },
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 0,
                  "Pt": [
                    {
                      "V": 9300,
                      "Var": 3000
                    },
                    {
                      "V": 9570,
                      "Var": 0
                    },
                    {
                      "V": 10200,
                      "Var": 0
                    },
                    {
                      "V": 10600,
                      "Var": -4000
                    }
                  ]
                },
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 0,
                  "Pt": [
                    {
                      "V": 9400,
                      "Var": 2000
                    },
                    {
                      "V": 9570,
                      "Var": 0
                    },
                    {
                      "V": 10500,
                      "Var": 0
                    },
                    {
                      "V": 10800,
                      "Var": -2000
                    }
                  ]
                }
              ]
            }

        m = device.Model(705, data=gdata_705)

        pdef_NPt = {"name": "NPt", "type": "uint16"}
        p_NPt = device.Point(pdef_NPt)
        p_NPt.value = 4

        pdef_NCrv = {"name": "NCrv", "type": "uint16"}
        p_NCrv = device.Point(pdef_NCrv)
        points = {'NPt': p_NPt, 'NCrv': p_NCrv}
        setattr(m, 'points', points)

        g2 = device.Group(gdef_705['group']['groups'][0], m)

        with pytest.raises(device.ModelError) as exc:
            g2._init_repeating_group(gdef_705['group']['groups'][0], 0, gdata_705, 0)
        assert 'Count field NCrv value not initialized for group Crv' in str(exc.value)

        # set value for NCrv count and reset the points attribute on model
        p_NCrv.value = 3
        setattr(m, 'points', points)
        groups = g2._init_repeating_group(gdef_705['group']['groups'][0], 0, gdata_705, 0)
        assert len(groups) == 3
        assert len(groups[0].groups['Pt']) == 4

    def test_get_dict(self):
        gdata_705 = {
              "ID": 705,
              "Ena": 1,
              "CrvSt": 1,
              "AdptCrvReq": 0,
              "AdptCrvRslt": 0,
              "NPt": 4,
              "NCrv": 3,
              "RvrtTms": 0,
              "RvrtRem": 0,
              "RvrtCrv": 0,
              "V_SF": -2,
              "DeptRef_SF": -2,
              "Crv": [
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 1,
                  "Pt": [
                    {
                      "V": 9200,
                      "Var": 3000
                    },
                    {
                      "V": 9670,
                      "Var": 0
                    },
                    {
                      "V": 10300,
                      "Var": 0
                    },
                    {
                      "V": 10700,
                      "Var": -3000
                    }
                  ]
                },
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 0,
                  "Pt": [
                    {
                      "V": 9300,
                      "Var": 3000
                    },
                    {
                      "V": 9570,
                      "Var": 0
                    },
                    {
                      "V": 10200,
                      "Var": 0
                    },
                    {
                      "V": 10600,
                      "Var": -4000
                    }
                  ]
                },
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 0,
                  "Pt": [
                    {
                      "V": 9400,
                      "Var": 2000
                    },
                    {
                      "V": 9570,
                      "Var": 0
                    },
                    {
                      "V": 10500,
                      "Var": 0
                    },
                    {
                      "V": 10800,
                      "Var": -2000
                    }
                  ]
                }
              ]
            }
        m2 = device.Model(705, data=gdata_705)
        assert m2.groups['Crv'][0].get_dict() == {'ActPt': 4, 'DeptRef': 1, 'Pri': 1, 'VRef': 1, 'VRefAuto': 0,
                                                  'VRefAutoEna': None, 'VRefAutoTms': None,
                                                  'RspTms': 6, 'ReadOnly': 1,
                                                  'Pt': [{'V': 9200, 'Var': 3000}, {'V': 9670, 'Var': 0},
                                                         {'V': 10300, 'Var': 0},
                                                         {'V': 10700, 'Var': -3000}]}

        # test computed
        m2.groups['Crv'][0].points['DeptRef'].sf_required = True
        m2.groups['Crv'][0].points['DeptRef'].sf_value = -2
        m2.groups['Crv'][0].DeptRef.cvalue = 1.16
        m2.groups['Crv'][0].points['Pri'].sf_required = True
        m2.groups['Crv'][0].points['Pri'].sf_value = 3
        computed_dict = m2.groups['Crv'][0].get_dict(computed=True)
        assert computed_dict['DeptRef'] == 1.16
        assert computed_dict['Pri'] == 1000.0

    def test_set_dict(self):
        gdata_705 = {
            "ID": 705,
            "Ena": 1,
            "CrvSt": 1,
            "AdptCrvReq": 0,
            "AdptCrvRslt": 0,
            "NPt": 4,
            "NCrv": 3,
            "RvrtTms": 0,
            "RvrtRem": 0,
            "RvrtCrv": 0,
            "V_SF": -2,
            "DeptRef_SF": -2,
            "RspTms_SF": 1,
            "Crv": [
                {
                    "ActPt": 4,
                    "DeptRef": 1,
                    "Pri": 1,
                    "VRef": 1,
                    "VRefAuto": 0,
                    "VRefTms": 5,
                    "RspTms": 6,
                    "ReadOnly": 1,
                    "Pt": [
                        {
                            "V": 9200,
                            "Var": 3000
                        },
                        {
                            "V": 9670,
                            "Var": 0
                        },
                        {
                            "V": 10300,
                            "Var": 0
                        },
                        {
                            "V": 10700,
                            "Var": -3000
                        }
                    ]
                },
                {
                    "ActPt": 4,
                    "DeptRef": 1,
                    "Pri": 1,
                    "VRef": 1,
                    "VRefAuto": 0,
                    "VRefTms": 5,
                    "RspTms": 6,
                    "ReadOnly": 0,
                    "Pt": [
                        {
                            "V": 9300,
                            "Var": 3000
                        },
                        {
                            "V": 9570,
                            "Var": 0
                        },
                        {
                            "V": 10200,
                            "Var": 0
                        },
                        {
                            "V": 10600,
                            "Var": -4000
                        }
                    ]
                },
                {
                    "ActPt": 4,
                    "DeptRef": 1,
                    "Pri": 1,
                    "VRef": 1,
                    "VRefAuto": 0,
                    "VRefTms": 5,
                    "RspTms": 6,
                    "ReadOnly": 0,
                    "Pt": [
                        {
                            "V": 9400,
                            "Var": 2000
                        },
                        {
                            "V": 9570,
                            "Var": 0
                        },
                        {
                            "V": 10500,
                            "Var": 0
                        },
                        {
                            "V": 10800,
                            "Var": -2000
                        }
                    ]
                }
            ]
        }
        m = device.Model(705, data=gdata_705)
        assert m.groups['Crv'][0].get_dict() == {'ActPt': 4, 'DeptRef': 1, 'Pri': 1, 'VRef': 1, 'VRefAuto': 0,
                                                 'VRefAutoEna': None, 'VRefAutoTms': None,
                                                 'RspTms': 6, 'ReadOnly': 1,
                                                 'Pt': [{'V': 9200, 'Var': 3000}, {'V': 9670, 'Var': 0},
                                                        {'V': 10300, 'Var': 0},
                                                        {'V': 10700, 'Var': -3000}]}
        new_dict = {'ActPt': 4, 'DeptRef': 4000, 'Pri': 5000, 'VRef': 3, 'VRefAuto': 2,
                                                 'VRefAutoEna': None, 'VRefAutoTms': None,
                                                 'RspTms': 2, 'ReadOnly': 2,
                                                 'Pt': [{'V': 111, 'Var': 111}, {'V': 123, 'Var': 1112},
                                                        {'V': 111, 'Var': 111},
                                                        {'V': 123, 'Var': -1112}]}

        m.groups['Crv'][0].set_dict(new_dict, dirty=True)
        assert m.groups['Crv'][0].get_dict() == new_dict
        assert m.groups['Crv'][0].VRef.value == 3
        assert m.groups['Crv'][0].VRef.dirty
        assert m.groups['Crv'][0].Pri.dirty

        m.groups['Crv'][0].points['DeptRef'].sf_required = True
        m.groups['Crv'][0].points['DeptRef'].sf_value = 3
        m.groups['Crv'][0].points['Pri'].sf_required = True
        m.groups['Crv'][0].points['Pri'].sf_value = 3
        m.groups['Crv'][0].set_dict(new_dict, computed=True)
        computed_dict = m.groups['Crv'][0].get_dict()
        assert computed_dict['DeptRef'] == 4.0
        assert computed_dict['Pri'] == 5.0

        m.groups['Crv'][0].DeptRef.sf_value = -2
        float_dict = {'DeptRef': 1.16}
        m.groups['Crv'][0].set_dict(float_dict, computed=True)
        assert m.groups['Crv'][0].DeptRef.value == 116
        assert m.groups['Crv'][0].DeptRef.cvalue == 1.16

    def test_get_json(self):
        gdata_705 = {
            "ID": 705,
            "Ena": 1,
            "CrvSt": 1,
            "AdptCrvReq": 0,
            "AdptCrvRslt": 0,
            "NPt": 4,
            "NCrv": 3,
            "RvrtTms": 0,
            "RvrtRem": 0,
            "RvrtCrv": 0,
            "V_SF": -2,
            "DeptRef_SF": -2,
            "Crv": [
                {
                    "ActPt": 4,
                    "DeptRef": 1,
                    "Pri": 1,
                    "VRef": 1,
                    "VRefAuto": 0,
                    "VRefTms": 5,
                    "RspTms": 6,
                    "ReadOnly": 1,
                    "Pt": [
                        {
                            "V": 9200,
                            "Var": 3000
                        },
                        {
                            "V": 9670,
                            "Var": 0
                        },
                        {
                            "V": 10300,
                            "Var": 0
                        },
                        {
                            "V": 10700,
                            "Var": -3000
                        }
                    ]
                },
                {
                    "ActPt": 4,
                    "DeptRef": 1,
                    "Pri": 1,
                    "VRef": 1,
                    "VRefAuto": 0,
                    "VRefTms": 5,
                    "RspTms": 6,
                    "ReadOnly": 0,
                    "Pt": [
                        {
                            "V": 9300,
                            "Var": 3000
                        },
                        {
                            "V": 9570,
                            "Var": 0
                        },
                        {
                            "V": 10200,
                            "Var": 0
                        },
                        {
                            "V": 10600,
                            "Var": -4000
                        }
                    ]
                },
                {
                    "ActPt": 4,
                    "DeptRef": 1,
                    "Pri": 1,
                    "VRef": 1,
                    "VRefAuto": 0,
                    "VRefTms": 5,
                    "RspTms": 6,
                    "ReadOnly": 0,
                    "Pt": [
                        {
                            "V": 9400,
                            "Var": 2000
                        },
                        {
                            "V": 9570,
                            "Var": 0
                        },
                        {
                            "V": 10500,
                            "Var": 0
                        },
                        {
                            "V": 10800,
                            "Var": -2000
                        }
                    ]
                }
            ]
        }
        m = device.Model(705, data=gdata_705)
        assert m.groups['Crv'][0].get_json() == '''{"ActPt": 4, "DeptRef": 1, "Pri": 1, "VRef": 1,''' + \
               ''' "VRefAuto": 0, "VRefAutoEna": null, "VRefAutoTms": null, "RspTms": 6, "ReadOnly": 1,''' + \
               ''' "Pt": [{"V": 9200, "Var": 3000}, {"V": 9670, "Var": 0}, {"V": 10300, "Var": 0},''' + \
               ''' {"V": 10700, "Var": -3000}]}'''

        # test computed
        m.groups['Crv'][0].points['DeptRef'].sf_required = True
        m.groups['Crv'][0].points['DeptRef'].sf_value = 3
        m.groups['Crv'][0].points['Pri'].sf_required = True
        m.groups['Crv'][0].points['Pri'].sf_value = 3
        assert m.groups['Crv'][0].get_json(computed=True) == '''{"ActPt": 4, "DeptRef": 1000.0,''' + \
               ''' "Pri": 1000.0, "VRef": 1, "VRefAuto": 0, "VRefAutoEna": null, "VRefAutoTms": null,''' + \
               ''' "RspTms": 6, "ReadOnly": 1, "Pt": [{"V": 92.0, "Var": 30.0}, {"V": 96.7, "Var": 0.0},''' + \
               ''' {"V": 103.0, "Var": 0.0}, {"V": 107.0, "Var": -30.0}]}'''

    def test_set_json(self):
        gdata_705 = {
            "ID": 705,
            "Ena": 1,
            "CrvSt": 1,
            "AdptCrvReq": 0,
            "AdptCrvRslt": 0,
            "NPt": 4,
            "NCrv": 3,
            "RvrtTms": 0,
            "RvrtRem": 0,
            "RvrtCrv": 0,
            "V_SF": -2,
            "DeptRef_SF": -2,
            "RspTms_SF": 1,
            "Crv": [
                {
                    "ActPt": 4,
                    "DeptRef": 1,
                    "Pri": 1,
                    "VRef": 1,
                    "VRefAuto": 0,
                    "VRefTms": 5,
                    "RspTms": 6,
                    "ReadOnly": 1,
                    "Pt": [
                        {
                            "V": 9200,
                            "Var": 3000
                        },
                        {
                            "V": 9670,
                            "Var": 0
                        },
                        {
                            "V": 10300,
                            "Var": 0
                        },
                        {
                            "V": 10700,
                            "Var": -3000
                        }
                    ]
                },
                {
                    "ActPt": 4,
                    "DeptRef": 1,
                    "Pri": 1,
                    "VRef": 1,
                    "VRefAuto": 0,
                    "VRefTms": 5,
                    "RspTms": 6,
                    "ReadOnly": 0,
                    "Pt": [
                        {
                            "V": 9300,
                            "Var": 3000
                        },
                        {
                            "V": 9570,
                            "Var": 0
                        },
                        {
                            "V": 10200,
                            "Var": 0
                        },
                        {
                            "V": 10600,
                            "Var": -4000
                        }
                    ]
                },
                {
                    "ActPt": 4,
                    "DeptRef": 1,
                    "Pri": 1,
                    "VRef": 1,
                    "VRefAuto": 0,
                    "VRefTms": 5,
                    "RspTms": 6,
                    "ReadOnly": 0,
                    "Pt": [
                        {
                            "V": 9400,
                            "Var": 2000
                        },
                        {
                            "V": 9570,
                            "Var": 0
                        },
                        {
                            "V": 10500,
                            "Var": 0
                        },
                        {
                            "V": 10800,
                            "Var": -2000
                        }
                    ]
                }
            ]
        }
        m = device.Model(705, data=gdata_705)
        assert m.groups['Crv'][0].get_json() == '''{"ActPt": 4, "DeptRef": 1, "Pri": 1, "VRef": 1,''' + \
               ''' "VRefAuto": 0, "VRefAutoEna": null, "VRefAutoTms": null, "RspTms": 6,''' + \
               ''' "ReadOnly": 1, "Pt": [{"V": 9200, "Var": 3000}, {"V": 9670, "Var": 0},''' + \
               ''' {"V": 10300, "Var": 0}, {"V": 10700, "Var": -3000}]}'''

        json_to_set = '''{"ActPt": 4, "DeptRef": 9999, "Pri": 9999, "VRef": 99, "VRefAuto": 88,''' + \
                      ''' "VRefAutoEna": null, "VRefAutoTms": 2, "RspTms": 2, "ReadOnly": 77,''' + \
                      ''' "Pt": [{"V": 77, "Var": 66}, {"V": 55, "Var": 44}, {"V": 33, "Var": 22},''' + \
                      ''' {"V": 111, "Var": -2222}]}'''

        m.groups['Crv'][0].set_json(json_to_set)
        assert m.groups['Crv'][0].get_json() == json_to_set
        assert m.groups['Crv'][0].DeptRef.value == 9999

        # test computed
        m.groups['Crv'][0].points['DeptRef'].sf_required = True
        m.groups['Crv'][0].points['DeptRef'].sf_value = 3
        m.groups['Crv'][0].points['Pri'].sf_required = True
        m.groups['Crv'][0].points['Pri'].sf_value = 3
        m.groups['Crv'][0].set_json(json_to_set, computed=True, dirty=True)
        assert m.groups['Crv'][0].points['DeptRef'].value == 10
        assert m.groups['Crv'][0].points['DeptRef'].dirty
        assert m.groups['Crv'][0].points['Pri'].value == 10
        assert m.groups['Crv'][0].points['Pri'].dirty

    def test_get_mb(self):
        gdata_705 = {
            "ID": 705,
            "Ena": 1,
            "CrvSt": 1,
            "AdptCrvReq": 0,
            "AdptCrvRslt": 0,
            "NPt": 4,
            "NCrv": 3,
            "RvrtTms": 0,
            "RvrtRem": 0,
            "RvrtCrv": 0,
            "V_SF": -2,
            "DeptRef_SF": -2,
            "Crv": [
                {
                    "ActPt": 4,
                    "DeptRef": 1,
                    "Pri": 1,
                    "VRef": 1,
                    "VRefAuto": 0,
                    "VRefTms": 5,
                    "RspTms": 6,
                    "ReadOnly": 1,
                    "Pt": [
                        {
                            "V": 9200,
                            "Var": 3000
                        },
                        {
                            "V": 9670,
                            "Var": 0
                        },
                        {
                            "V": 10300,
                            "Var": 0
                        },
                        {
                            "V": 10700,
                            "Var": -3000
                        }
                    ]
                },
                {
                    "ActPt": 4,
                    "DeptRef": 1,
                    "Pri": 1,
                    "VRef": 1,
                    "VRefAuto": 0,
                    "VRefTms": 5,
                    "RspTms": 6,
                    "ReadOnly": 0,
                    "Pt": [
                        {
                            "V": 9300,
                            "Var": 3000
                        },
                        {
                            "V": 9570,
                            "Var": 0
                        },
                        {
                            "V": 10200,
                            "Var": 0
                        },
                        {
                            "V": 10600,
                            "Var": -4000
                        }
                    ]
                },
                {
                    "ActPt": 4,
                    "DeptRef": 1,
                    "Pri": 1,
                    "VRef": 1,
                    "VRefAuto": 0,
                    "VRefTms": 5,
                    "RspTms": 6,
                    "ReadOnly": 0,
                    "Pt": [
                        {
                            "V": 9400,
                            "Var": 2000
                        },
                        {
                            "V": 9570,
                            "Var": 0
                        },
                        {
                            "V": 10500,
                            "Var": 0
                        },
                        {
                            "V": 10800,
                            "Var": -2000
                        }
                    ]
                }
            ]
        }
        m = device.Model(705, data=gdata_705)
        assert m.groups['Crv'][0].get_mb() == b'\x00\x04\x00\x01\x00\x01\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00' \
                                              b'\x00\x06\x00\x01#\xf0\x0b\xb8%\xc6\x00\x00(<\x00\x00)\xcc\xf4H'

        # test computed
        m.groups['Crv'][0].points['DeptRef'].sf_required = True
        m.groups['Crv'][0].points['DeptRef'].sf_value = 3
        m.groups['Crv'][0].points['Pri'].sf_required = True
        m.groups['Crv'][0].points['Pri'].sf_value = 3
        assert m.groups['Crv'][0].get_mb(computed=True) == b'\x00\x04\x03\xe8\x03\xe8\x00\x01\x00\x00\xff\xff\xff' \
                                                           b'\xff\x00\x00\x00\x06\x00\x01\x00\\\x00\x1e\x00`\x00\x00' \
                                                           b'\x00g\x00\x00\x00k\xff\xe2'

    def test_set_mb(self):
        gdata_705 = {
            "ID": 705,
            "Ena": 1,
            "CrvSt": 1,
            "AdptCrvReq": 0,
            "AdptCrvRslt": 0,
            "NPt": 4,
            "NCrv": 3,
            "RvrtTms": 0,
            "RvrtRem": 0,
            "RvrtCrv": 0,
            "V_SF": -2,
            "DeptRef_SF": -2,
            "Crv": [
                {
                    "ActPt": 4,
                    "DeptRef": 1,
                    "Pri": 1,
                    "VRef": 1,
                    "VRefAuto": 0,
                    "VRefTms": 5,
                    "RspTms": 6,
                    "ReadOnly": 1,
                    "Pt": [
                        {
                            "V": 9200,
                            "Var": 3000
                        },
                        {
                            "V": 9670,
                            "Var": 0
                        },
                        {
                            "V": 10300,
                            "Var": 0
                        },
                        {
                            "V": 10700,
                            "Var": -3000
                        }
                    ]
                },
                {
                    "ActPt": 4,
                    "DeptRef": 1,
                    "Pri": 1,
                    "VRef": 1,
                    "VRefAuto": 0,
                    "VRefTms": 5,
                    "RspTms": 6,
                    "ReadOnly": 0,
                    "Pt": [
                        {
                            "V": 9300,
                            "Var": 3000
                        },
                        {
                            "V": 9570,
                            "Var": 0
                        },
                        {
                            "V": 10200,
                            "Var": 0
                        },
                        {
                            "V": 10600,
                            "Var": -4000
                        }
                    ]
                },
                {
                    "ActPt": 4,
                    "DeptRef": 1,
                    "Pri": 1,
                    "VRef": 1,
                    "VRefAuto": 0,
                    "VRefTms": 5,
                    "RspTms": 6,
                    "ReadOnly": 0,
                    "Pt": [
                        {
                            "V": 9400,
                            "Var": 2000
                        },
                        {
                            "V": 9570,
                            "Var": 0
                        },
                        {
                            "V": 10500,
                            "Var": 0
                        },
                        {
                            "V": 10800,
                            "Var": -2000
                        }
                    ]
                }
            ]
        }
        m = device.Model(705, data=gdata_705)
        assert m.groups['Crv'][0].get_mb() == b'\x00\x04\x00\x01\x00\x01\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00' \
                                              b'\x00\x06\x00\x01#\xf0\x0b\xb8%\xc6\x00\x00(<\x00\x00)\xcc\xf4H'

        bs = b'\x00\x04\x03\xe7\x03x\x03\t\x02\x9a\x02+\x01\xbc\x01M\x00\xde\x00o' \
             b'\x00\xde\x01M\x01\xbc\x02+\x02\x9a\xfc\xf7\xf4H\x0b\xb8'

        m.groups['Crv'][0].set_mb(bs, dirty=True)
        assert m.groups['Crv'][0].get_mb() == bs
        assert m.groups['Crv'][0].DeptRef.value == 999
        assert m.groups['Crv'][0].DeptRef.dirty

        # test computed
        # set points DeptRef and Pri to 3000 w/ byte string
        computed_bs = b'\x00\x04\x0b\xb8\x0b\xb8\x00\x01\x00\x00\x00\x05\x00\x06\x00\x01#\xf0\x0b\xb8%\xc6\x00\x00(<' \
                      b'\x00\x00)\xcc\xf4H'
        m.groups['Crv'][0].points['DeptRef'].sf_required = True
        m.groups['Crv'][0].points['DeptRef'].sf_value = 3
        m.groups['Crv'][0].points['Pri'].sf_required = True
        m.groups['Crv'][0].points['Pri'].sf_value = 3
        m.groups['Crv'][0].set_mb(computed_bs, computed=True)
        assert m.groups['Crv'][0].points['DeptRef'].value == 3
        assert m.groups['Crv'][0].points['Pri'].value == 3


class TestModel:
    def test__init__(self):
        m = device.Model(704)
        assert m.model_id == 704
        assert m.model_addr == 0
        assert m.model_len == 0
        assert m.model_def['id'] == 704
        assert m.error_info == ''
        assert m.gdef['name'] == 'DERCtlAC'
        assert m.mid is None
        assert m.device is None

        assert m.model == m
        m2 = device.Model('abc')
        assert m2.error_info == 'Invalid model id: abc\n'

        gdata_705 = {
              "ID": 705,
              "Ena": 1,
              "CrvSt": 1,
              "AdptCrvReq": 0,
              "AdptCrvRslt": 0,
              "NPt": 4,
              "NCrv": 3,
              "RvrtTms": 0,
              "RvrtRem": 0,
              "RvrtCrv": 0,
              "V_SF": -2,
              "DeptRef_SF": -2,
              "Crv": [
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 1,
                  "Pt": [
                    {
                      "V": 9200,
                      "Var": 3000
                    },
                    {
                      "V": 9670,
                      "Var": 0
                    },
                    {
                      "V": 10300,
                      "Var": 0
                    },
                    {
                      "V": 10700,
                      "Var": -3000
                    }
                  ]
                },
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 0,
                  "Pt": [
                    {
                      "V": 9300,
                      "Var": 3000
                    },
                    {
                      "V": 9570,
                      "Var": 0
                    },
                    {
                      "V": 10200,
                      "Var": 0
                    },
                    {
                      "V": 10600,
                      "Var": -4000
                    }
                  ]
                },
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 0,
                  "Pt": [
                    {
                      "V": 9400,
                      "Var": 2000
                    },
                    {
                      "V": 9570,
                      "Var": 0
                    },
                    {
                      "V": 10500,
                      "Var": 0
                    },
                    {
                      "V": 10800,
                      "Var": -2000
                    }
                  ]
                }
              ]
            }
        # test repeating group model
        m2 = device.Model(705, data=gdata_705)
        assert m2.model_id == 705
        assert m2.model_addr == 0
        assert m2.model_len == 0
        assert m2.model_def['id'] == 705
        assert m2.error_info == ''
        assert m2.gdef['name'] == 'DERVoltVar'
        assert m2.mid is None
        assert m2.device is None

    def test__error(self):
        m = device.Model(704)
        m.add_error('test error')
        assert m.error_info == 'test error\n'


class TestDevice:
    def test__init__(self):
        d = device.Device()
        assert d.name is None
        assert d.did is None
        assert d.models == {}
        assert d.model_list == []
        assert d.model_class == device.Model

    def test__get_attr__(self):
        d = device.Device()
        m = device.Model()
        setattr(m, 'model_id', 'mid_test')
        setattr(m, 'gname', 'group_test')
        d.add_model(m)
        assert d.mid_test

        with pytest.raises(AttributeError) as exc:
            d.foo
        assert "\'Device\' object has no attribute \'foo\'" in str(exc.value)

    def test_scan(self):
        pass

    def test_add_model(self):
        d = device.Device()
        m = device.Model()
        setattr(m, 'model_id', 'mid_test')
        setattr(m, 'gname', 'group_test')
        d.add_model(m)
        assert d.models['mid_test']
        assert d.models['group_test']
        assert m.device == d

    def test_get_dict(self):
        d = device.Device()
        gdata_705 = {
              "ID": 705,
              "Ena": 1,
              "CrvSt": 1,
              "AdptCrvReq": 0,
              "AdptCrvRslt": 0,
              "NPt": 4,
              "NCrv": 3,
              "RvrtTms": 0,
              "RvrtRem": 0,
              "RvrtCrv": 0,
              "V_SF": -2,
              "DeptRef_SF": -2,
              "Crv": [
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 1,
                  "Pt": [
                    {
                      "V": 9200,
                      "Var": 3000
                    },
                    {
                      "V": 9670,
                      "Var": 0
                    },
                    {
                      "V": 10300,
                      "Var": 0
                    },
                    {
                      "V": 10700,
                      "Var": -3000
                    }
                  ]
                },
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 0,
                  "Pt": [
                    {
                      "V": 9300,
                      "Var": 3000
                    },
                    {
                      "V": 9570,
                      "Var": 0
                    },
                    {
                      "V": 10200,
                      "Var": 0
                    },
                    {
                      "V": 10600,
                      "Var": -4000
                    }
                  ]
                },
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 0,
                  "Pt": [
                    {
                      "V": 9400,
                      "Var": 2000
                    },
                    {
                      "V": 9570,
                      "Var": 0
                    },
                    {
                      "V": 10500,
                      "Var": 0
                    },
                    {
                      "V": 10800,
                      "Var": -2000
                    }
                  ]
                }
              ]
            }
        m = device.Model(705, data=gdata_705)
        d.add_model(m)
        assert d.get_dict() == {'name': None, 'did': None, 'models': [
            {'ID': 705, 'L': 67, 'Ena': 1, 'AdptCrvReq': 0, 'AdptCrvRslt': 0, 'NPt': 4, 'NCrv': 3, 'RvrtTms': 0,
             'RvrtRem': 0, 'RvrtCrv': 0, 'V_SF': -2, 'DeptRef_SF': -2, 'RspTms_SF': None, 'Crv': [
                {'ActPt': 4, 'DeptRef': 1, 'Pri': 1, 'VRef': 1, 'VRefAuto': 0, 'VRefAutoEna': None, 'VRefAutoTms': None,
                 'RspTms': 6, 'ReadOnly': 1,
                 'Pt': [{'V': 9200, 'Var': 3000}, {'V': 9670, 'Var': 0}, {'V': 10300, 'Var': 0},
                        {'V': 10700, 'Var': -3000}]},
                {'ActPt': 4, 'DeptRef': 1, 'Pri': 1, 'VRef': 1, 'VRefAuto': 0, 'VRefAutoEna': None, 'VRefAutoTms': None,
                 'RspTms': 6, 'ReadOnly': 0,
                 'Pt': [{'V': 9300, 'Var': 3000}, {'V': 9570, 'Var': 0}, {'V': 10200, 'Var': 0},
                        {'V': 10600, 'Var': -4000}]},
                {'ActPt': 4, 'DeptRef': 1, 'Pri': 1, 'VRef': 1, 'VRefAuto': 0, 'VRefAutoEna': None, 'VRefAutoTms': None,
                 'RspTms': 6, 'ReadOnly': 0,
                 'Pt': [{'V': 9400, 'Var': 2000}, {'V': 9570, 'Var': 0}, {'V': 10500, 'Var': 0},
                        {'V': 10800, 'Var': -2000}]}], 'mid': None, 'error': '', 'model_id': 705}]}

        # computed
        m.groups['Crv'][0].points['DeptRef'].sf_required = True
        m.groups['Crv'][0].points['DeptRef'].sf_value = 3
        m.groups['Crv'][0].points['Pri'].sf_required = True
        m.groups['Crv'][0].points['Pri'].sf_value = 3
        assert d.get_dict(computed=True) == {'name': None, 'did': None, 'models': [
            {'ID': 705, 'L': 67, 'Ena': 1, 'AdptCrvReq': 0, 'AdptCrvRslt': 0, 'NPt': 4, 'NCrv': 3, 'RvrtTms': 0,
             'RvrtRem': 0, 'RvrtCrv': 0, 'V_SF': -2, 'DeptRef_SF': -2, 'RspTms_SF': None, 'Crv': [
                {'ActPt': 4, 'DeptRef': 1000.0, 'Pri': 1000.0, 'VRef': 1, 'VRefAuto': 0, 'VRefAutoEna': None,
                 'VRefAutoTms': None, 'RspTms': 6, 'ReadOnly': 1,
                 'Pt': [{'V': 92.0, 'Var': 30.0}, {'V': 96.7, 'Var': 0.0}, {'V': 103.0, 'Var': 0.0},
                        {'V': 107.0, 'Var': -30.0}]},
                {'ActPt': 4, 'DeptRef': 1, 'Pri': 1, 'VRef': 1, 'VRefAuto': 0, 'VRefAutoEna': None, 'VRefAutoTms': None,
                 'RspTms': 6, 'ReadOnly': 0,
                 'Pt': [{'V': 93.0, 'Var': 30.0}, {'V': 95.7, 'Var': 0.0}, {'V': 102.0, 'Var': 0.0},
                        {'V': 106.0, 'Var': -40.0}]},
                {'ActPt': 4, 'DeptRef': 1, 'Pri': 1, 'VRef': 1, 'VRefAuto': 0, 'VRefAutoEna': None, 'VRefAutoTms': None,
                 'RspTms': 6, 'ReadOnly': 0,
                 'Pt': [{'V': 94.0, 'Var': 20.0}, {'V': 95.7, 'Var': 0.0}, {'V': 105.0, 'Var': 0.0},
                        {'V': 108.0, 'Var': -20.0}]}], 'mid': None, 'error': '', 'model_id': 705}]}

    def test_get_json(self):
        d = device.Device()
        gdata_705 = {
              "ID": 705,
              "Ena": 1,
              "CrvSt": 1,
              "AdptCrvReq": 0,
              "AdptCrvRslt": 0,
              "NPt": 4,
              "NCrv": 3,
              "RvrtTms": 0,
              "RvrtRem": 0,
              "RvrtCrv": 0,
              "V_SF": -2,
              "DeptRef_SF": -2,
              "Crv": [
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 1,
                  "Pt": [
                    {
                      "V": 9200,
                      "Var": 3000
                    },
                    {
                      "V": 9670,
                      "Var": 0
                    },
                    {
                      "V": 10300,
                      "Var": 0
                    },
                    {
                      "V": 10700,
                      "Var": -3000
                    }
                  ]
                },
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 0,
                  "Pt": [
                    {
                      "V": 9300,
                      "Var": 3000
                    },
                    {
                      "V": 9570,
                      "Var": 0
                    },
                    {
                      "V": 10200,
                      "Var": 0
                    },
                    {
                      "V": 10600,
                      "Var": -4000
                    }
                  ]
                },
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 0,
                  "Pt": [
                    {
                      "V": 9400,
                      "Var": 2000
                    },
                    {
                      "V": 9570,
                      "Var": 0
                    },
                    {
                      "V": 10500,
                      "Var": 0
                    },
                    {
                      "V": 10800,
                      "Var": -2000
                    }
                  ]
                }
              ]
            }
        m = device.Model(705, data=gdata_705)
        d.add_model(m)
        assert d.get_json() == '''{"name": null, "did": null, "models": [{"ID": 705, "L": 67, "Ena": 1,''' + \
               ''' "AdptCrvReq": 0, "AdptCrvRslt": 0, "NPt": 4, "NCrv": 3, "RvrtTms": 0, "RvrtRem": 0,''' + \
               ''' "RvrtCrv": 0, "V_SF": -2, "DeptRef_SF": -2, "RspTms_SF": null, "Crv": [{"ActPt": 4,''' + \
               ''' "DeptRef": 1, "Pri": 1, "VRef": 1, "VRefAuto": 0, "VRefAutoEna": null, "VRefAutoTms": null,''' + \
               ''' "RspTms": 6, "ReadOnly": 1, "Pt": [{"V": 9200, "Var": 3000}, {"V": 9670, "Var": 0},''' + \
               ''' {"V": 10300, "Var": 0}, {"V": 10700, "Var": -3000}]}, {"ActPt": 4, "DeptRef": 1,''' + \
               ''' "Pri": 1, "VRef": 1, "VRefAuto": 0, "VRefAutoEna": null, "VRefAutoTms": null,''' + \
               ''' "RspTms": 6, "ReadOnly": 0, "Pt": [{"V": 9300, "Var": 3000}, {"V": 9570, "Var": 0},''' + \
               ''' {"V": 10200, "Var": 0}, {"V": 10600, "Var": -4000}]}, {"ActPt": 4, "DeptRef": 1,''' + \
               ''' "Pri": 1, "VRef": 1, "VRefAuto": 0, "VRefAutoEna": null, "VRefAutoTms": null,''' + \
               ''' "RspTms": 6, "ReadOnly": 0, "Pt": [{"V": 9400, "Var": 2000}, {"V": 9570, "Var": 0},''' + \
               ''' {"V": 10500, "Var": 0}, {"V": 10800, "Var": -2000}]}], "mid": null, "error": "",''' + \
               ''' "model_id": 705}]}'''

        # computed
        m.groups['Crv'][0].points['DeptRef'].sf_required = True
        m.groups['Crv'][0].points['DeptRef'].sf_value = 3
        m.groups['Crv'][0].points['Pri'].sf_required = True
        m.groups['Crv'][0].points['Pri'].sf_value = 3
        assert d.get_json(computed=True) == '''{"name": null, "did": null, "models": [{"ID": 705,''' + \
               ''' "L": 67, "Ena": 1, "AdptCrvReq": 0, "AdptCrvRslt": 0, "NPt": 4, "NCrv": 3, "RvrtTms": 0,''' + \
               ''' "RvrtRem": 0, "RvrtCrv": 0, "V_SF": -2, "DeptRef_SF": -2, "RspTms_SF": null, ''' + \
               '''"Crv": [{"ActPt": 4, "DeptRef": 1000.0, "Pri": 1000.0, "VRef": 1, "VRefAuto": 0, ''' + \
               '''"VRefAutoEna": null, "VRefAutoTms": null, "RspTms": 6, "ReadOnly": 1, ''' + \
               '''"Pt": [{"V": 92.0, "Var": 30.0}, {"V": 96.7, "Var": 0.0}, {"V": 103.0, "Var": 0.0},''' + \
               ''' {"V": 107.0, "Var": -30.0}]}, {"ActPt": 4, "DeptRef": 1, "Pri": 1, "VRef": 1,''' + \
               ''' "VRefAuto": 0, "VRefAutoEna": null, "VRefAutoTms": null, "RspTms": 6, "ReadOnly": 0,''' + \
               ''' "Pt": [{"V": 93.0, "Var": 30.0}, {"V": 95.7, "Var": 0.0}, {"V": 102.0, "Var": 0.0},''' + \
               ''' {"V": 106.0, "Var": -40.0}]}, {"ActPt": 4, "DeptRef": 1, "Pri": 1, "VRef": 1, "VRefAuto": 0,''' + \
               ''' "VRefAutoEna": null, "VRefAutoTms": null, "RspTms": 6, "ReadOnly": 0,''' + \
               ''' "Pt": [{"V": 94.0, "Var": 20.0}, {"V": 95.7, "Var": 0.0}, {"V": 105.0, "Var": 0.0},''' + \
               ''' {"V": 108.0, "Var": -20.0}]}], "mid": null, "error": "", "model_id": 705}]}'''

    def test_get_mb(self):
        d = device.Device()
        gdata_705 = {
              "ID": 705,
              "Ena": 1,
              "CrvSt": 1,
              "AdptCrvReq": 0,
              "AdptCrvRslt": 0,
              "NPt": 4,
              "NCrv": 3,
              "RvrtTms": 0,
              "RvrtRem": 0,
              "RvrtCrv": 0,
              "V_SF": -2,
              "DeptRef_SF": -2,
              "Crv": [
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 1,
                  "Pt": [
                    {
                      "V": 9200,
                      "Var": 3000
                    },
                    {
                      "V": 9670,
                      "Var": 0
                    },
                    {
                      "V": 10300,
                      "Var": 0
                    },
                    {
                      "V": 10700,
                      "Var": 3000
                    }
                  ]
                },
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 0,
                  "Pt": [
                    {
                      "V": 9300,
                      "Var": 3000
                    },
                    {
                      "V": 9570,
                      "Var": 0
                    },
                    {
                      "V": 10200,
                      "Var": 0
                    },
                    {
                      "V": 10600,
                      "Var": 4000
                    }
                  ]
                },
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 0,
                  "Pt": [
                    {
                      "V": 9400,
                      "Var": 2000
                    },
                    {
                      "V": 9570,
                      "Var": 0
                    },
                    {
                      "V": 10500,
                      "Var": 0
                    },
                    {
                      "V": 10800,
                      "Var": 2000
                    }
                  ]
                }
              ]
            }
        m = device.Model(705, data=gdata_705)
        d.add_model(m)
        assert d.get_mb() == b"\x02\xc1\x00C\x00\x01\x00\x00\x00\x00\x00\x04\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00" \
                             b"\x00\x00\xff\xfe\xff\xfe\x80\x00\x00\x04\x00\x01\x00\x01\x00\x01\x00\x00\xff\xff\xff" \
                             b"\xff\x00\x00\x00\x06\x00\x01#\xf0\x0b\xb8%\xc6\x00\x00(<\x00\x00)\xcc\x0b\xb8\x00\x04" \
                             b"\x00\x01\x00\x01\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x06\x00\x00$T\x0b\xb8%b" \
                             b"\x00\x00'\xd8\x00\x00)h\x0f\xa0\x00\x04\x00\x01\x00\x01\x00\x01\x00\x00\xff\xff\xff" \
                             b"\xff\x00\x00\x00\x06\x00\x00$\xb8\x07\xd0%b\x00\x00)\x04\x00\x00*0\x07\xd0"

        # computed
        m.groups['Crv'][0].points['DeptRef'].sf_required = True
        m.groups['Crv'][0].points['DeptRef'].sf_value = 3
        m.groups['Crv'][0].points['Pri'].sf_required = True
        m.groups['Crv'][0].points['Pri'].sf_value = 3
        assert d.get_mb(computed=True) == b'\x02\xc1\x00C\x00\x01\x00\x00\x00\x00\x00\x04\x00\x03\x00\x00\x00' \
                                          b'\x00\x00\x00\x00\x00\x00\x00\xff\xfe\xff\xfe\x80\x00\x00\x04\x03' \
                                          b'\xe8\x03\xe8\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x06\x00' \
                                          b'\x01\x00\\\x00\x1e\x00`\x00\x00\x00g\x00\x00\x00k\x00\x1e\x00\x04' \
                                          b'\x00\x01\x00\x01\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x06' \
                                          b'\x00\x00\x00]\x00\x1e\x00_\x00\x00\x00f\x00\x00\x00j\x00(\x00\x04' \
                                          b'\x00\x01\x00\x01\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x06' \
                                          b'\x00\x00\x00^\x00\x14\x00_\x00\x00\x00i\x00\x00\x00l\x00\x14'

    def test_set_mb(self):
        d = device.Device()
        gdata_705 = {
              "ID": 705,
              "Ena": 1,
              "CrvSt": 1,
              "AdptCrvReq": 0,
              "AdptCrvRslt": 0,
              "NPt": 4,
              "NCrv": 3,
              "RvrtTms": 0,
              "RvrtRem": 0,
              "RvrtCrv": 0,
              "V_SF": -2,
              "DeptRef_SF": -2,
              "Crv": [
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 1,
                  "Pt": [
                    {
                      "V": 9200,
                      "Var": 3000
                    },
                    {
                      "V": 9670,
                      "Var": 0
                    },
                    {
                      "V": 10300,
                      "Var": 0
                    },
                    {
                      "V": 10700,
                      "Var": 3000
                    }
                  ]
                },
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 0,
                  "Pt": [
                    {
                      "V": 9300,
                      "Var": 3000
                    },
                    {
                      "V": 9570,
                      "Var": 0
                    },
                    {
                      "V": 10200,
                      "Var": 0
                    },
                    {
                      "V": 10600,
                      "Var": 4000
                    }
                  ]
                },
                {
                  "ActPt": 4,
                  "DeptRef": 1,
                  "Pri": 1,
                  "VRef": 1,
                  "VRefAuto": 0,
                  "VRefTms": 5,
                  "RspTms": 6,
                  "ReadOnly": 0,
                  "Pt": [
                    {
                      "V": 9400,
                      "Var": 2000
                    },
                    {
                      "V": 9570,
                      "Var": 0
                    },
                    {
                      "V": 10500,
                      "Var": 0
                    },
                    {
                      "V": 10800,
                      "Var": 2000
                    }
                  ]
                }
              ]
            }
        m = device.Model(705, data=gdata_705)
        d.add_model(m)
        assert d.get_mb() == b"\x02\xc1\x00C\x00\x01\x00\x00\x00\x00\x00\x04\x00\x03\x00\x00\x00\x00\x00\x00\x00" \
                             b"\x00\x00\x00\xff\xfe\xff\xfe\x80\x00\x00\x04\x00\x01\x00\x01\x00\x01\x00\x00\xff" \
                             b"\xff\xff\xff\x00\x00\x00\x06\x00\x01#\xf0\x0b\xb8%\xc6\x00\x00(<\x00\x00)\xcc\x0b" \
                             b"\xb8\x00\x04\x00\x01\x00\x01\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x06\x00" \
                             b"\x00$T\x0b\xb8%b\x00\x00'\xd8\x00\x00)h\x0f\xa0\x00\x04\x00\x01\x00\x01\x00\x01\x00" \
                             b"\x00\xff\xff\xff\xff\x00\x00\x00\x06\x00\x00$\xb8\x07\xd0%b\x00\x00)\x04\x00\x00*0" \
                             b"\x07\xd0"

        # DeptRef and Pri set to 3000 in byte string
        bs = b"\x02\xc1\x00?\x00\x01\x00\x01\x00\x00\x00\x00\x00\x04\x00\x03\x00\x00\x00\x00\x00\x00" \
             b"\x00\x00\x00\x00\xff\xfe\xff\xfe\x00\x04\x0b\xb8\x0b\xb8\x00\x01\x00\x00\x00\x05\x00" \
             b"\x06\x00\x01#\xf0\x0b\xb8%\xc6\x00\x00(<\x00\x00)\xcc\xf4H\x00\x04\x00\x01\x00\x01\x00" \
             b"\x01\x00\x00\x00\x05\x00\x06\x00\x00$T\x0b\xb8%b\x00\x00'\xd8\x00\x00)h\xf0`\x00\x04" \
             b"\x00\x01\x00\x01\x00\x01\x00\x00\x00\x05\x00\x06\x00\x00$\xb8\x07\xd0%b\x00\x00)\x04\x00\x00*0\xf80"
        d.set_mb(bs, dirty=True)
        assert m.groups['Crv'][0].DeptRef.value == 3000
        assert m.groups['Crv'][0].DeptRef.dirty
        assert m.groups['Crv'][0].Pri.value == 3000
        assert m.groups['Crv'][0].Pri.dirty

        # computed
        m.groups['Crv'][0].points['DeptRef'].sf_required = True
        m.groups['Crv'][0].points['DeptRef'].sf_value = 3
        m.groups['Crv'][0].points['Pri'].sf_required = True
        m.groups['Crv'][0].points['Pri'].sf_value = 3
        d.set_mb(bs, computed=True, dirty=False)
        assert m.groups['Crv'][0].DeptRef.value == 3
        assert not m.groups['Crv'][0].DeptRef.dirty
        assert m.groups['Crv'][0].Pri.value == 3
        assert not m.groups['Crv'][0].Pri.dirty

    def test_find_mid(self):
        d = device.Device()
        m = device.Model()
        setattr(m, 'model_id', 'mid_test')
        setattr(m, 'gname', 'group_test')
        setattr(m, 'mid', 'mid_test')
        d.add_model(m)
        assert d.find_mid('mid_test') == m
