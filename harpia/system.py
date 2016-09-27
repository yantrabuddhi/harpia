# -*- coding: utf-8 -*-
# [HARPIA PROJECT]
#
#
# S2i - Intelligent Industrial Systems
# DAS - Automation and Systems Department
# UFSC - Federal University of Santa Catarina
# Copyright: 2006 - 2007 Luis Carlos Dill Junges (lcdjunges@yahoo.com.br),
#                        Clovis Peruchi Scotti (scotti@ieee.org),
#                        Guilherme Augusto Rutzen (rutzen@das.ufsc.br), 
#                        Mathias Erdtmann (erdtmann@gmail.com)
#                        and S2i (www.s2i.das.ufsc.br)
#            2007 - 2009 Clovis Peruchi Scotti (scotti@ieee.org),
#                        S2i (www.s2i.das.ufsc.br)
#
#
#    This program is free software: you can redistribute it and/or modify it
#    under the terms of the GNU General Public License version 3, as published
#    by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranties of
#    MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
#    PURPOSE.  See the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    For further information, check the COPYING file distributed with this software.
#
#----------------------------------------------------------------------

import harpia.plugins
from harpia.control.preferencescontrol import PreferencesControl
from harpia.model.preferences import Preferences

import pkgutil # For dynamic package load
import inspect # For module inspect

from glob import glob # To load examples
import os
import copy

import sys

class System(object):

    APP='harpia'
    DIR='/usr/share/harpia/po'

    ZOOM_ORIGINAL = 1
    ZOOM_IN = 2
    ZOOM_OUT = 3

    VERSION = "0.0.1"

    # ----------------------------------------------------------------------
    # An inner class instance to be singleton
    # ----------------------------------------------------------------------
    class __Singleton:
        # ----------------------------------------------------------------------
        def __init__(self):
            self.Log = None
            self.properties = Preferences()
            self.blocks = {}
            self.list_of_examples = []
            self.connections = {}
            self.__load()

        # ----------------------------------------------------------------------
        def __load(self):
            self.__load_blocks()
            self.__load_connections()
            examples = glob(os.environ['HARPIA_DATA_DIR'] + "examples/*")
            for example in examples:
                self.list_of_examples.append(example)
            self.list_of_examples.sort()
            PreferencesControl(self.properties).load()


        # ----------------------------------------------------------------------
        def __load_blocks(self):
            for importer, modname, ispkg in pkgutil.walk_packages(
                            harpia.plugins.__path__,
                            harpia.plugins.__name__ + ".",
                            None):
                if ispkg:
                    continue
                module = __import__(modname, fromlist="dummy")
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and "Label" in obj().get_description():
                        obj_type = obj().type
                        language = obj_type.split(".")[2]
                        framework = obj_type.split(".")[3]
                        # Adding a property do class dinamically
                        obj.language = language 
                        obj.framework = framework
                        self.blocks[obj_type] = obj

        # ----------------------------------------------------------------------
        def __load_connections(self):
            self.connections = {        "HRP_INT":{
            "icon_in":"images/conn_int_in.png",
            "icon_out":"images/conn_int_out.png",
            "multiple": False,
            "code": 'block$to_block$_int_i$to_block_in$ = block$from_block$_int_o$from_block_out$;// INT conection\n'
            },
        "HRP_DOUBLE":{
            "icon_in":"images/conn_double_in.png",
            "icon_out":"images/conn_double_out.png",
            "multiple": False,
            "code": 'block$to_block$_double_i$to_block_in$ = block$from_block$_double_o$from_block_out$;// DOUBLE conection\n'
            },
        "HRP_RECT":{
            "icon_in":"images/conn_rect_in.png",
            "icon_out":"images/conn_rect_out.png",
            "multiple": False,
            "code": 'block$to_block$_rect_i$to_block_in$ = block$from_block$_rect_o$from_block_out$;// RECT conection\n'
            },
        "HRP_IMAGE":{
            "icon_in":"images/conn_image_in.png",
            "icon_out":"images/conn_image_out.png",
            "multiple": False,
            "code": 'block$to_block$_img_i$to_block_in$ = cvCloneImage(block$from_block$_img_o$from_block_out$);// IMG conection\n'
            },
        "HRP_POINT":{
            "icon_in":"images/conn_point_in.png",
            "icon_out":"images/conn_point_out.png",
            "multiple": False,
            "code": 'block$to_block$_point_i$to_block_in$ = block$from_block$_point_o$from_block_out$;// POINT conection\n'
            },

        "HRP_WEBAUDIO_SOUND":{
            "icon_in":"images/conn_sound_in.png",
            "icon_out":"images/conn_sound_out.png",
            "multiple": True,
            "code": 'block_$from_block$.connect(block_$to_block$_i[$to_block_in$]);\n'
            },
        "HRP_WEBAUDIO_FLOAT":{
            "icon_in":"images/conn_float_in.png",
            "icon_out":"images/conn_float_out.png",
            "multiple": True,
            "code": 'block_$from_block$_o$from_block_out$.push(block_$to_block$_i[$to_block_in$]);\n'
            },
        "HRP_WEBAUDIO_CHAR":{
            "icon_in":"images/conn_char_in.png",
            "icon_out":"images/conn_char_out.png",
            "multiple": True,
            "code": 'block_$from_block$_o$from_block_out$.push(block_$to_block$_i[$to_block_in$]);\n'
            }
        }

    # Instance variable to the singleton
    instance = None

    # ----------------------------------------------------------------------
    def __init__(self):
        if not System.instance:
            System.instance = System.__Singleton()

    def __new__(cls): # __new__ always a classmethod
        if System.instance == None:
            System.instance = System.__Singleton()
            #Add properties dynamically
            cls.properties = System.instance.properties
            cls.blocks = System.instance.blocks
            cls.list_of_examples = System.instance.list_of_examples
            cls.connections = System.instance.connections

    # ----------------------------------------------------------------------
    @classmethod
    def set_log(cls, Logger):
        try:
            cls.instance.Log = Logger
        except:
            print "Could not set logger"

    # ----------------------------------------------------------------------
    @classmethod
    def log(cls, msg):
        try:
            cls.instance.Log.log(msg)
        except:
            print msg
# ------------------------------------------------------------------------------