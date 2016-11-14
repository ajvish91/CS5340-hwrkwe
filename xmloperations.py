import PIL.Image
import xml.etree.ElementTree as ET


def machinePrintedPart(filepath):
    # Captures the jpeg file and extracts METADATA
    jpgfile = PIL.Image.open(filepath)
    print filepath
    # The METADATA is an XML, hence parsing
    myxml = ET.fromstring(jpgfile.info["Description"])

    # print jpgfile.info["Description"]

    # Gets the text corresponding to the file a01-000u-s00-00.png
    machine_printed_part = myxml.find("machine-printed-part")
    lines = ""
    for parts in machine_printed_part:
        lines = lines + parts.attrib["text"] + " "
    print len(lines)
    return lines
