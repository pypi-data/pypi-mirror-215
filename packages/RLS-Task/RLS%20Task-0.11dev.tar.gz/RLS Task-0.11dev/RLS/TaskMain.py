import requests
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication
import sys

# Send a GET request to the XML file URL
url = 'http://agromet.mkgp.gov.si/APP2/AgrometContent/xml/55.xml'
response = requests.get(url)
# TEMPS tavg = avg temp.; tx = max temp; tn = min temp.
# HUMIDITY rhavg, rhx, rhn
#  
 
if response.status_code == 200: # Check if the request was successful
    root = ET.fromstring(response.content) # Parse the XML content

    # Extract temperature data from the XML
    temperatures = []
    entries = 10
    for element in root.iter('tavg'):
        temperatures.append(float(element.text))
        #if len(temperatures) >= entries: # Limiting entries for testing
        #    break
        if root.iter("/data"):
            break
    
    
        print(temperatures)

    # Create the graph using matplotlib
    plt.plot(temperatures)
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Variation')
    plt.show()

    # Start the PyQt5 event loop
    app = QApplication([])
    app.exec_()
    sys.exit(app.exec())
else:
    print(f'Request failed with status code: {response.status_code}')