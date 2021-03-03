import json
import math
from collections import OrderedDict
import os
import sunspec2.mdef as mdef
import sunspec2.smdx as smdx
import sunspec2.mb as mb


class ModelError(Exception):
    pass

ACCESS_REGION_REGS = 123

this_dir, this_filename = os.path.split(__file__)
models_dir = os.path.join(this_dir, 'models')

model_defs_path = ['.', models_dir]
model_path_options = ['.', 'json', 'smdx']


def get_model_defs_path():
    return model_defs_path


def set_model_defs_path(path_list):
    if not isinstance(path_list, list):
        raise mdef.ModelDefinitionError('Invalid path list type, path list is not a list')
    global model_defs_path
    model_defs_path = path_list


def get_model_info(model_id):
    try:
        glen = 0
        model_def = get_model_def(model_id)
        gdef = model_def.get(mdef.GROUP)
        # check if groups have a count point
        has_group_count = check_group_count(gdef)
        # if group has count point, compute the length of top-level points
        if has_group_count:
            points = gdef.get(mdef.POINTS)
            if points:
                for pdef in points:
                    info = mb.point_type_info.get(pdef[mdef.TYPE])
                    plen = pdef.get(mdef.SIZE, None)
                    if plen is None:
                        glen += info.len
    except:
        raise

    return (model_def, has_group_count, glen)


def check_group_count(gdef):
    has_group_count = (gdef.get(mdef.COUNT) is not None)
    if not has_group_count:
        groups = gdef.get(mdef.GROUPS)
        if groups:
            for g in groups:
                has_group_count = check_group_count(g)
                if has_group_count:
                    break
    return has_group_count


def get_model_def(model_id, mapping=True):
    try:
        model_id = int(model_id)
    except:
        raise mdef.ModelDefinitionError('Invalid model id: %s' % model_id)

    model_def_file_json = mdef.to_json_filename(model_id)
    model_def_file_smdx = smdx.to_smdx_filename(model_id)
    model_def = None
    for path in model_defs_path:
        # look in directory, then json/, then smdx/
        for path_option in model_path_options:
            try:
                model_def = mdef.from_json_file(os.path.join(path, path_option, model_def_file_json))
            except FileNotFoundError:
                pass
            except Exception as e:
                raise mdef.ModelDefinitionError('Error loading model definition for model %s: %s' %
                                                 (model_id, str(e)))

            if model_def is None:
                try:
                    model_def = smdx.from_smdx_file(os.path.join(path, path_option, model_def_file_smdx))
                except FileNotFoundError:
                    pass
                except Exception as e:
                    raise mdef.ModelDefinitionError('Error loading model definition for model %s: %s' %
                                                     (model_id, str(e)))

            if model_def is not None:
                if mapping:
                    add_mappings(model_def[mdef.GROUP])
                return model_def
    raise mdef.ModelDefinitionError('Model definition not found for model %s' % model_id)


# add id mapping for points and groups for more efficient lookup by id
def add_mappings(group_def):
    point_defs = {}
    group_defs = {}

    points = group_def.get(mdef.POINTS, None)
    if points:
        for p in group_def[mdef.POINTS]:
            point_defs[p[mdef.NAME]] = p

    groups = group_def.get(mdef.GROUPS, None)
    if groups:
        for g in group_def[mdef.GROUPS]:
            group_defs[g[mdef.NAME]] = g
            add_mappings(g)

    group_def['point_defs'] = point_defs
    group_def['group_defs'] = group_defs


class Point(object):
    def __init__(self, pdef=None, model=None, group=None, model_offset=0, data=None, data_offset=0):
        self.model = model          # model object containing the point
        self.group = group
        self.pdef = pdef            # point definition
        self.len = 0                # mb register len of point
        self.info = None            # point def info
        self.offset = model_offset  # mb register offset from beginning of the model
        self._value = None          # value
        self.dirty = False          # value has been changed without being written
        self.sf = None              # scale factor point name
        self.sf_value = None        # value of scale factor
        self.sf_required = False    # point has a scale factor
        if pdef:
            self.sf_required = (pdef.get(mdef.SF) is not None)
            if self.sf_required:
                sf = self.pdef.get(mdef.SF)
                try:
                    self.sf_value = int(sf)
                except ValueError:
                    self.sf = sf

            self.info = mb.point_type_info.get(pdef[mdef.TYPE])
            plen = pdef.get(mdef.SIZE, None)
            self.len = self.info.len
            if plen is not None:
                self.len = int(plen)

            if data is not None:
                self._set_data(data=data, offset=data_offset)

    def __str__(self):
        return self.disp()

    def disp(self, indent=None):
        if indent is None:
            indent = ''
        return '%s%s:  %s\n' % (indent, self.pdef[mdef.NAME], self.value)

    def _set_data(self, data=None, offset=0):
        if isinstance(data, (bytes, bytearray)):
            byte_offset = offset * 2
            if byte_offset < len(data):
                self.set_mb(data=data[byte_offset:], dirty=False)
        elif isinstance(data, dict):
            value = data.get(self.pdef[mdef.NAME])
            if value is not None:
                self.set_value(data=value)

    def resolve_sf(self):
        pass

    @property
    def value(self):
        return self.get_value()

    @value.setter
    def value(self, v):
        self.set_value(v, dirty=True)

    @property
    def cvalue(self):
        return self.get_value(computed=True)

    @cvalue.setter
    def cvalue(self, v):
        self.set_value(v, computed=True, dirty=True)

    def get_value(self, computed=False):
        v = self._value
        if computed and v is not None:
            if self.sf_required:
                if self.sf_value is None:
                    if self.sf:
                        sf = self.group.points.get(self.sf)
                        if sf is None:
                            sf = self.model.points.get(self.sf)
                        if sf is not None:
                            self.sf_value = sf.value
                        else:
                            raise ModelError('Scale factor %s for point %s not found' % (self.sf, self.pdef['name']))
            if self.sf_value:
                sfv = self.sf_value
                if sfv:
                    v = v * math.pow(10, sfv)
        return v

    def set_value(self, data=None, computed=False, dirty=None):
        v = data
        if dirty is not None:
            self.dirty = dirty
        if computed:
            if self.sf_required:
                if self.sf_value is None:
                    if self.sf:
                        sf = self.group.points.get(self.sf)
                        if sf is None:
                            sf = self.model.points.get(self.sf)
                        if sf is not None:
                            self.sf_value = sf.value
                            if sf.value is not None:
                                self.sf_value = sf.value
                            else:
                                raise ModelError('SF field %s value not initialized for point %s' %
                                                 (self.sf, self.pdef['name']))
                        else:
                            raise ModelError('Scale factor %s for point %s not found' % (self.sf, self.pdef['name']))
            if self.sf_value:
                self._value = round(round(float(v), abs(self.sf_value)) / math.pow(10, self.sf_value))
            else:
                self._value = v
        else:
            self._value = v

    def get_mb(self, computed=False):
        v = self._value
        data = None
        if computed and v is not None:
            if self.sf_required:
                if self.sf_value is None:
                    if self.sf:
                        sf = self.group.points.get(self.sf)
                        if sf is None:
                            sf = self.model.points.get(self.sf)
                        if sf is not None:
                            self.sf_value = sf.value
                        else:
                            raise ModelError('Scale factor %s for point %s not found' % (self.sf, self.pdef['name']))
            if self.sf_value:
                sfv = self.sf_value
                if sfv:
                    v = int(v * math.pow(10, sfv))
                data = self.info.to_data(v, (int(self.len) * 2))
        elif v is None:
            data = mb.create_unimpl_value(self.pdef[mdef.TYPE], len=(int(self.len) * 2))

        if data is None:
            data = self.info.to_data(v, (int(self.len) * 2))
        return data

    def set_mb(self, data=None, computed=False, dirty=None):
        try:
            mb_len = self.len
            # if not enough data, do not set but consume the data
            if len(data) < mb_len * 2:
                return len(data)
            self.set_value(self.info.data_to(data[:mb_len * 2]), computed=computed, dirty=dirty)
            if not self.info.is_impl(self.value):
                self.set_value(None)
                self.sf_value = None
        except Exception as e:
            self.model.add_error('Error setting value for %s: %s' % (self.pdef[mdef.NAME], str(e)))
        return mb_len

    def is_impl(self):
        impl = False
        v = self.value
        if v is not None:
            impl = self.info.is_impl(self.value)
        return impl


class Group(object):
    def __init__(self, gdef=None, model=None, model_offset=0, group_len=0, data=None, data_offset=0, group_class=None,
                 point_class=None, index=None):
        self.gdef = gdef
        self.model = model
        self.gname = None
        self.offset = model_offset
        self.len = group_len
        self.points = OrderedDict()
        self.groups = OrderedDict()
        self.points_len = 0
        self.group_class = group_class
        self.index = index
        self.access_regions = []

        if group_class is None:
            self.group_class = self.__class__
        if point_class is None:
            point_class = Point

        if gdef is not None:
            self.gname = gdef[mdef.NAME]
            self.gdef = gdef

            # initialize points and point values, if present
            points = self.gdef.get(mdef.POINTS)
            if points:
                for pdef in points:
                    p = point_class(pdef, model=self.model, group=self, model_offset=model_offset, data=data,
                                    data_offset=data_offset)
                    self.points_len += p.len
                    model_offset += p.len
                    data_offset += p.len
                    self.points[pdef[mdef.NAME]] = p
            # initialize groups
            groups = self.gdef.get(mdef.GROUPS)
            if groups:
                for gdef in groups:
                    gdata = self._group_data(data=data, name=gdef[mdef.NAME])
                    if gdef.get(mdef.COUNT) is not None:
                        g = self._init_repeating_group(gdef=gdef, model_offset=model_offset, data=gdata,
                                                       data_offset=data_offset)
                        group_count = len(g)
                        if group_count:
                            self.groups[gdef[mdef.NAME]] = g
                            glen = g[0].len * group_count
                            model_offset += glen
                            data_offset += glen
                    else:
                        g = self.group_class(gdef, model=self.model, model_offset=model_offset, data=gdata,
                                        data_offset=data_offset)
                        self.groups[gdef[mdef.NAME]] = g
                        model_offset += g.len
                        data_offset += g.len
            mlen = model_offset - self.offset
            if self.len:
                if self.len + 2 != mlen:
                    self.model.add_error('Model length %s not equal to calculated model length %s for model %s' %
                                        (self.len + 2, mlen, self.model.model_id ))
            self.len = mlen

        # check if group fits in access region
        if self.len > ACCESS_REGION_REGS:
            if self.points_len > ACCESS_REGION_REGS:
                index = 0
                count = 0
                for p, point in self.points.items():
                    if count + point.len > ACCESS_REGION_REGS:
                        self.access_regions.append((index, count))
                        index = count
                        count = 0
                    count += point.len
                if count > 0:
                    self.access_regions.append((index, count))
            else:
                self.access_regions.append((0, self.points_len))
                groups_len = self.len - self.points_len
                if groups_len > ACCESS_REGION_REGS:
                    for g, group in self.groups.items():
                        if isinstance(group, list) and len(group) > 0:
                            glen = group[0].len
                            if glen > ACCESS_REGION_REGS:
                                raise ModelError('Nested groups too big')
                            index = self.points_len
                            for i in range(len(group)):
                                self.access_regions.append((index, glen))
                                index += glen
                        elif group.len > ACCESS_REGION_REGS:
                            raise ModelError('Nested single group too big')

        len_point = self.points.get('L')
        if len_point:
            len_point.set_value(self.len - 2)

        id_point = self.points.get('ID')
        if id_point:
            id_val = id_point.pdef.get('value')
            if id_val:
                id_point.set_value(id_point.pdef['value'])

    def __getattr__(self, attr):
        v = self.points.get(attr)
        if v is None:
            v = self.groups.get(attr)
        if v is None:
            raise AttributeError("%s object has no attribute %s" % (self.group_class.__name__, attr))
        return v

    def __str__(self):
        return self.disp()

    def disp(self, indent=None):
        if indent is None:
            indent = ''
        if self.index is not None:
            index = '(%s)' % self.index
        else:
            index = ''
        s = '%s%s%s:\n' % (indent, self.gdef[mdef.NAME], index)

        indent += '  '
        for k, p in self.points.items():
            s += p.disp(indent)

        for k, g in self.groups.items():
            if isinstance(g, list):
                for i in range(len(g)):
                    s += g[i].disp(indent=indent)
            else:
                s += g.disp(indent)

        return s

    def _group_data(self, data=None, name=None, index=None):
        if isinstance(data, dict):
            data = data.get(name)
        elif isinstance(data, list):
            if index is not None and len(data) > index:
                data = data[index]
            else:
                data = None
        return data

    # check group count in dict data
    def _get_data_group_count(self, data=None):
        if isinstance(data, list):
            return len(data)

    def _init_repeating_group(self, gdef=None, model_offset=None, data=None, data_offset=0):
        groups = []
        # get group count as a constant
        count = None
        try:
            count = int(gdef[mdef.COUNT])
        except ValueError:
            pass
        except AttributeError:
            self.model.add_error('Count definition %s missing for group %s' % (gdef[mdef.COUNT], gdef[mdef.NAME]))
        if count is None:
            # get count as model point
            count_attr = getattr(self.model, gdef[mdef.COUNT], None)
            if count_attr is None:
                raise ModelError('Count field %s undefined for group %s' % (gdef[mdef.COUNT], gdef[mdef.NAME]))
            count = count_attr.value
        if count is None:
            raise ModelError('Count field %s value not initialized for group %s ' %
                             (gdef[mdef.COUNT], gdef[mdef.NAME]))

        data_group_count = self._get_data_group_count(data=data)
        model_len = self.model.len
        if model_len <= self.model.points_len:
            # if legacy model definition but it is defined in format that number of groups are known, use that count
            # to avoid having to figure out the length in the model data
            if count == 0 and data_group_count:
                count = data_group_count

        # allocate the group entries if the count is available
        if count > 0:
            for i in range(count):
                gdata = self._group_data(data=data, index=i)
                g = self.group_class(gdef=gdef, model=self.model, model_offset=model_offset, data=gdata,
                                     data_offset=data_offset, index=i+1)
                model_offset += g.len
                data_offset += g.len
                groups.append(g)
        elif count == 0:
            data_group_count = self._get_data_group_count(data=data)
            # legacy model definition - need to calculate repeating count by model length
            # compute count based on model len if present, otherwise allocate when set
            model_len = self.model.len
            if model_len:
                gdata = self._group_data(data=data, name=gdef[mdef.NAME])
                g = self.group_class(gdef=gdef, model=self.model, model_offset=model_offset, data=gdata,
                                     data_offset=data_offset, index=1)
                group_points_len = g.points_len
                # count is model.len-model.points_len/group_points_len
                # (ID and L points are not included in model length)
                repeating_len = model_len - (self.model.points_len - 2)
                if repeating_len > 0:
                    remaining = repeating_len % group_points_len
                    if remaining != 0:
                        raise ModelError('Repeating group count not consistent with model length for model %s,'
                                         'model repeating len = %s, model repeating group len = %s' %
                                         (self.model.model_id, repeating_len, group_points_len))

                    count = int(repeating_len / group_points_len)
                    if count > 0:
                        groups.append(g)
                        model_offset += g.len
                        data_offset += g.len
                    for i in range(count - 1):
                        g = self.group_class(gdef=gdef, model=self.model, model_offset=model_offset, data=data,
                                           data_offset=data_offset, index=i+2)
                        model_offset += g.len
                        data_offset += g.len
                        groups.append(g)
        return groups

    def get_dict(self, computed=False):
        d = {}
        for pid, p in self.points.items():
            d[pid] = p.get_value(computed=computed)
        for gid, group in self.groups.items():
            if isinstance(group, list):
                glist = []
                for g in group:
                    glist.append(g.get_dict(computed=computed))
                d[gid] = glist
            else:
                d[gid] = group.get_dict(computed=computed)
        return d

    def set_dict(self, data=None, computed=False, dirty=None):
        groups = []
        group_def = self.gdef
        for k, v in data.items():
            if k in group_def['point_defs']:
                self.points[k].set_value(data=v, computed=computed, dirty=dirty)
            elif k in group_def['group_defs']:
                # write points first as group initialization may depend on point value for group counts
                groups.append(k)
        for k in groups:
            if isinstance(self.groups[k], list):
                i = 0
                for rg in self.groups[k]:
                    rg.set_dict(data[k][i], computed=computed, dirty=dirty)
                    i += 1
            else:
                self.groups[k].set_dict(data[k], computed=computed, dirty=dirty)

    def get_json(self, computed=False):
        return json.dumps(self.get_dict(computed=computed))

    def set_json(self, data=None, computed=False, dirty=None):
        if data is not None:
            d = json.loads(data)
            self.set_dict(d, computed=computed, dirty=dirty)

    def get_mb(self, computed=False):
        data = bytearray()
        for pid, point in self.points.items():
            data.extend(point.get_mb(computed=computed))
        for gid, group in self.groups.items():
            if isinstance(group, list):
                for g in group:
                    data.extend(g.get_mb(computed=computed))
            else:
                data.extend(group.get_mb(computed=computed))
        return bytes(data)

    def set_mb(self, data=None, computed=False, dirty=None):
        if data:
            data_len = len(data)
        else:
            data_len = 0
        offset = 0
        for pid, point in self.points.items():
            if data_len > offset:
                mb_len = point.set_mb(data[offset:], computed=computed, dirty=dirty)
                if mb_len is not None:
                    offset += mb_len * 2

        for gid, group in self.groups.items():
            if isinstance(group, list):
                for g in group:
                    if data_len > offset:
                        mb_len = g.set_mb(data[offset:], computed=computed, dirty=dirty)
                        if mb_len is not None:
                            offset += mb_len * 2
                        else:
                            return None
            else:
                if data_len > offset:
                    mb_len = group.set_mb(data[offset:], computed=computed, dirty=dirty)
                    if mb_len is not None:
                        offset += mb_len * 2
                    else:
                        return None
        return int(offset/2)


class Model(Group):
    def __init__(self, model_id=None, model_addr=0, model_len=0, model_def=None, data=None, group_class=Group):
        self.model_id = model_id
        self.model_addr = model_addr
        self.model_len = model_len
        self.model_def = model_def
        self.error_info = ''
        self.mid = None
        self.device = None
        self.model = self

        gdef = None
        try:
            if self.model_def is None and model_id is not None:
                self.model_def = get_model_def(model_id)
            if self.model_def is not None:
                gdef = self.model_def.get(mdef.GROUP)
        except Exception as e:
            self.add_error(str(e))

        Group.__init__(self, gdef=gdef, model=self.model, model_offset=0, group_len=self.model_len, data=data,
                       data_offset=0, group_class=group_class)

    def add_error(self, error_info):
        self.error_info = '%s%s\n' % (self.error_info, error_info)

    def get_dict(self, computed=False):
        d = Group.get_dict(self, computed=computed)
        d['mid'] = self.mid
        d['error'] = self.error_info
        d['model_id'] = self.model_id
        return d


class Device(object):
    def __init__(self, model_class=Model):
        self.name = None
        self.did = None
        self.models = {}
        self.model_list = []
        self.model_class = model_class

    def __getattr__(self, attr):
        v = self.models.get(attr)
        if v is None:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, attr))
        return v

    def scan(self, data=None):
        pass

    def add_model(self, model):
        # add by model id
        model_id = model.model_id
        model_list = self.models.get(model_id)
        if model_list is None:
            model_list = []
            self.models[model_id] = model_list
        model_list.append(model)
        # add by group id
        gname = model.gname
        model_list = self.models.get(gname)
        if model_list is None:
            model_list = []
            self.models[gname] = model_list
        model_list.append(model)
        # add to model list
        self.model_list.append(model)

        model.device = self

    def get_dict(self, computed=False):
        d = {'name': self.name, 'did': self.did, 'models': []}
        for m in self.model_list:
            d['models'].append(m.get_dict(computed=computed))
        return d

    def get_json(self, computed=False):
        return json.dumps(self.get_dict(computed=computed))

    def get_mb(self, computed=False):
        data = bytearray()
        for m in self.model_list:
            data.extend(m.get_mb(computed=computed))
        return bytes(data)

    def set_mb(self, data=None, computed=False, dirty=None):
        if data:
            data_len = len(data)
        else:
            data_len = 0
        offset = 0
        for m in self.model_list:
            if data_len > offset:
                mb_len = m.set_mb(data[offset:], dirty=dirty, computed=computed)
                if mb_len is not None:
                    offset += mb_len * 2
                else:
                    return None
        return int(offset/2)

    def find_mid(self, mid=None):
        if mid is not None:
            for m in self.model_list:
                if m.mid == mid:
                    return m

    # assumes data should be used to create and initialize the models, does not currently update an initialized device
    def _set_dict(self, data, computed=False, detail=False):
        if self.model_list:
            raise ModelError('Device already initialized')
        self.name = data.get('name')
        models = data.get('models')
        for m in models:
            if detail:
                model_id = m['ID']['value']
            else:
                model_id = m['ID']
            if model_id != mdef.END_MODEL_ID:
                model_def = model_len = None
                try:
                    model_def = get_model_def(model_id)
                except:
                    model_len = m.get('L')
                if not model_len:
                    model_len = 0
                model = Model(model_def=model_def, data=m, model_id=m['ID'], model_len=model_len)
                self.add_model(model=model)
