#!/usr/bin/env python
import os, re, sys
from PIL import Image


SCRIPT_PATH =  os.path.dirname(os.path.realpath(__file__)) + "/"
IMAGE_FILE_REGEX = '^.+\.(png|jpg|jpeg|tif|tiff|gif|bmp)$'
THUMBNAIL_WIDTH = 120

base_path = sys.argv[1]

image_files = list()

for root, dirs, files in os.walk(base_path):
  for image in files:
    if re.match(IMAGE_FILE_REGEX, image): 
      try:
        im = Image.open(os.path.join(root,image))
        image_files.append([os.path.join(root,image),im.size])
      except:
        continue
if ( len(image_files) < 1 ):
	print "No images found"
	sys.exit(1)
for image in image_files:
  print os.path.basename(image[0]), " - ", str(image[1][0]) + 'x' + str(image[1][1])


html = [
    '<html>',
    '<head>',
    ' <style type="text/css">',
    '   .container img {',
    '      margin-bottom: 10px;',
    '    }',
    '  </style>',
    '</head>',
    '<body>',
    ' <div class="container">',
    '   <div class="col-md-10 col-lg-8 col-md-offset-1 col-lg-offset-2">',
    '     <div id="container">'
    ]

for image in image_files:
  ratio = THUMBNAIL_WIDTH / float(image[1][0])
  height = int(ratio * image[1][1])
  html.append('       <a href="file:///'+image[0]+'" target="_blank"><img class="lazy" data-original="file:///'+image[0]+'" width="'+str(THUMBNAIL_WIDTH)+'" height="'+str(height)+'"></a>')

html.extend(
    [
    '     </div>',
    '   </div>',
    ' </div>',
    ' <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>',
    ' <script src="'+SCRIPT_PATH+'jquery.lazyload.js?v=1.9.1"></script>',
    ' <script src="'+SCRIPT_PATH+'jquery.scrollstop.js"></script>',
    ' <script src="'+SCRIPT_PATH+'all.js"></script>',
    ' <script type="text/javascript">',
    '   $(function() {',
    '     $("img.lazy").lazyload({',
    '       event: "scrollstop"',
    '     });',
    '   });',
    ' </script>',
    '</body>',
    '</html>'
    ])

#print "\n".join(html)

index_file = open(SCRIPT_PATH+"index.html", 'w')
index_file.write('\n'.join(html))
index_file.close

print "file:///"+SCRIPT_PATH+"index.html"
