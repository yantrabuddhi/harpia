#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class LiveDelay(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__
        self.frameNumber = 5

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Inserts a delay inside a live stream"
    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        self.frameNumber = int(round(float(self.frameNumber)))
        blockTemplate.imagesIO = 'IplImage * block$id$_img_i1 = NULL;\n' + \
                                 'IplImage * block$id$_img_o1 = NULL;\n' + \
                                 'int i_$id$ = 0;\n' + \
                                 'IplImage * block$id$_buffer[' + str(self.frameNumber) + '] = {'
        for idx in range(self.frameNumber):
            blockTemplate.imagesIO += 'NULL'
            if idx != self.frameNumber - 1:
                blockTemplate.imagesIO += ','
        blockTemplate.imagesIO += '};\n'

        for idx in range(self.frameNumber):
            blockTemplate.imagesIO += 'block$id$_buffer[' + str(
                idx) + '] = cvCreateImage( cvSize(640,480), 8, 3);\n'
            blockTemplate.imagesIO += 'cvSetZero(block$id$_buffer[' + str(idx) + ']);\n'

        blockTemplate.imagesIO += 'block$id$_img_o1 = block$id$_buffer[' + str(self.frameNumber - 1) + '];\n'

        blockTemplate.functionCall = '''
if(block$id$_img_i1){
    cvReleaseImage(&(block$id$_buffer[i_$id$]));
    block$id$_buffer[i_$id$] = cvCloneImage(block$id$_img_i1);
    i_$id$++;
    i_$id$ %= $frameNumber$;
    block$id$_img_o1 = block$id$_buffer[i_$id$];
}
'''

        blockTemplate.dealloc = 'cvReleaseImage(&block$id$_img_i1);\n'
        blockTemplate.outDealloc = '''
for(i_$id$=0; i_$id$<$frameNumber$; i_$id$++)
    if(block$id$_buffer[i_$id$] != NULL)
        cvReleaseImage(&(block$id$_buffer[i_$id$]));
'''

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            'Label': _('Live Delay'),
            'Icon': 'images/liveDelay.png',
            'Color': '250:20:30:150',
            'InTypes': {0: 'HRP_IMAGE'},
            'OutTypes': {0: 'HRP_IMAGE'},
            'Description': _('Inserts a delay inside a live stream'),
            'TreeGroup': _('General'),
            'TimeShifts': True
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
            "frameNumber":{"name": "Time (in frames)",
                        "type": HARPIA_INT,
                        "value": self.frameNumber,
                        "lower":1,
                        "upper":200,
                        "step":1
                        }
        }

# ------------------------------------------------------------------------------
