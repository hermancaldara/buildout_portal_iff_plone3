# -*- coding: UTF-8 -*-
"""
transform .xls file to HTML
uses xlhtml
"""
import re, tempfile
import os, os.path
from os.path import join as pjoin
from transform_libs.double_encoded import noDoubleEncoding
from Products.PortalTransforms.libtransforms.utils import bin_search, \
     sansext, bodyfinder, scrubHTML
from Products.PortalTransforms.libtransforms.commandtransform import commandtransform

#some binary transforms add a signature arbitrary encoded in non utf-8 charset... 
#Therefore process_double_encoding returns pure utf-8 result.
process_double_encoding = True

mimecmdmap = {
    'text/plain': "xlhtml",
    'text/html': "xlhtml",
}

mimeextmap = {
    'text/plain': "txt",
    'text/html': "html",
}

class document(commandtransform):

    def __init__(self, name, data, outmime):
        """ Initialization: create tmp work directory and copy the
        document into a file"""
        self.outmime=outmime
        commandtransform.__init__(self, name, binary=mimecmdmap[outmime])
        name = self.name()
        if not name.endswith('.xls'):
            name = name + ".xls"
        self.tmpdir, self.fullname = self.initialize_tmpdir(data, filename=name)

    def convert(self):
        "Convert the document"
        tmpdir = self.tmpdir

        print 'cd "%s" && %s "%s" > "%s.%s"' % (tmpdir, self.binary,
                                                             self.fullname,
                                                             self.__name__,
                                                             mimeextmap[self.outmime],)

        if os.name == 'posix':
            os.system('cd "%s" && %s "%s" > "%s.%s"' % (tmpdir, self.binary,
                                                             self.fullname,
                                                             self.__name__,
                                                             mimeextmap[self.outmime],))

    def _html(self):
        try:
            htmlfile = open(pjoin(self.tmpdir, self.__name__+".html"), 'r')
            html = htmlfile.read()
        except IOError:
            return ""
        if process_double_encoding :
            html = noDoubleEncoding(html)
        htmlfile.close()
        #xlhtml gives verry complex html ; scrubHTML takes soooo long !
        #html = scrubHTML(html)
        body = bodyfinder(html)
        return body
    
    def _text(self):
        try:
            txtfile = open(pjoin(self.tmpdir, self.__name__+".txt"), 'r')
            text = txtfile.read()
        except IOError:
            return ""
        txtfile.close()
        return text
    
    def getconverted(self):
        mimeoutmap= {
            'text/plain': self._text,
            'text/html':  self._html,
        }
        return mimeoutmap[self.outmime]()
