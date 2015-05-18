__author__ = 'sorkhei'

# Setting the classpath to tika-app.jar in order to access java classes
import os
os.environ['CLASSPATH'] = '/Users/sorkhei/Downloads/tika.jar'

# Using jnius in order to access  java libraries within python
from jnius import autoclass, cast



Tika = autoclass('org.apache.tika.Tika')
Metadata = autoclass('org.apache.tika.metadata.Metadata')
FileInputStream = autoclass('java.io.FileInputStream')

#   PDFParser = autoclass('org.apache.tika.parser.pdf.PDFParser')
#   ParseContext = autoclass('org.apache.tika.parser.ParseContext')
#   BodyContentHandler = autoclass('org.apache.tika.sax.BodyContentHandler')
#   ContentHandler = autoclass('org.xml.sax.ContentHandler')
#   InputStream = autoclass('java.io.InputStream')


tika = Tika()
meta = Metadata()
text = tika.parseToString(FileInputStream('test.pdf'), meta)



