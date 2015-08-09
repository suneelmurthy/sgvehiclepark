#  *************************************************************************
#  *
#  * Vps Pte Ltd, Singapore
#  * __________________
#  *
#  *  [2015] - [2015] Vps Pte Ltd Incorporated
#  *  All Rights Reserved.
#  *
# @(#)File:           $sgvehiclepark.py$
# @(#)Version:        $1.0$
# @(#)Last changed:   $Date: 2015/08/08 01:33:00 $
# @(#)Purpose:        Addition of URL References for API's
# @(#)Author:         Suneel N.G.
# @(#)Copyright:      (C) Vps Pte Ltd 2015
# ----------------------------------------------------------------------------------------
# | Version Number   |  		User   			|    			Changes made 			|
# ----------------------------------------------------------------------------------------
# |                  |              			|                           			|
# ----------------------------------------------------------------------------------------
# | 2015/07/26, 1.0  | Suneel N. G.				| API's definitions                 	|
# ----------------------------------------------------------------------------------------
#  * Vps Pte Ltd CONFIDENTIAL
#  * NOTICE:  All information contained herein is, and remains
#  * the property of Vps Pte Ltd Incorporated and its suppliers,
#  * if any.  The intellectual and technical concepts contained
#  * herein are proprietary to Pte Ltd Incorporated
#  * and its suppliers and may be covered by Singapore and Foreign Patents,
#  * patents in process, and are protected by trade secret or copyright law.
#  * Dissemination of this information or reproduction of this material
#  * is strictly forbidden unless prior written permission is obtained
#  * from Pte Ltd Incorporated.
# ----------------------------------------------------------------------------------------

import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
import csv
from google.appengine.ext import db
import models
from google.appengine.api import search
from datetime import datetime
import json
from django.shortcuts import render_to_response
from django import http
import pickle
from google.appengine.api import background_thread

PRODUCT_INDEX = "ProductIndex"
SHOP_INDEX = "ShopIndex"
BLOCKTABLE_INDEX = "BlockTableIndex"
HOURLY_PRICE = 1.0


def query(request):
    response = http.HttpResponse()
    response._headers['Content-Type'] = 'text/html'
    queryString = request.GET.__getitem__('queryString')
    query=search.Query(queryString)
    index = search.Index(name=PRODUCT_INDEX)
    result=index.search(query)
    if not result.results:
        index = search.Index(name=SHOP_INDEX)
        result=index.search(queryString)
    root = {};

    returnResult = [];
    for r in result.results :
        fields = []
        for s in r.fields :
            value=s.value
            if type(value) is search.GeoPoint:
                value = str(s.value.latitude) + "," + str(s.value.longitude)
            fields.append({'name' : s.name, 'value' : value});
        returnResult.append({'fields' : fields})
    root = {
        'data' : returnResult
    };
    data= json.dumps(root)
    return http.HttpResponse(data);

def refresh(request):
        response = http.HttpResponse()
        response._headers['Content-Type'] = 'text/json'
        response.write('YES G running!!')

        shopIndex = search.Index(name=SHOP_INDEX)
        productIndex = search.Index(name=PRODUCT_INDEX)
        shopDocument = []
        mall = "data/" + request.GET.__getitem__('mall');
        index=1
        location = readLocation(mall + '/file.loc')
        tempMall = request.GET.__getitem__('mall')
        with open(mall+'/MallDirectory.csv', 'rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader :
                #print row
                if len(row) > 2 :
                    entry = models.Shop(name=row[0], category=row[1], imageUrl=row[2], address=tempMall + " " +row[3], location = location)
                    shopDocument.append(search.Document(
                    fields=[
                       search.TextField(name='name', value=row[0]),
                       search.TextField(name='category', value=row[1]),
                       search.TextField(name='address', value=entry.address),
                       search.GeoField(name='location', value=search.GeoPoint(location.lat, location.lon))#z
                       ]))
                    entry.put()
                    try:
                        if index % 200 == 0:
                            shopIndex.put(shopDocument)
                            shopDocument = []
                    except search.Error:
                        print "error while indexing.."
                index += 1
        index = 0
        productDocument = []
        file = open(mall+'/ProductListing.csv')
        with open(mall+'/ProductListing.csv', 'rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader :
                if len(row) > 2 :
                    entry = models.Product(name=row[0], category=row[1], price=float(row[2]), address = str(tempMall).replace("-", " ") , location = location)
                    productDocument .append(search.Document(
                    fields=[
                       search.TextField(name='name', value=row[0]),
                       search.TextField(name='category', value=row[1]),
                       search.TextField(name='address', value=entry.address),
                       search.GeoField(name='location', value=search.GeoPoint(location.lat, location.lon))#z
                       ]))
                    entry.put()
                    try:
                        if index % 200 == 0:
                            productIndex.put(productDocument)
                            productDocument = []
                    except search.Error:
                        print "error while indexing.."
                index += 1
            if(index < 200):
                productIndex.put(productDocument)
        return http.HttpResponse();


# Method to add new user
# Throw an error if user already exist
def sgvpnewuserregister(request):
    entity = models.Customer.get_by_key_name(request.Cust_Nric)
    if not entity:
        #No entry with the NRIC detected in the db
        #Creaty entity
        entity = models.Customer
        entity.Cust_Nric = request.Cust_Nric
        entity.Cust_Handphone = request.Cust_Handphone
        entity.Cust_Password = request.Cust_Password
        entity.Cust_Amount = 0
        entity.put()
        # Registration is successful
        response = 'Registration Successful'
    else:
        #Entity is present
        response = 'User Already Exists'
    return response


# Method to update user information
# Throw an error if user does not exist
def sgvpupdateuserinfo(request):
    entity = models.Customer.get_by_key_name(request.Cust_Nric)
    if not entity:
        # No entry with the NRIC detected in the db
        # Invalid Request
        response = 'Invalid User'
    else:
        #Entity is present
        #Update the User Information
        entity.Cust_FirstName = request.Cust_FirstName
        entity.Cust_LastName = request.Cust_LastName
        entity.Cust_Email = request.Cust_Email
        entity.put()
        response = 'User Information Update Successful'
    return response


# Method to edit/add credit card information
# Throw an error if credit card already exist.
def sgvpupdatecreditcardinfo(request):
    entity = models.Customer.get_by_key_name(request.Cust_Nric)
    if not entity:
        # No entry with the NRIC detected in the db
        # Invalid Request
        response = 'Invalid User'
    else:
        # Entity is present
        # Check if the credit card already exist.
        entity_card = models.Customer.Cust_Creditcard.get_by_key_name(request.Card_Number)
        if not entity_card:
            # No entry with above card is detected.
            # Add card
            entity_card = models.Creditcard
            entity_card.Card_Name = request.Card_Name
            entity_card.Card_Number = request.Card_Number
            entity_card.Card_Expiry = request.Card_Expiry
            entity.Cust_Creditcard.append(entity_card)
            # Credit card added successfully
            response = 'New Credit Card Added'
        else:
            # Credit card is detected.
            # Update the data
            entity.Cust_Creditcard.Card_Name = request.Card_Name
            entity.Cust_Creditcard.Card_Number = request.Card_Number
            entity.Cust_Creditcard.Card_Expiry = request.Card_Expiry
            entity.put()
            # Credit card added successfully
            response = 'Credit Card Update Successful'

    return response

# Method to edit/add vehicle information
# Throw an error if vehicle already exist or if invalid.
def sgvpupdatevehicleinfo(request):
    entity = models.Customer.get_by_key_name(request.Cust_Nric)
    if not entity:
        # No entry with the NRIC detected in the db
        # Invalid Request
        response = 'Invalid User'
    else:
        # Entity is present
        # Check if the vehicle already exist.
        entity_vehicle = models.Customer.Cust_Vehicle.get_by_key_name(request.Veh_Regnumber)
        if not entity_vehicle:
            # No entry with above card is detected.
            # Add card
            entity_vehicle = models.Cust_Vehicle
            entity_vehicle.Veh_Regnumber = request.Veh_Regnumber
            # Fetch the below information from internal database or API call
            entity_vehicle.Veh_Type = request.Veh_Type
            entity_vehicle.Veh_Chassisnumber = request.Veh_Chassisnumber
            entity_vehicle.Veh_Enginenumber = request.Veh_Enginenumber
            entity.Cust_Vehicle.append(entity_vehicle)
            # Credit card added successfully
            response = 'New Vehicle Added'
        else:
            # Credit card is detected.
            # Update the data
            entity.Cust_Vehicle.Veh_Regnumber = request.Card_Name
            entity.Cust_Vehicle.Veh_Type = request.Card_Number
            entity.Cust_Vehicle.Veh_Chassisnumber = request.Card_Expiry
            entity.Cust_Vehicle.Veh_Enginenumber = request.Veh_Enginenumber
            entity.put()
            # Credit card added successfully
            response = 'Vehicle Update Successful'

    return response

# Method to authenticate user log in
# Throw an error if user does not exist or invalid password.
def sgvpuserauthentication(request):
    entity = models.Customer.get_by_key_name(request.Cust_Nric)
    if not entity:
        # No entry with the NRIC detected in the db
        # Invalid Request
        response = 'Invalid User'
    else:
        # Entity is present
        # Hash the password
        hash_pwd = hash(request.Cust_Password)
        # Compare the password
        if hash_pwd == entity.Cust_Password:
            # Valid credentials
            response = 'Login Successful'
        else:
            # Incorrect credentials
            response = 'Invalid UserID or Password'
    return response


# Method to delete user
# Throw an error if user does not exist or invalid password.
def sgvpsdeleteuser(request):
    entity = models.Customer.get_by_key_name(request.Cust_Nric)
    if not entity:
        # No entry with the NRIC detected in the db
        # Invalid Request
        response = 'Invalid User'
    else:
        # Entity is present
        # Hash the password
        hash_pwd = hash(request.Cust_Password)
        # Compare the password
        if hash_pwd == entity.Cust_Password:
            # Valid credentials
            # Delete Account
            entity.delete()
            response = 'Account Deleted Successfully'
        else:
            # Incorrect credentials
            response = 'Invalid UserID or Password'
    return response


# Method to add currency to the user
# Throw an error if user does not exist or invalid password.
def sgvpaddcurrency(request):
    entity = models.Customer.get_by_key_name(request.Cust_Nric)
    if not entity:
        # No entry with the NRIC detected in the db
        # Invalid Request
        response = 'Invalid User'
    else:
        # Entity is present
        # Add top up amount.
        # Cannot be greater than $100
        if request.Cust_Amount > 100:
            # Invalid amount.
            # Do Nothing.
            response = 'Amount Exceeds the limit'
        elif request.Cust_Amount < 0:
            # Invalid amount
            response = 'Invalid Amount'
        else:
            # Valid Amount (0 - $100)
            # Decrypt the amount
            decrypt_amount = entity.Cust_Amount
            # Add the amount
            new_amount = decrypt_amount + request.Cust_Amount
            # Encrypt the amount
            encrypt_amount = new_amount
            entity.Cust_Amount = encrypt_amount
            response = 'Amount Update Successful'
    return response

# Method to read the currency
# Throw an error if user does not exist or invalid password.
def sgvpreadcurrency(request):
    entity = models.Customer.get_by_key_name(request.Cust_Nric)
    if not entity:
        # No entry with the NRIC detected in the db
        # Invalid Request
        response = 'Invalid User'
    else:
        # Entity is present
        # Add top up amount.
        # Cannot be greater than $100
        decrypt_amount = entity.Cust_Amount
        response = 'Amount Read Successful'
    return response


def startTimer():
    t = background_thread.start_new_background_thread(startParking, ["foo", "bar"])

def startParking(userId):
    #First get the coupon entry and balance for this user.
    #If there is enough balance, start a timer for half hour first.
    user = models.Customer.get_by_key_name(userId)
    for 
    Timer(5, update, ()).start()











