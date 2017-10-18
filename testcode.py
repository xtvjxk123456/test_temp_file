#coding:utf-8

import os
import sys
import maya.cmds as mc


filepath ='fsfsdfs'
test='fsfsfs'

hh= os.path.join(filepath,test)

tt =os.path.normpath(hh)
print tt
