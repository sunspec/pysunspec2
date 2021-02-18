pySunSpec2
#########

Overview
========
pySunSpec is a python package that provides objects and applications that support interaction with SunSpec compliant
devices and documents. pySunSpec runs in most environments that support Python and is tested on Windows 7 and
Windows 10.

This is the next generation of pySunSpec tools. It supports all SunSpec infomation model definitions and formats including smdx and
json. The Python objects used for interacting with devices have some differences from version 1 and it is not backward
compatable with version 1. This version of pySunSpec must be used with devices implementing the 7xx series of
information models as they use updated modeling concepts.

Copyright (c) 2020 SunSpec Alliance

Features
========
- Provides access to SunSpec Modbus RTU and TCP devices, and device image files
- High level object model allowing easy device scripting
- Minimal dependencies for core package allowing it to run in more constrained Python environments
- Runs on Windows, and other environments that support Python


Requirements
============
- Python 3.5-3.8
- pySerial (if using Modbus RTU)
- openpyxl (if using Excel spreadsheet)
- pytest (if running tests)

Installation
=================================
Installing from the setup.py file:

 C:\> python setup.py install
 
or if the python path isn't configured:
 
 C:\> c:\\Python37\\python.exe setup.py install
 
Interacting with a SunSpec Device
=================================

The SunSpecModbusClientDeviceRTU, SunSpecModbusClientDeviceTCP, and FileClientDevice classes are used for high level
access to a SunSpec device. These three classes represent the three contexts which you can operate in: RTU, TCP
and device image. The three classes support the same interface, thus operating in the same way in regards to scripting
and functionality. The three classes are wrappers around the Device object, which provides the user with the easiest
syntax for basic operations. Because these context specific objects are a wrapper for the Device object,
functions and patterns are shared across the contexts, but are adapted to their specific context. This means that all
device types have the same device interaction.

The Device object contains Model, Group, and Point objects, all dynamically created from the models in the device.

All of the examples in this guide use commands in the Python command interpreter for illustrative purposes but the
common use case would be to use Python scritps/programs to interact with a SunSpec device.

pySunSpec Objects
-----------------

The Device, Model, Group and Point objects provide the interface for interacting with device instances.

These objects provide a Python representation of the physical device and contain the current values associated with the
points implemented in the device. The point values represent a snapshot of the device at time the point were last
explicitly read from or written to the device. Values are transferred from the physical device to the object when a
read() is performed on an object and from the object to the device when a write is performed. Models, groups, and
points can all be read and written. When models or groups are written, only point values that have been set in the
object since the last read or write are written. A read will overwrite values that have been set and not written.

Device
^^^^^^
The Device object is an interface for different device types, allowing all device types to have the same device
interaction. The three classes which instantiate a device object are: SunSpecModbusClientDeviceRTU,
SunSpecModbusClientDeviceTCP, and FileClientDevice.

Model
^^^^^
A Model object is created for each model found on the device during the model discovery process. The Model object
dynamically creates Point and Group objects based on the model definition and points and groups found in the model.

In the model, group, point hierarchy, a model is a single top-level group. When groups and points are added in the
discovery process they are placed as object attributes using their definition name. This allows the groups and points
to be accessed hierarchically as object attributes allowing an efficient reference syntax.

Group
^^^^^
A Group object represents a group in a model. The object can contain both points and groups. The Group object
dynamically creates Points and Group objects based on points and groups in its group.

Point
^^^^^
The Point object represents a point in a model. There are three key attributes for each point: value, sf_value, and
cvalue.

The value attribute represents the base value for the point. The sf_value attribute represents the scale factor value
for the point, if applicable. The cvalue attribute represents the computed value for the point. The computed value is
created by applying the scale factor value to the base value. Value can be get or set using either their value or
cvalue.

Here are some get examples, where "d"  is the Device object, "DERMeasureAC[0]" is the Model object , and "LLV" is the
Point object.

Get value on point: ::

    >>> d.DERMeasureAC[0].LLV.value
    2403

Get scale factor value on point: ::

    >>> d.DERMeasureAC[0].LLV.sf_value
    -1

Get the computed value on the point, where the scale factor is -1: ::

    >>> d.DERMeasureAC[0].LLV.cvalue
    240.3

And some set examples, where where "d"  is the Device object, "DEREnterService[0]" is the Model object , and "ESVHi" is
the Point object.

Set value on point: ::

    >>> d.DEREnterService[0].ESVHi.value = 2450

Get the point as cvalue: ::

    >>> d.DEREnterService[0].ESVHi.cvalue
    245.0

Set computed value on point, where the computed value is calculated from the scale factor, and the scale factor is
-1: ::

    >>> d.DEREnterService[0].ESVHi.cvalue = 245.1

Get the point as value: ::

    >>> d.DEREnterService[0].ESVHi.value
    2451

Remember, getting and setting the points only updates the Python object and does not read or write the values to the
physical device.

Accessing a SunSpec Device
--------------------------
Accessing with a SunSpec device involves the following steps:

1. Create a device object using one of the device classes (Modbus TCP, Modbus RTU, or Device File).
2. Perform device model discovery using the scan() method on the device.
3. Read and write contents of the device as needed.

Creating a Device Object
------------------------
The following are examples of how to initialize a Device objects using one of the device classes based on the device
type.

TCP
^^^
The following is how to open and initialize a TCP Device, where the slave ID is set to 1, the IP address of the TCP
device is
127.0.0.1, and the port is 8502::

    >>> import sunspec2.modbus.client as client
    >>> d = client.SunSpecModbusClientDeviceTCP(slave_id=1, ipaddr='127.0.0.1', ipport=8502)

RTU
^^^
The following to open and initialize a RTU Device, where the slave ID is set to 1, and the name of the serial port is
COM2::

    >>> import sunspec2.modbus.client as client
    >>> d = client.SunSpecModbusClientDeviceRTU(slave_id=1, name="COM2")

Device Image
^^^^^^^^^^^^
The following is how to open a Device Image file named "model_702_data.json"::

    >>> import sunspec2.file.client as client
    >>> d = client.FileClientDevice('model_702_data.json')

Closing a device
----------------
When done with a device, close it:

    >>> d.close()

Device Model Discovery
----------------------
The scan() method must be called after initialization of the device. Scan invokes the device model discovery
process. For different device types, scan may or may not be necessary, but it can be called on any device type.
Depending on the type, scan may either go through the device Modbus map, or it may go through the device image file.
For Modbus, scan searches three device addresses (0, 40000, 50000), looking for the 'SunS' identifier. Upon discovery
of the SunS identifier, scan uses the model ID and model length to find each model present in the device. Model
definitions are used during the discovery process to create the Model, Group, and Points objects associated with the
model. If a model is encountered that does not have a model definition, it is noted but its contents are not interpreted.
The scan is performed until the end model is encountered.

The scan produces a dictionary containing entries for each model ID found. Two dictionary keys are created for each
model ID. The first key is the model ID as an int, the second key is the model name as a string. Since it is possible
that a device may contain more than one model with the same model ID, the dictionary keys refer to a list of model
objects with that ID. Both keys refer to the same model list for a model ID.

    >>> d = client.SunSpecModbusClientDeviceTCP(slave_id=1, ipaddr='127.0.0.1', ipport=8502)
    >>> d.scan()


Determine which models are present in the device: ::

    >>> d.models
    {1: [<__main__.SunSpecModbusClientModel object at 0x000001FD7A6082B0>],
     'common': [<__main__.SunSpecModbusClientModel object at 0x000001FD7A6082B0>],
     705: [<__main__.SunSpecModbusClientModel object at 0x000001FD7A8B28B0>],
     'DERVoltVar': [<__main__.SunSpecModbusClientModel object at 0x000001FD7A8B28B0>]}

Models are stored in a dictionary using the key for the model ID, and the model name. In this case, the device has two
models: common (model 1), DERVoltVar (model 705).

Reading from a Device
---------------------
To acquire the values from the physical device, an explicit read operation must be performed with the read() method
on a device, model, group, or point within the device.

To perform a read() for the common model contents: ::

    >>> d.common[0].read()

The model, group, and point objects, in the common model, have been updated to the latest values on the device.

Writing to a Device
-------------------
To update the physical device with values that have been set in the device, an explict write() operation must be done on
a device, model, group, or point. Only the fields that have been set since the last read or write in the model are
actually written to the physical device.

Get the value on the point "Ena" in the "DERVoltVar" model: ::

    >>> d.DERVoltVar[0].Ena.value
    0

Set the value for the point and write to the device: ::

    >>> d.DERVoltVar[0].Ena.value = 1
    >>> d.DERVoltVar[0].write()
    >>> d.DERVoltVar[0].read()

Get the value on the point "Ena" in the "DERVoltVar" model: ::

    >>> print(d.DERVoltVar[0].Ena.value)
    1

After assigning the value on the point object, "Ena", write() must be called in order to update the device. Many
consider it a good Modbus practice to read after every write to check if the operation was successful, but it is not
required. In this example, we perform a read() after a write().

Additional Information
----------------------
The groups and points in a group are contained in ordered groups and points dictionaries if needed. Repeating groups are
represented as a list of groups.

Get the groups present in the model 705 on the device: ::

    >>> d.DERVoltVar[0].groups
    OrderedDict([('Crv', [<__main__.SunSpecModbusClientGroup object at 0x000001FD7A58EFA0>,
                          <__main__.SunSpecModbusClientGroup object at 0x000001FD7A58EF40>,
                          <__main__.SunSpecModbusClientGroup object at 0x000001FD7A58EEE0>])])

Get the points present in the model 705 on the device: ::

    >>> d.DERVoltVar[0].points
    OrderedDict([('ID', <__main__.SunSpecModbusClientPoint object at 0x000001FD7A59C2E0>),
                 ('L', <__main__.SunSpecModbusClientPoint object at 0x000001FD7A59C2B0>),
                 ('Ena', <__main__.SunSpecModbusClientPoint object at 0x000001FD7A59C280>),
                 ('CrvSt', <__main__.SunSpecModbusClientPoint object at 0x000001FD7A59C250>),
                 ('AdptCrvReq', <__main__.SunSpecModbusClientPoint object at 0x000001FD7A59C220>),
                 ('AdptCrvRslt', <__main__.SunSpecModbusClientPoint object at 0x000001FD7A59C0A0>),
                 ('NPt', <__main__.SunSpecModbusClientPoint object at 0x000001FD7A59C0D0>),
                 ('NCrv', <__main__.SunSpecModbusClientPoint object at 0x000001FD7A59C100>),
                 ('RvrtTms', <__main__.SunSpecModbusClientPoint object at 0x000001FD7A59C130>),
                 ('RvrtRem', <__main__.SunSpecModbusClientPoint object at 0x000001FD7A59C160>),
                 ('RvrtCrv', <__main__.SunSpecModbusClientPoint object at 0x000001FD7A59C190>),
                 ('V_SF', <__main__.SunSpecModbusClientPoint object at 0x000001FD7A59C1C0>),
                 ('DeptRef_SF', <__main__.SunSpecModbusClientPoint object at 0x000001FD7A59C1F0>)])

Full Example of a Device Interaction
------------------------------------
This section will go over the full steps on how to set a volt-var curve.

Initialize device, and run device discovery with scan(): ::

    >>> d = client.SunSpecModbusClientDeviceRTU(slave_id=1, name="COM2")
    >>> d.scan()

Confirm that model 705 (DERVoltVar) is on the device: ::

    >>> d.models
    {1: [<__main__.SunSpecModbusClientModel object at 0x000001FD7A6082B0>],
     'common': [<__main__.SunSpecModbusClientModel object at 0x000001FD7A6082B0>],
     705: [<__main__.SunSpecModbusClientModel object at 0x000001FD7A8B28B0>],
     'DERVoltVar': [<__main__.SunSpecModbusClientModel object at 0x000001FD7A8B28B0>]}

Read the volt-var model from the device to ensure the latest values:

    >>> vv = d.DERVoltVar[0]
    >>> vv.read()

Display the current curve values (the first curve). Curve 1 is a read-only curve indicating the current curve settings:

    >>> print(vv.Crv[0])
    Crv(1):
      ActPt:  4
      DeptRef:  1
      Pri:  1
      VRef:  100
      VRefAuto:  0
      VRefAutoEna:  None
      VRefTms:  5
      RspTms:  0
      ReadOnly:  1
      Pt(1):
        V:  9200
        Var:  3000
      Pt(2):
        V:  9670
        Var:  0
      Pt(3):
        V:  10300
        Var:  0
      Pt(4):
        V:  10700
        Var:  -3000

Note that, by convention, SunSpec repeating elements, such as curves, are labeled with an index of 1 for the first
element, but when accessing in the Python objects, the index of the first element is 0. Here we see the first curve
being accessed with the 0 index but labeled as curve 1 in the output. Parentheses are used with the index of 1 to
indicate it is a SunSpec 1-based index.

Use the second curve to hold the new curve settings and write to the device:

    >>> c = vv.Crv[1]
    >>> c.ActPt = 4
    >>> c.DeptRef = 1
    >>> c.VRef = 100
    >>> c.VRefAutoEna = 0
    >>> c.Pt[0].V = 9300
    >>> c.Pt[0].Var = 2000
    >>> c.Pt[1].V = 9700
    >>> c.Pt[1].Var = 0
    >>> c.Pt[2].V = 10350
    >>> c.Pt[2].Var = 0
    >>> c.Pt[3].V = 10680
    >>> c.Pt[3].Var = -2000
    >>> c.write()

Write point adopt curve request point to adopt the curve 2 values:

    >>> vv.AdptCrvReq = 2
    >>> vv.write()

Read the adopt curve result and contents of the curves:

    >>> vv.read()
    >>> print(vv.AdptCrvRslt)
    1

The result indicates completed. The first curve should now contain the updated values reflecting the current active curve settings:

    >>> print(vv.Crv[0])
    Crv(1):
      ActPt:  4
      DeptRef:  1
      Pri:  1
      VRef:  100
      VRefAuto:  0
      VRefAutoEna:  None
      VRefTms:  5
      RspTms:  0
      ReadOnly:  1
      Pt(1):
        V:  9300
        Var:  2000
      Pt(2):
        V:  9700
        Var:  0
      Pt(3):
        V:  10350
        Var:  0
      Pt(4):
        V:  10680
        Var:  -2000

Check to see if the function is enabled by checking the Ena point. ::

    >>> print(vv.Ena.value)
    0

The function is disabled, set the value to 1, and write to device, in order to enable the function. ::

    >>> vv.Ena.value = 1
    >>> d.write()

It is considered a best practice with Modbus to verify values written to the device by reading them back to ensure they
were set properly. That step has been omitted to here to focus on the update sequence.

Contribution
============
If you wish to contribute to the project, please contact support@sunspec.org to sign a CLA.
