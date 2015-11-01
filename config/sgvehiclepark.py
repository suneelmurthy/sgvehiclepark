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

# ----------------------------------------------------------------------------------------
#  import section
# ----------------------------------------------------------------------------------------
import csv
import models
from google.appengine.api import search
from google.appengine.ext import ndb
import json
from django import http
from datetime import datetime
import hashlib, binascii
import math
import time
import logging
import webapp2
from google.appengine.api import memcache


# ----------------------------------------------------------------------------------------
#  definition section
# ----------------------------------------------------------------------------------------
PRODUCT_INDEX = "ProductIndex"
SHOP_INDEX = "ShopIndex"
BLOCKTABLE_INDEX = "BlockTableIndex"
HOURLY_PRICE = 1.0
TIMER_ACTIVE = 0
TIMER_EXPIRED = 1
TIMER_SNA = 2
PARKING_PRICE = [0.5,0.65,2,4]
# Timer value in seconds
DEF_TIMER_VALUE = 30

# ----------------------------------------------------------------------------------------
#  Class Definitions
# ----------------------------------------------------------------------------------------
class timerset_class:
    def __init__(self):
        self.accountuser = None
        self.timercount = 0
        self.vehiclenumber = '0'

class request_class:
    def __init__(self):
        self.Cust_Nric = None
        self.Veh_Regnumber = None
        self.duration = None
        self.coupon = None
        self.Tran_Records = int(0)



# ----------------------------------------------------------------------------------------
#  Method definition section
# ----------------------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------------------
#  User Account Methods
# ----------------------------------------------------------------------------------------
# Method to add new user
# Throw an error if user already exist
def sgvpnewuserregister(request):

    #Check if user exist
    entity = models.Customer.query(models.Customer.Cust_Nric == request.Cust_Nric).get()
    if not entity:
        #No entry with the NRIC detected in the db
        #Creaty entity
        entity = models.Customer()
        entity.Cust_Nric = request.Cust_Nric
        entity.Cust_Handphone = request.Cust_Handphone
        hash_pwd = hashlib.sha256(str(request.Cust_Password) + str(entity.Cust_Handphone))
        hash_pwd_hex = hash_pwd.hexdigest()
        # Hashing the password with salt key
        #hash_pwd = hashlib.pbkdf2_hmac('sha256', str(request.Cust_Password),str(entity.Cust_Handphone),100000)
        #hash_pwd = binascii.hexlify(hash_pwd)
        #entity.Cust_Password = hash_pwd
        entity.Cust_Password = str(hash_pwd_hex)
        # ciphertext = encrypt(entity.Cust_Handphone,10)
        # entity.Cust_Amount = binascii.hexlify(ciphertext)
        entity.Cust_Amount = float(10)
        entity.put()
        # Registration is successful
        response = 'Registration Successful'
    else:
        #Entity is present
        response = 'User Already Exists'
    return response

# Method to update user information
# Throw an error if user does not exist
def sgvpgetuserinfo(request):
    #Check if user exist
    entity = models.Customer.query(models.Customer.Cust_Nric == request.id).get()
    return entity


# Method to update user information
# Throw an error if user does not exist
def sgvpupdateuserinfo(request):
    #Check if user exist
    entity = models.Customer.query(models.Customer.Cust_Nric == request.Cust_Nric).get()
    if not entity:
        # No User in the db
        # Invalid Request
        response = 'Invalid User'
    else:
        # User is present
        # Update the User Information
        entity.Cust_FirstName = request.Cust_FirstName
        entity.Cust_LastName = request.Cust_LastName
        entity.Cust_Email = request.Cust_Email
        entity.put()
        response = 'User Information Update Successful'
    return response

# Method to delete user
# Throw an error if user does not exist or invalid password.
def sgvpsdeleteuser(request):
    # Check if user exist
    entity = models.Customer.query(models.Customer.Cust_Nric == request.Cust_Nric).get()
    if not entity:
        # No entry with the NRIC detected in the db
        # Invalid Request
        response = 'Invalid User or User does not exist'
    else:
        # User present
        # Hash the password
        # hash_pwd = hashlib.pbkdf2_hmac('sha256', str(request.Cust_Password),str(entity.Cust_Handphone),100000)
        # hash_pwd = binascii.hexlify(hash_pwd)
        hash_pwd = hashlib.sha256(str(request.Cust_Password) + str(entity.Cust_Handphone))
        hash_pwd_hex = hash_pwd.hexdigest()
        # Compare the password
        if hash_pwd_hex == entity.Cust_Password:
            # Valid credentials
            # Delete Account
            entity.key.delete()
            response = 'Account Deleted Successfully'
        else:
            # Incorrect credentials
            response = 'Invalid Password'
    return response


# Method to authenticate user log in
# Throw an error if user does not exist or invalid password.
def sgvpuserauthentication(request):
    # Check if user exist
    entity = models.Customer.query(models.Customer.Cust_Nric == request.Cust_Nric).get()
    if not entity:
        # No entry with the NRIC detected in the db
        # Invalid Request
        response = 'Invalid User or User does not exist'
    else:
        # Entity is present
        # Hash the password
        # hash_pwd = hashlib.pbkdf2_hmac('sha256', str(request.Cust_Password),str(entity.Cust_Handphone),100000)
        # hash_pwd = binascii.hexlify(hash_pwd)
        # Compare the password
        hash_pwd = hashlib.sha256(str(request.Cust_Password) + str(entity.Cust_Handphone))
        hash_pwd_hex = hash_pwd.hexdigest()
        if hash_pwd_hex == entity.Cust_Password:
            # Valid credentials
            response = 'Login Successful'
        else:
            # Incorrect credentials
            response = 'Invalid UserID or Password'
    return response


# Method to read out latest 10 transactions
# Throw an error if user does not exist or invalid password.
def sgvpusertransactionhistory(request):
    # Check if user exist
    entity = models.Customer.query(models.Customer.Cust_Nric == request.Cust_Nric).get()
    if not entity:
        # No entry with the NRIC detected in the db
        # Invalid Request
        response = 'Invalid User or User does not exist'
    else:
        # Entity is present
        # Query the data
        Transaction_entity = models.Transaction.query(models.Transaction.Trans_Nric == str(request.Cust_Nric))
        Transaction_entity = Transaction_entity.order(-models.Transaction.Trans_Starttime)
        Transaction_entity = Transaction_entity.fetch(int(request.Tran_Records))
        response = 'Transaction Records Retrieved successfully'
    return response


# Method to read out latest 10 transactions
# Throw an error if user does not exist or invalid password.
def sgvptransactionhistory():
    # Check if user exist
    Transaction_entity = models.Transaction.query().fetch()
    # if not entity:
    #     # No entry with the NRIC detected in the db
    #     # Invalid Request
    #     response = 'Invalid User or User does not exist'
    # else:
    #     # Entity is present
    #     # Query the data

    response = 'Invalid User or User does not exist'
    # response = json.dumps(Transaction_entity)
    return Transaction_entity


# Method to read out if user is already registered
# Throw an error if user does not exist or invalid password.
def sgvpusercheck(request):
    # Check if user exist
    entity = models.Customer.query(models.Customer.Cust_Nric == request.Cust_Nric).get()
    if not entity:
        # No entry with the NRIC detected in the db
        # User does not exist
        response = 'Invalid User or User does not exist'
    else:
        # Entity is present
        # User exist
        response = 'User exist'
    return response

# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
#  Credit Card Methods
# ----------------------------------------------------------------------------------------
# Method to edit/add credit card information
# Throw an error if credit card already exist.
def sgvpupdatecreditcardinfo(request):
    # Check if user exist
    entity = models.Customer.query(models.Customer.Cust_Nric == request.Cust_Nric).get()
    if not entity:
        # No entry with the NRIC detected in the db
        # Invalid Request
        response = 'Invalid User'
    else:
        # Entity is present
        # Check if the credit card already exist.
        card_found = None
        for each_card in entity.Cust_Creditcard:
            if each_card.Card_Number == request.Card_Number:
                # Credit Card already available
                card_found = 1
                break
        # card_status
        if not card_found:
            # Card not available in the database
            # Add card
            card = models.Creditcard()
            card.Card_Name = request.Card_Name
            # Type and card check is required
            card.Card_Number = int(request.Card_Number)
            card.Card_Expiry = request.Card_Expiry
            entity.Cust_Creditcard.append(card)
            entity.put()
            # Credit card added successfully
            response = 'New Credit Card Added Successfully'
        else:
            # Card Present
            response = 'Card Already Exists'
    return response

# Method to delete credit card information
# Throw an error if credit card does not exist.
def sgvpdeletecreditcard(request):
    # Check if user exist
    entity = models.Customer.query(models.Customer.Cust_Nric == request.Cust_Nric).get()
    if not entity:
        # No entry with the NRIC detected in the db
        # Invalid Request
        response = 'Invalid User'
    else:
        # Entity is present
        # Check if the credit card already exist.
        card_found = None
        card_count = 0
        for each_card in entity.Cust_Creditcard:
            card_count += 1
            if each_card.Card_Number == request.Card_Number:
                # Credit Card already available
                card_found = 1
                break
        # card_status
        if not card_found:
            # Card not available in the database
            # Invalid Request
            # Credit card added successfully
            response = 'Invalid Credit Card or Credit Card Does not Exist.'
        else:
            # Card Present
            # Delete Card
            del entity.Cust_Creditcard[card_count - 1]
            entity.put()
            response = 'Card Deleted Successfully'
    return response
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
#  Vehicle Methods
# ----------------------------------------------------------------------------------------
# Method to edit/add vehicle information
# Throw an error if vehicle already exist or if invalid.
def sgvpnewvehicleregister(request):
    # Check if user exist
    entity = models.Customer.query(models.Customer.Cust_Nric == request.Cust_Nric).get()
    if not entity:
        # No entry with the NRIC detected in the db
        # Invalid Request
        response = 'Invalid User or User does not exist'
    else:
        # Entity is present
        # Check if the vehicle already exist.
        # Check if the credit card already exist.
        vehicle_found = None
        for each_veh in entity.Cust_Vehicle:
            if each_veh.Veh_Regnumber == request.Veh_Regnumber:
                # Vehicle already available
                vehicle_found = 1
                break

        # card_status
        if not vehicle_found:
            # Vehicle not available in the database
            # Add vehicle
            veh = models.Vehicle()
            # Vehicle check from LTA is needed (Backend/frontend)
            veh.Veh_Regnumber = request.Veh_Regnumber
            veh.Veh_Type = request.Veh_Type
            veh.Veh_Chassisnumber = request.Veh_Chassisnumber
            veh.Veh_Enginenumber = request.Veh_Enginenumber
            entity.Cust_Vehicle.append(veh)
            entity.put()
            # Credit card added successfully
            response = 'New Vehicle Added Successfully'
        else:
            # Vehicle Present in Database
            response = 'Vehicle Already Exists'
    return response

# Method to delete vehicle information
# Throw an error if vehicle already exist or if invalid.
def sgvpdeletevehicle(request):
    # Check if user exist
    entity = models.Customer.query(models.Customer.Cust_Nric == request.Cust_Nric).get()
    if not entity:
        # No entry with the NRIC detected in the db
        # Invalid Request
        response = 'Invalid User or User does not exist'
    else:
        # Entity is present
        # Check if the vehicle already exist.
        vehicle_found = None
        vehicle_count = 0
        # Check if the credit card already exist.
        for each_veh in entity.Cust_Vehicle:
            vehicle_count += 1
            if each_veh.Veh_Regnumber == request.Veh_Regnumber:
                # Vehicle already available
                vehicle_found = 1
                break
        # card_status
        if not vehicle_found:
            # Vehicle not available in the database
            # Invalid Request
            response = 'Invalid Vehicle or Vehicle does not exist'
        else:
            # Vehicle Present in Database
            # Delete Vehicle
            del entity.Cust_Vehicle[vehicle_count - 1]
            entity.put()
            response = 'Vehicle Deleted Successfully'
    return response
# ----------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------
#  Transaction/Credit Methods
# ----------------------------------------------------------------------------------------
# Method to update currency to the user account
# Throw an error if user does not exist or invalid password.
def sgvpupdatecurrency(request):
    # Check if user exist
    entity = models.Customer.query(models.Customer.Cust_Nric == request.Cust_Nric).get()
    if not entity:
        # No entry with the NRIC detected in the db
        # Invalid Request
        response = 'Invalid User or User Does Not Exist'
    else:
        # Entity is present
        # Update User Amount.
        # Call LTA Server API
        amount_lta = 100
        entity.Cust_Amount = float(amount_lta)
        entity.put()
        response = 'Amount Update Successful'
    return response

# Method to read the currency
# Throw an error if user does not exist or invalid password.
def sgvpreadcurrency(request):
    response = {}
    # Check if user exist
    entity = models.Customer.query(models.Customer.Cust_Nric == request.Cust_Nric).get()
    if not entity:
        # No entry with the NRIC detected in the db
        # Invalid Request
        Amount = None
        ResponseMsg = 'Invalid User'
    else:
        # Entity is present
        # Read Amount
        # plaintext = decrypt(entity.Cust_Handphone,entity.Cust_Amount)
        # decrypt_amount = binascii.hexlify(plaintext)
        # Amount = decrypt_amount
        Amount = entity.Cust_Amount
        ResponseMsg = 'Amount Read Successful'
    response = {
        'Amount' : Amount,
        'ResponseMsg' : ResponseMsg
    }
    response = json.dumps(response)
    return response
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
#  Coupon Start, Stop & Renew Methods
# ----------------------------------------------------------------------------------------
# Method to start the parking coupon
# Throw an error if vehicle/user is invalid.
def sgvpstartcoupon(request):
    # Variables
    amount_valid = None

    # Check if user exist
    entity = models.Customer.query(models.Customer.Cust_Nric == request.Cust_Nric).get()
    if not entity:
        # No entry with the NRIC detected in the db
        # Invalid Request
        response = 'Invalid User or User does not exist'
    else:
        # User is Valid
        # Check if the vehicle Reg number is valid.
        vehicle_found = None
        vehicle_count = 0
        for each_veh in entity.Cust_Vehicle:
            vehicle_count += 1
            if each_veh.Veh_Regnumber == request.Veh_Regnumber:
                # Vehicle already available
                vehicle_found = True
                veh_regnumber = each_veh.Veh_Regnumber
                break

        # vehicle Status
        if not vehicle_found:
            # Vehicle not available in the database
            # Invalid Request
            response = 'Invalid Vehicle or Vehicle Does Not Exists.'
        else:
            # Vehicle Present in Database
            # Variables
            start_timer = False
            parking_amount = 0.0
            # Duration in min
            duration = request.Park_Duration
            # Coupon Type
            # 0 = Normal
            # 1 = CBD
            # 2 = Night
            # 3 = Full Day Parking
            coupon_type = request.Park_Coupon
            duration_valid = (duration % 1)
            coupon_valid = (coupon_type < 4)
            if (0 == duration_valid) and coupon_valid:
                # Coupon and Duration elements are valid
                # Update Code Later
                parking_amount = (duration)*PARKING_PRICE[coupon_type]

                # Balance check for the parking request
                user_amount = entity.Cust_Amount
                if parking_amount <= user_amount:
                    # Sufficient Amount available
                    amount_valid = True
                else:
                    # Insufficient Amount
                    amount_valid = False

                # Check if any coupon is active for the same vehicle
                vehicle_entity = models.Transaction.query(ndb.AND(models.Transaction.Trans_Regnumber == str(request.Veh_Regnumber),
                                                                  models.Transaction.Trans_Stoptime == None)).get()
                if not vehicle_entity:
                    # No active transaction detected
                    # start new timer
                    start_timer = True
                    response = 'Coupon started successfully'
                else:
                    # Active transaction detected
                    start_timer = False
                    vehicle_start_user = vehicle_entity.Trans_Nric
                    if (vehicle_start_user == entity.Cust_Nric):
                        # New request is from the same user
                        response = 'Coupon already active.'
                    else:
                        # Already active from a different user
                        response = 'Coupon already active from a different user.'
            else:
                # Invalid coupon or duration
                response = 'Invalid Coupon or Duration.'

            # Timer Handling
            if True == start_timer:
                # start timer
                # variables
                timer_found = False
                if True == amount_valid:
                    # Valid Amount detected

                    # Credit Transaction
                    amount = entity.Cust_Amount
                    amount = amount - parking_amount
                    entity.Cust_Amount = float(amount)
                    entity.put()

                    # Log transaction
                    entity_transaction = models.Transaction()
                    entity_transaction.Trans_Type = 'Parking Coupon Normal'
                    entity_transaction.Trans_Regnumber = entity.Cust_Vehicle[vehicle_count - 1].Veh_Regnumber
                    entity_transaction.Trans_Chassisnumber = entity.Cust_Vehicle[vehicle_count - 1].Veh_Chassisnumber
                    entity_transaction.Trans_Enginenumber = entity.Cust_Vehicle[vehicle_count - 1].Veh_Enginenumber
                    entity_transaction.Trans_Amount = float(parking_amount)
                    entity_transaction.Trans_Nric = entity.Cust_Nric
                    entity_transaction.Trans_Startduration = (request.Park_Duration * 60)
                    entity_transaction.Trans_Timerstatus = int(TIMER_ACTIVE)
                    time_stamp = datetime.utcnow()
                    entity_transaction.Trans_Starttime = time_stamp
                    entity_transaction.Trans_Date = time_stamp.date()
                    entity_transaction.Trans_Location = ndb.GeoPt(request.Park_Loclat, request.Park_Loclong)
                    entity_transaction.put()

                    # Mem cache handling
                    entity_memcache = memcache.get("Transaction_Coupon")

                    if not entity_memcache:
                        transactionarray = []
                        transactionarray.append(entity_transaction)
                        memcache.set("Transaction_Coupon",transactionarray,1200)
                    else:
                        transactionarray = []
                        for each_memset in entity_memcache:
                            transactionarray.append(each_memset)
                        transactionarray.append(entity_transaction)
                        memcache.set("Transaction_Coupon",transactionarray,1200)
                else:
                    # No Valid Amount
                    response = 'Insufficient Balance'

    return response

# Method to stop the parking coupon
# Throw an error if vehicle/user is invalid.
def sgvpstopcoupon(request):
    # Check if user exist
    entity = models.Customer.query(models.Customer.Cust_Nric == request.Cust_Nric).get()
    if not entity:
        # No entry with the NRIC detected in the db
        # Invalid Request
        response = 'Invalid User or User does not exist'
    else:
        # User is Valid
        # Check if the vehicle Reg number is valid.
        vehicle_found = False
        vehicle_count = 0
        veh_regnumber = None
        for each_veh in entity.Cust_Vehicle:
            vehicle_count += 1
            if each_veh.Veh_Regnumber == request.Veh_Regnumber:
                # Vehicle already available
                vehicle_found = 1
                veh_regnumber = each_veh.Veh_Regnumber
                break

         # vehicle Status
        if not vehicle_found:
            # Vehicle not available in the database
            # Invalid Request
            response = 'Invalid Vehicle or Vehicle Does Not Exists.'
        else:
            # Vehicle Present in Database
            # Check if any coupon is active for the same vehicle
            vehicle_entity = models.Transaction.query(ndb.AND(models.Transaction.Trans_Regnumber == str(request.Veh_Regnumber),
                                                              models.Transaction.Trans_Stoptime == None)).get()
            if not vehicle_entity:
                # No Active transaction detected
                response = 'No Active Parking Coupon'
            else:
                # Active transaction detected
                # Log the transaction
                time_stamp = datetime.utcnow()
                vehicle_entity.Trans_Stoptime = time_stamp
                time_diff = time_stamp - vehicle_entity.Trans_Starttime
                vehicle_entity.Trans_Stopduration = int(time_diff.seconds)

                Trans_Amount = vehicle_entity.Trans_Amount
                unit_cost = (Trans_Amount * 60)/vehicle_entity.Trans_Startduration
                new_time = time_diff.seconds/60.0
                units = math.ceil(float(new_time))
                parking_amount = (units)*unit_cost

                vehicle_entity.Trans_Amount = parking_amount
                vehicle_entity.put()

                # Credit Transactions
                entity.Cust_Amount += Trans_Amount
                amount = entity.Cust_Amount
                amount = amount - parking_amount
                entity.Cust_Amount = float(amount)
                entity.put()

                # Delete from Mem cache
                entry_count = 0
                entry_found = False
                entity_memcache = memcache.get("Transaction_Coupon")
                if entity_memcache:
                    for each_memcache in entity_memcache:
                        entry_count += 1
                        if each_memcache.Trans_Regnumber == request.Veh_Regnumber:
                            # Memcache Entry found
                            entry_found = True
                            break

                    if entry_found == True:
                        # Delete Memcache Entry
                        del entity_memcache[entry_count-1]
                        # Update mem cache
                        if entity_memcache:
                            memcache.set("Transaction_Coupon",entity_memcache,1200)
                        else:
                            memcache.delete("Transaction_Coupon")

                response = 'Parking Coupon Stopped Successfully'
    return response

# Method to renew the parking coupon
# Throw an error if vehicle/user is invalid.
def sgvprenewcoupon(request):
    # Check if user exist
    entity = models.Customer.query(models.Customer.Cust_Nric == request.Cust_Nric).get()
    if not entity:
        # No entry with the NRIC detected in the db
        # Invalid Request
        response = 'Invalid User or User does not exist'
    else:
        # User is Valid
        # Check if the vehicle Reg number is valid.
        vehicle_found = None
        vehicle_count = 0
        veh_regnumber = None
        for each_veh in entity.Cust_Vehicle:
            vehicle_count += 1
            if each_veh.Veh_Regnumber == request.Veh_Regnumber:
                # Vehicle already available
                vehicle_found = 1
                break

         # vehicle Status
        if not vehicle_found:
            # Vehicle not available in the database
            # Invalid Request
            response = 'Invalid Vehicle or Vehicle Does Not Exists.'
        else:
            # Vehicle Present in Database
            # Validate Coupon type and amount.
            # Duration in min
            duration = request.Park_Duration
            # Coupon Type: 0 = Normal, 1 = CBD, 2 = Night, 3 = Full Day Parking
            coupon_type = request.Park_Coupon
            duration_valid = (duration % 1)
            coupon_valid = (coupon_type < 4)
            if (0 == duration_valid) and coupon_valid:
                # Coupon and Duration elements are valid
                parking_amount = (duration)*PARKING_PRICE[coupon_type]
                # Balance check for the parking request
                user_amount = entity.Cust_Amount
                if float(parking_amount) <= float(user_amount):
                    # Sufficient Amount available
                    # Check if any coupon is active for the same vehicle
                    vehicle_entity = models.Transaction.query(ndb.AND(models.Transaction.Trans_Regnumber == str(request.Veh_Regnumber),
                                                                      models.Transaction.Trans_Stoptime == None)).get()
                    if not vehicle_entity:
                        # No Active transaction detected
                        # Start New Timer
                        response = 'Parking Coupon Has Expired'
                    else:
                        # Active transaction detected

                        #Credit Transaction
                        amount = entity.Cust_Amount
                        amount = amount - parking_amount
                        entity.Cust_Amount = float(amount)
                        entity.put()

                        # Update Transaction entity
                        vehicle_entity.Trans_Startduration += request.Park_Duration * 60
                        vehicle_entity.Trans_Amount += parking_amount
                        vehicle_entity.put()

                        # Update Memcache
                        memcache_count = 0
                        entity_memcache = memcache.get("Transaction_Coupon")

                        if entity_memcache:
                            for each_memcache in entity_memcache:
                                memcache_count += 1
                                if each_memcache.Trans_Regnumber == str(request.Veh_Regnumber):
                                    # Memcache entry found
                                    # Update the entry
                                    entity_memcache[memcache_count - 1] = vehicle_entity

                                    # write memcache
                                    memcache.set("Transaction_Coupon",entity_memcache,1200)

                        # Response message
                        response = 'Coupon Renewed Successfully.'
                else:
                    # Insufficient Amount
                    response = 'Insufficient Balance. Please Top up.'
            else:
                # Invalid coupon or duration
                response = 'Invalid Coupon or Duration.'
    return response
# ----------------------------------------------------------------------------------------


# Method to add new user
# Throw an error if user already exist
def sgvptestuser(request):
    queryString = request.GET.__getitem__('queryString')
    request_coupon = request_class()
    request_coupon.Cust_Nric = queryString
    request_coupon.Veh_Regnumber = str(10001)
    request_coupon.coupon = 0
    request_coupon.duration = 30
    request_coupon.Tran_Records = 12
    # response = sgvpstartcoupon(request_coupon)
    # time.sleep(1)
    # response = sgvpstopcoupon(request_coupon)
    response = sgvpusertransactionhistory(request_coupon)
    a = 5
    #entity = models.Customer.get_by_key_name(queryString)
    # entity = models.Customer.query(models.Customer.Cust_Nric == queryString).get()
    # if not entity:
    #     #No entry with the NRIC detected in the db
    #     #Creaty entity
    #     entity = models.Customer()
    #     entity.Cust_Nric = queryString
    #     entity.Cust_Handphone = 82852567
    #     entity.Cust_Password = '12345678'
    #     entity.Cust_Amount = 100
    #     entity.put()
    #     # Registration is successful
    #     response = 'Registration Successful'
    # else:
    #     #Entity is present
    #     # entity.Cust_Amount = 1000
    #     # entity.put()
    #     entity.key.delete()
    #     response = 'User Already Exists'
    return response

def sgvptestcard(request):
    queryString = request.GET.__getitem__('queryString')
    #entity = models.Customer.get_by_key_name(queryString)
    entity = models.Customer.query(models.Customer.Cust_Nric == queryString).get()
    if not entity:
        #No entry with the NRIC detected in the db
        response = 'User does not exist'
    else:
        #Entity is present
        # check if card is present

        found = None
        for each in entity.Cust_Creditcard:
            if each.Card_Number == (10000 + int(queryString)):
                found = 1

                del entity.Cust_Creditcard[0]
                #entity.Cust_Creditcard[0].delete
                entity.put()
                break

        if not found:
            # No card present
            card = models.Creditcard()
            card.Card_Name = 'Suneel'
            card.Card_Number = (10000 + int(queryString))
            card.Card_Expiry = '02/17'
            entity.Cust_Creditcard.append(card)
            entity.put()
        else:
            # Card Present
            response = 'Card Exists'
        response = 'User Already Exists'
    return response

# -------------------------------------End Of File----------------------------------------


# ----------------------------------------------------------------------------------------
#  Periodic Cron Task
# ----------------------------------------------------------------------------------------
# Method to run cyclically every 1 minute
# Method is responsible to monitor the parking coupon time and notify when the coupon is expired.
class cron_task1min(webapp2.RequestHandler):
    def post(self): # should run at most 1/s
        print "Post", time.time()

    def get(self):
        entry_count = 0
        delete_index = []

        # Time Stamp
        time_stamp = datetime.utcnow()
        logging.debug('Cron Start')
        logging.debug(datetime.utcnow())

        # Read from memcache
        entity_memcache = memcache.get("Transaction_Coupon")

        if entity_memcache:
            for each_memcache in entity_memcache:

                # Time difference
                time_diff = time_stamp - each_memcache.Trans_Starttime

                # Check if timer has expired
                if time_diff.seconds > each_memcache.Trans_Startduration:
                    # Timer has expired
                    # Stop the coupoun
                    # Delete from memcache
                    delete_index.append(int(entry_count))

                    # Retrieve the transaction entity
                    vehicle_entity = models.Transaction.query(ndb.AND(models.Transaction.Trans_Regnumber == str(each_memcache.Trans_Regnumber),
                                                                      models.Transaction.Trans_Stoptime == None)).get()

                    if vehicle_entity:
                        # Active transaction detected
                        # Log the transaction
                        vehicle_entity.Trans_Stoptime = time_stamp
                        vehicle_entity.Trans_Stopduration = vehicle_entity.Trans_Startduration
                        vehicle_entity.put()

                # loop counter
                entry_count += 1

        # Delete memcache entry
        for i in sorted(delete_index, reverse=True):
            del entity_memcache[i]

        # Update mem cache
        if entity_memcache:
            memcache.set("Transaction_Coupon",entity_memcache,1200)
        else:
            memcache.delete("Transaction_Coupon")

        # Logging
        logging.debug('Cron End')
        logging.debug(datetime.utcnow())


# -----------------------------------End Of Cron File-------------------------------------


# ----------------------------------------------------------------------------------------
# Cron Configuration
# ----------------------------------------------------------------------------------------
app = webapp2.WSGIApplication([
# ('/worker', backgroundthread_cbck),
('/crontask1min', cron_task1min),
])

# -------------------------------End Of Cron Configuration--------------------------------
