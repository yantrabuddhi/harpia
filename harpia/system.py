# -*- coding: utf-8 -*-
"""
This module contains the System class.
"""
import os
import sys
import copy
import inspect  # For module inspect
import pkgutil  # For dynamic package load
import harpia.extensions
from glob import glob  # To load examples
from harpia.control.preferencescontrol import PreferencesControl
from harpia.control.portcontrol import PortControl
from harpia.control.plugincontrol import PluginControl
from harpia.control.codetemplatecontrol import CodeTemplateControl
from harpia.model.preferences import Preferences
from harpia.model.codetemplate import CodeTemplate
from harpia.model.plugin import Plugin
from harpia.model.port import Port


class System(object):
    """
    This class contains methods related the System class.
    """

    APP = 'harpia'
    DATA_DIR = "/usr/share/harpia/"

    ZOOM_ORIGINAL = 1
    ZOOM_IN = 2
    ZOOM_OUT = 3

    VERSION = "0.0.1"
    # Instance variable to the singleton
    instance = None

    # ----------------------------------------------------------------------
    # An inner class instance to be singleton
    # ----------------------------------------------------------------------
    class __Singleton:
        # ----------------------------------------------------------------------

        def __init__(self):
            self.Log = None
            self.properties = Preferences()
            self.code_templates = {}
            self.plugins = {}
            self.list_of_examples = []
            self.ports = {}
            self.__load()

        # ----------------------------------------------------------------------
        def __load_xml(self, data_dir):
            if not os.path.exists(data_dir):
                return
            for file_name in os.listdir(data_dir):
                full_file_path = data_dir + "/" + file_name

                # Recursion to make it more interesting...
                if os.path.isdir(full_file_path):
                    self.__load_xml(full_file_path)

                if not file_name.endswith(".xml"):
                    continue

                code_template = CodeTemplateControl.load(full_file_path)
                if code_template is not None:
                    code_template.source = "xml"
                    self.code_templates[code_template.type] = code_template

                port = PortControl.load(full_file_path)
                if port is not None:
                    port.source = "xml"
                    self.ports[port.type] = port

                plugin = PluginControl.load(full_file_path)
                if plugin is not None:
                    plugin.source = "xml"
                    self.plugins[plugin.type] = plugin

        # ----------------------------------------------------------------------
        def __load(self):
            # Create user directory if does not exist
            if not os.path.isdir(System.get_user_dir() + "/extensions/"):
                try:
                    os.makedirs(System.get_user_dir() + "/extensions/")
                except:
                    pass
            # Load the preferences
            self.properties = PreferencesControl.load()
            # Load Examples
            examples = glob(System.DATA_DIR + "examples/*")
            for example in examples:
                self.list_of_examples.append(example)
            self.list_of_examples.sort()

            # Load CodeTemplates, Plugins and Ports
            self.code_templates.clear()
            self.ports.clear()
            self.plugins.clear()
            # First load ports on python classes.
            # They are installed with harpia as root 
            for importer, modname, ispkg in pkgutil.walk_packages(
                    harpia.extensions.__path__,
                    harpia.extensions.__name__ + ".",
                    None):
                if ispkg:
                    continue
                module = __import__(modname, fromlist="dummy")
                for name, obj in inspect.getmembers(module):
                    if not inspect.isclass(obj):
                        continue
                    modname = inspect.getmodule(obj).__name__
                    if not modname.startswith("harpia.extensions"):
                        continue
                    instance = obj()
                    if isinstance(instance, CodeTemplate):
                        self.code_templates[instance.type] = instance
                    if isinstance(instance, Port):
                        instance.source = "Python"
                        self.ports[instance.type] = instance
                    if isinstance(instance, Plugin):
                        if instance.label != "":
                            self.plugins[instance.type] = instance

            # Load XML files in application space
            self.__load_xml(System.DATA_DIR + "extensions/")
            # Load XML files in user space
            self.__load_xml(System.get_user_dir() + "/extensions/")

    # ----------------------------------------------------------------------
    def __init__(self):
        if not System.instance:
            System.instance = System.__Singleton()

    # ----------------------------------------------------------------------
    def __new__(cls):  # __new__ always a classmethod
        if System.instance is None:
            System.instance = System.__Singleton()
            # Add properties dynamically
            cls.properties = System.instance.properties
            cls.plugins = System.instance.plugins
            cls.list_of_examples = System.instance.list_of_examples
            cls.ports = System.instance.ports
            cls.code_templates = System.instance.code_templates

    # ----------------------------------------------------------------------
    @classmethod
    def set_log(cls, Logger):
        """
        This method set the log.
        """
        try:
            cls.instance.Log = Logger
        except:
            print "Could not set logger"

    # ----------------------------------------------------------------------
    @classmethod
    def log(cls, msg):
        "This metho show the log."
        try:
            cls.instance.Log.log(msg)
        except:
            print msg

    # ----------------------------------------------------------------------
    @classmethod
    def get_user_dir(cls):
        home_dir = os.path.expanduser("~")
        home_dir = home_dir + "/" + System.APP
        return home_dir

# ------------------------------------------------------------------------------
