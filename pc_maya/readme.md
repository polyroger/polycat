At the moment we are using a maya module to configure the maya start up.
Modules are basically just virtual re recreations the maya users start up. A module is the file structure that makes up the paths maya is looking for
the .mod file location has to be referenced by your maya.env under the " MAYA_MODULE_PATH "
the .mod file then references the name of the module and its location, can be relative to itsself. Using a env variable to set the path seemed to break the creation of other variables in the file.

=               -creates a new variable
PATH:=menus     -the absolute path of the folder "menus" in the MAYA_MOUDULE_PATH

there is more syntax like this....google maya module and you will find it