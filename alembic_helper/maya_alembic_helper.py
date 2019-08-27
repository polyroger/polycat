import maya.cmds as cmds
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.realpath(sys.argv[0])))).replace(os.sep, "/"))
from pc_utilities import pc_helper


BASE_ATTRIBUTES = [
    "-frameRange",
    "-dataFormat ogawa"
]


class Helper:
    def __init__(self):
        self.check_alembic_plugin()
        self._node = None
        self._output = None
        self._command = self.__create_default_command()

    @property
    def set_alembic_node(self, node):
        self._node = node

    @property
    def get_alembic_node(self):
        return self._node

    @property
    def set_alembic_output(self, output):
        self._output = output

    @property
    def get_alembic_output(self):
        return self._output

    @property
    def set_alembic_command(self, commands):
        self._command = self.__create_default_command(extra_attributes=commands)

    @property
    def get_alembic_command(self):
        return self._command


    def export_alembic(self):
        ["-root {}".format(str(self._node)),"-file {}".format(self._output)]
        if os.path.exists(os.path.dirname(self._output)):
            cmds.AbcExport(j=self._command)

    def __create_default_command(self, extra_attributes=None):
        attrs = BASE_ATTRIBUTES
        if extra_attributes is not None:
            attrs = attrs + extra_attributes
        attrs = attrs + self.__get_write_attributes()
        return " ".join(attrs)
    
    def __get_write_attributes(self):
        return ["-root {}".format(self._node),"-file {}".format(self._output)]

    @classmethod
    def check_alembic_plugin(cls):
        if cmds.pluginInfo('AbcExport.so', query=True, loaded=True) is False:
            cmds.loadPlugin("AbcExport.so")
        if cmds.pluginInfo('AbcImport.so', query=True, loaded=True) is False:
            cmds.loadPlugin("AbcImport.so")
