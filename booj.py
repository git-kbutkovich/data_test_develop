### download these libraries if pip install requirements.txt does not work
"""
import xml.etree.ElementTree as ET
import pandas as pd
import csv
"""


## Step 1:  Downlading and parsing XML file with ETree

### step 2: parse XML and get root
#using a flat file instead of Web page. Could not get the URL to work
url = 'BoojCodeTest.xml'
tree = ET.parse(url)
root = tree.getroot()

### step 3 : create and open CSV
xml_data_to_csv = open('output.csv', 'w')

### step 4 : create list to contain header
list_head = []

### step 5 : create variable to write to csv
csv_writer = csv.writer(xml_data_to_csv)

### step 6 : loop for each node
count = 0
for element in root.findall('Listing'):
    List_nodes = []

    #Get head by tag
    if count == 0:

        for location in element.findall('Location'):
            StreetAddress = location.find('StreetAddress').tag
            list_head.append(StreetAddress)



        for listingdetail in element.findall('ListingDetails'):

            MlsId = listingdetail.find('MlsId').tag
            list_head.append(MlsId)

            MlsName = listingdetail.find('MlsName').tag
            list_head.append(MlsName)

            DateListed = listingdetail.find('DateListed').tag
            list_head.append(DateListed)

            Price  = listingdetail.find('Price').tag
            list_head.append(Price)



        for basicdetail in element.findall('BasicDetails'):

            Description = basicdetail.find('Description').tag
            list_head.append(Description)

            Bedrooms  = basicdetail.find('Bedrooms').tag
            list_head.append(Bedrooms)

            Bathrooms  = basicdetail.find('FullBathrooms').tag
            list_head.append(Bathrooms)


        for richdetail in element.findall('RichDetails'):

            Appliances  = richdetail.find('Appliances').tag
            list_head.append(Appliances)

            Rooms = richdetail.find('RoomCount').tag
            list_head.append(Rooms)


        csv_writer.writerow(list_head)
        count += 1

    #get child node
    for location in element.findall('Location'):

        StreetAddress = location.find('StreetAddress').text
        List_nodes.append(StreetAddress)



    for listingdetail in element.findall('ListingDetails'):

        MlsId = listingdetail.find('MlsId').text
        List_nodes.append(MlsId)

        MlsName = listingdetail.find('MlsName').text
        List_nodes.append(MlsName)

        DateListed = listingdetail.find('DateListed').text
        List_nodes.append(DateListed)

        Price  = listingdetail.find('Price').text
        List_nodes.append(Price)



    for basicdetail in element.findall('BasicDetails'):

        Description = basicdetail.find('Description').text
        List_nodes.append(Description[:200])

        Bedrooms  = basicdetail.find('Bedrooms').text
        List_nodes.append(Bedrooms)

        Bathrooms  = basicdetail.find('FullBathrooms').text
        List_nodes.append(Bathrooms)

    ## attempting tp go one element deeper, to no avail
    for richdetail in element.findall('RichDetails/Appliances'):

        Appliances  = richdetail.findtext('Appliance')
        List_nodes.append(Appliances)

    ## attempting tp go one element deeper, to no avail
    for richdetail in element.findall('RichDetails/Rooms'):

        Rooms = richdetail.findtext('Room')
        List_nodes.append(Rooms)

    csv_writer.writerow(List_nodes)

#close csv file
xml_data_to_csv.close()


## Creating a DataFrame
with open('output.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    master = list(reader)

header = master[0]
data = master[1:]

df = pd.DataFrame(columns=header, data=data)

## Creating mask for finding "and" in the description
and_mask = df['Description'].str.contains('and')
df = df[and_mask]

## Creating a mask for isolating only 2016 dates and sorted by date

## formatting to DateTime
df['DateListed'] = pd.to_datetime(df['DateListed'])

#add a new column for Year.
df['Year'] = df['DateListed'].apply(lambda x: x.year)
#add a new column for Month.
df['Month'] = df['DateListed'].apply(lambda x: x.month)
#add a new column for Day.
df['Day'] = df['DateListed'].apply(lambda x: x.day)

year_mask = df['Year'] == 2016
df = df[year_mask]

#sortby to get the DataFrame aligned by Date
df.sort_values(['Year', 'Month', 'Day'], ascending=True, inplace=True)
df.drop(['Year', 'Month', 'Day'], axis=1, inplace=True)

#exporting our CSV file
df.to_csv('final.csv')
print(df.head())
