import csv

# ////////// Gather Territory Records Data //////////
with open("SOPO Territory #01.csv", "r") as structures:

    reader = csv.reader(structures)

    addresses = []
    counter = 0
    for row in reader:
        item_list = []
        #print(row)
        for item in row:
            if item != '':
                item_list.append(item)
        addresses.append(item_list)
    #print(len(addresses))

    for element in addresses:
        if element == []:
            addresses.remove(element)

    index = 0
    for address in addresses:
        if address == ['Address', 'Name', 'Phone Numbers', 'Notes']:
            break
        index += 1
    
    dncs = addresses[4:index]
    clean_addresses = addresses[index + 1:]
            
    # print("DNCs", dncs)
    # print("Addresses", clean_addresses)



updated_addresses = []

# ////////// Gather Poughkeepsie Structures Data //////////
with open("Poughkeepsie Structures.csv", "r") as structures:
    
    reader = csv.DictReader(structures)
    
    for address in clean_addresses:
        print(address[0].upper())
        counter = 0
        for row in reader:
            counter += 1
            print("Row " + row['PROP_ADDR'])
            if address[0].upper() == row['PROP_ADDR']:
                print("match")
            
        print(counter)