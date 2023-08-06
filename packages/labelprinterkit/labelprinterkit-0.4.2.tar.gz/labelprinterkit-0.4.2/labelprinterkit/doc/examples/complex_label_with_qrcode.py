# This example creates a more complex label with a QR Code and two text lines.
#
# The label will look like this sketch:
#
# +-------+------------------+
# |  QR   | Text 1           |
# | Code  +------------------+
# |       | Text 2           |
# +-------+------------------+
#

# First let's import all the needed Classes

from labelprinterkit.backends.network import TCPBackend
from labelprinterkit.printers import P750W
from labelprinterkit.label import Label, Box, Text, QrCode, Padding
from labelprinterkit.job import Job
from labelprinterkit.constants import MediaType, MediaSize
from labelprinterkit.page import Page
from PIL import Image

# The label will be created for a 12mm band. The 12mm has 70 pixel/points width.
# So let's create a QR code with 70 pixels width.
qrcode = QrCode(70, "https://pypi.org/project/labelprinterkit/")

# Create text for the label
# The upper text is 25 pixels height and the lower text is 45 pixels height.
# Both together have the 70 points width of the label.
# The lower label gets 1 pixel padding on the top for some spacing.
# If the font_size is not given, the font_size is calculated automatically to fit in the width
text1 = Text("This label is proudly presented by", 25, 'comic.ttf')
text2 = Text("labelprinterkit", 45, 'comic.ttf', padding=Padding(0, 1, 0, 0))

# Insert Text into boxes
box = Box(70, text1, text2, vertical=True)

# Create label with rows from above
label = Label(qrcode, box)

# Create job with configuration and add label as page
job = Job(MediaSize.W12, MediaType.LAMINATED_TAPE)
job.add_page(label)

# Create a page from a Pillow image and add it to the job
image = Image.new("1", (70, 200), "white")
page = Page.from_image(image)
job.add_page(page)

# Use TCP backend to connect to printer
backend = TCPBackend('labelprinter-1.net.scc.kit.edu')
printer = P750W(backend)

# Print job
printer.print(job)
