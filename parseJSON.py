"""
Group Name: ZA
Members: Zachary Werle, Aviv Yaaran
The following code is meant to parse the JSON files provided and output the values to text. 
We were provided a file which we used as reference to make ours to better understand the code for milestone 2.
"""
import json

def parseCategories():
    infile = open('yelp_business.JSON')
    outfile = open('yelp_categories.sql', 'w')
    for line in infile:
        jsn = json.loads(line)
        for category in list(jsn["categories"]):
            new_category = category.replace('\'', '\'\'')
            out = 'INSERT INTO categories VALUES (\'' + jsn['business_id'] + '\',\'' + new_category + '\');\n'
            outfile.write(out)
    infile.close()
    outfile.close()

def parseZipCodeData():
    infile = open('zipData.sql')
    outfile = open('yelp_zipCodeData.sql', 'w')
    for line in infile:
        if 'INSERT' not in line:
            out = "INSERT INTO zipcodedata VALUES "
            zip_vals = line.split(',')
            out += zip_vals[0] + ',' + zip_vals[2] + ',0,'
            out += zip_vals[3][:zip_vals[3].index(')')] + ');\n'
            outfile.write(out)
    infile.close()
    outfile.close()

def parseLocation():
    infile = open('yelp_business.JSON')
    outfile = open('yelp_location.sql', 'w')
    inserts = []
    for line in infile:
        out = 'INSERT INTO location VALUES ('
        jsn = json.loads(line)
        out += "'" + jsn["business_id"] +"',"
        out += "'" + jsn["postal_code"] + "'" + ','
        out += "'" + jsn["state"] + "'" + ','
        out += "'" + jsn["city"] + "'"
        out += ');\n'
        outfile.write(out)
    infile.close()
    outfile.close()

def parseBusiness():
    infile = open('yelp_business.JSON')
    outfile = open('yelp_business.sql', 'w')
    for line in infile:
        out = 'INSERT INTO business VALUES ('
        jsn = json.loads(line)
        name = jsn['name'].replace('\'', '\'\'')
        out += "'" + jsn["business_id"] +"',"
        out += "'" + name + "'" + ','
        out += "'" + jsn["state"] + "'" + ','
        out += "'" + jsn["city"] + "'" + ','
        out += "'" + jsn["postal_code"] + "'" + ',' 
        out += '0' + ','
        out += '0.0' + ','
        out += '0'
        out += ');\n'

        """for category in list(jsn["categories"]):
            out += business_id + ',\'' + category + '\'\n'

        for hours in jsn["hours"].items():
            out += business_id + ',\'' + hours[0] + '\',\'' + hours[1][:hours[1].index("-")] + '\',\'' + hours[1][hours[1].index("-") + 1:] + '\'\n'

        for attribute in jsn["attributes"].items():
            if isinstance(attribute[1], dict):
                for sub_attribute in attribute[1].items():
                    out += business_id + ',\'' + sub_attribute[0] + '\',\'' + str(sub_attribute[1]) + '\'\n'
            else:
                out += business_id + ',\'' + attribute[0] + '\',\'' + str(attribute[1]) + '\'\n'"""

        outfile.write(out)
    infile.close()
    outfile.close()
        
def parseReview():
    infile = open('yelp_review.JSON')
    outfile = open('yelp_review.sql', 'w')
    for line in infile:
        out = 'INSERT INTO reviews VALUES ('
        jsn = json.loads(line)
        out += "'" + jsn["review_id"] + "'" + ','
        out += "'" + jsn["business_id"] + "'" + ','
        out += '0,'
        out += str(jsn["stars"]) + ','
        out += '0.0);\n'
        outfile.write(out)
    outfile.close()
    infile.close()

def parseCheckin():
    infile = open('yelp_checkin.JSON')
    outfile = open('yelp_checkin.sql', 'w')
    for line in infile:
        jsn = json.loads(line)
        for days in jsn["time"].items():
            for hours in days[1].items():
                    day = days[0]
                    hour = str(hours[0])
                    numCheckins = str(hours[1])
                    out = 'INSERT INTO checkin VALUES ('
                    out += "'" + jsn["business_id"] +"'"
                    out += ',\'' + day + '\',\'' + hour + '\',' + numCheckins + ');\n'
                    outfile.write(out)
    infile.close()
    outfile.close()

def parseRecievesReview():
    infile = open('yelp_review.JSON')
    outfile = open('yelp_recievesReview.sql', 'w')
    for line in infile:
        out = 'INSERT INTO recievesreview VALUES ('
        jsn = json.loads(line)
        out += "'" + jsn["business_id"] +"',"
        out += "'" + jsn["review_id"] +"');\n"
        outfile.write(out)
    infile.close()
    outfile.close()

def parseRecievesCheckIn():
    infile = open('yelp_checkin.JSON')
    outfile = open('yelp_recievesCheckIn.sql', 'w')
    for line in infile:
        jsn = json.loads(line)
        for days in jsn["time"].items():
            for hours in days[1].items():
                    day = days[0]
                    hour = str(hours[0])
                    numCheckins = str(hours[1])
                    out = 'INSERT INTO recievescheckin VALUES ('
                    out += "'" + jsn["business_id"] +"'"
                    out += ',\'' + day + '\',\'' + hour + '\');\n'
                    outfile.write(out)
    infile.close()
    outfile.close()

def parseType():
    infile = open('yelp_business.JSON')
    outfile = open('yelp_type.sql', 'w')
    for line in infile:
        jsn = json.loads(line)
        for category in list(jsn["categories"]):
            new_category = category.replace('\'', '\'\'')
            out = 'INSERT INTO type VALUES (\'' + jsn['business_id'] + '\',\'' + new_category + '\');\n'
            outfile.write(out)
    infile.close()
    outfile.close()

def parseResidesIn():
    infile = open('yelp_business.JSON')
    outfile = open('yelp_residesIn.sql', 'w')
    for line in infile:
        out = 'INSERT INTO resides_in VALUES ('
        jsn = json.loads(line)
        out += "'" + jsn["business_id"] + "',"
        out += "'" + jsn["postal_code"] + "');\n"
        outfile.write(out)
    infile.close()
    outfile.close()

def parseBusinessIs():
    infile = open('yelp_business.JSON')
    outfile = open('yelp_businessIs.sql', 'w')
    for line in infile:
        out = 'INSERT INTO businessIs VALUES (0,0);\n'
        outfile.write(out)
    infile.close()
    outfile.close()

if __name__ == '__main__':
    parseCategories()
    parseZipCodeData()
    parseLocation()
    parseBusiness()
    parseReview()
    parseCheckin()
    parseRecievesReview()
    parseRecievesCheckIn()
    parseType()
    parseResidesIn()
    parseBusinessIs()
    