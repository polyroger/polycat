At the moment we are using a maya module to configure the maya start up.
Modules are basically just virtual re recreations the maya users start up. A module is the file structure that makes up the paths maya is looking for
the .mod file location has to be referenced by your maya.env under the " MAYA_MODULE_PATH "
the .mod file then references the name of the module and its location. Best parctice is to have the env location and the module locaction the same