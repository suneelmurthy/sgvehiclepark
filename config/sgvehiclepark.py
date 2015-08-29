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
import threading
import time
from threading import Timer
import logging
from google.appengine.api import background_thread
from google.appengine.api import taskqueue
import webapp2

#from simplecrypt import encrypt, decrypt



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
        for each_veh in entity.Cust_Creditcard:
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
    duration = None
    coupon_type = None
    duration_valid = None
    coupon_type = None
    response = None

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
            parking_timer = False
            updateparktimer = False
            # Duration in min
            duration = request.Park_Duration
            # Coupon Type
            # 0 = Normal
            # 1 = CBD
            # 2 = Night
            # 3 = Full Day Parking
            coupon_type = request.Park_Coupon
            duration_valid = (duration % 30)
            coupon_valid = (coupon_type < 4)
            if (0 == duration_valid) and coupon_valid:
                # Coupon and Duration elements are valid
                parking_amount = (duration/30)*PARKING_PRICE[coupon_type]

                #Parking Timer
                parking_timer = (duration/30)

                # Balance check for the parking request
                amount_valid = None
                user_amount = entity.Cust_Amount
                if parking_amount <= user_amount:
                    # Sufficient Amount available
                    amount_valid = True
                else:
                    # Insufficient Amount
                    amount_valid = False

                # Check if any coupon is active for the same vehicle
                vehicle_status = None
                vehicle_start_user = None
                vehicle_entity = models.Transaction.query(ndb.AND(models.Transaction.Trans_Regnumber == str(request.Veh_Regnumber),
                                                                  models.Transaction.Trans_Timerstatus == int(TIMER_ACTIVE))).get()
                if not vehicle_entity:
                    # No Active transaction detected
                    vehicle_status = False
                else:
                    # Active transaction detected
                    vehicle_status = True
                    vehicle_start_user = vehicle_entity.Trans_Nric

                # Check if coupon/timer window is open
                if True == vehicle_status:
                    # Active transaction/window detected
                    # check if the active request is from the same user
                    if (vehicle_start_user == entity.Cust_Nric):
                        # New request is from the same user
                        updateparktimer = True
                        start_timer = True
                        response = 'Coupon already active.'
                    else:
                        # Already active from a different user
                        updateparktimer = False
                        # Check if coupon is active
                        if not vehicle_entity.Trans_Stoptime:
                            # Coupon is active
                            # Invalid Request
                            response = 'Coupon already active from a different user.'
                            start_timer = False
                        else:
                            # Coupon is inactive
                            # Check if coupon window is active
                            if int(TIMER_ACTIVE) == vehicle_entity.Trans_Timerstatus:
                                # Timer still running Coupon window open
                                # Transfer the current status
                                start_timer = False
                            else:
                                # Timer Coupon window expired
                                # Start a new timer
                                start_timer = True
                            response = 'Coupon started successfully'
                else:
                    # No active transaction detected
                    # start new timer
                    start_timer = True
                    response = 'Coupon started successfully'
            else:
                # Invalid coupon or duration
                response = 'Invalid Coupon or Duration.'

            if True == start_timer:
                # start timer
                # variables
                timer_found = False
                if True == amount_valid:
                    # Valid Amount detected
                    # Start Timer
                    if updateparktimer == True:
                        #  Already active window detected and active timer detected.
                        # Update timer count.
                        timerthreads = threading.enumerate()
                        for timers in timerthreads:
                            logging.debug(timers.getName())
                            if timers.getName() == veh_regnumber:
                                # Vehicle timer thread found update

                                timer_found = True
                                # Update timer count
                                timers.args[0].timercount += parking_timer
                                logging.debug("Timer Thread")
                                break
                            else:
                                # Timer not fount start new timer
                                timer_found = False
                                # timer_entity = Timer(DEF_TIMER_VALUE, timerexpired_callback, int(parkingtimer))
                                # timer_entity.setName(veh_regnumber)
                                # timer_entity.start()

                    # Timer status
                    if timer_found != True:
                        # start new timer
                        # timer variable set
                        user_set = timerset_class()
                        user_set.timercount = int(parking_timer)
                        user_set.vehiclenumber = str(veh_regnumber)
                        user_set.accountuser = entity.Cust_Nric

                        #Starting background thread

                        # bg_thread = threading.Thread(target=thread_cbck, args=(user_set,))
                        # bg_thread.start()
                        taskqueue.add(url='/worker', params={'timercount':parking_timer, 'vehiclenumber':veh_regnumber,
                                                            'accountuser':entity.Cust_Nric})


                        # timer_entity = Timer(int(DEF_TIMER_VALUE), timerexpired_callback, (user_set,))
                        # timer_entity.setName(veh_regnumber)
                        # timer_entity.start()
                        logging.debug("Timer Started")
                        timerthreads = threading.enumerate()
                        for timers in timerthreads:
                            logging.debug(timers.getName())
                            if timers.getName() == veh_regnumber:
                                logging.debug("Timer Found 1")

                    # Credit Transaction
                    amount = entity.Cust_Amount
                    amount = amount - PARKING_PRICE[coupon_type]
                    entity.Cust_Amount = float(amount)
                    entity.put()

                    # Log transaction
                    entity_transaction = models.Transaction()
                    entity_transaction.Trans_Type = 'Parking Coupon Normal'
                    entity_transaction.Trans_Regnumber = entity.Cust_Vehicle[vehicle_count - 1].Veh_Regnumber
                    entity_transaction.Trans_Chassisnumber = entity.Cust_Vehicle[vehicle_count - 1].Veh_Chassisnumber
                    entity_transaction.Trans_Enginenumber = entity.Cust_Vehicle[vehicle_count - 1].Veh_Enginenumber
                    entity_transaction.Trans_Amount = float(PARKING_PRICE[coupon_type])
                    entity_transaction.Trans_Nric = entity.Cust_Nric
                    entity_transaction.Trans_Timerstatus = int(TIMER_ACTIVE)
                    time_stamp = datetime.utcnow()
                    entity_transaction.Trans_Starttime = time_stamp
                    entity_transaction.Trans_Date = time_stamp.date()
                    entity_transaction.put()
                    logging.debug("Delay Started")
                    #time.sleep(35)
                    logging.debug("Delay Ended")
                    timerthreads = threading.enumerate()
                    for timers in timerthreads:
                        logging.debug(timers.getName())
                        if timers.getName() == veh_regnumber:
                            logging.debug("Timer Found 1")

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
        vehicle_found = None
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
                # Search for the timer thread.
                timerthreads = threading.enumerate()
                for timers in timerthreads:
                    if timers.getName() == str(veh_regnumber):
                        # Vehicle timer thread found update
                        # Update timer count
                        timers.args[0].timercount = 0
                        response = 'Parking Coupon Stopped Successfully'
                        # Log Transaction.
                        time_stamp = datetime.utcnow()
                        vehicle_entity.Trans_Stoptime = time_stamp
                        time_diff = time_stamp - vehicle_entity.Trans_Starttime
                        vehicle_entity.Trans_Duration = int(time_diff.seconds)
                        vehicle_entity.put()
                        break
                    else:
                        # Timer not found
                        response = 'Parking Coupon Has Expired'
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
                veh_regnumber = each_veh.Veh_Regnumber
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
            duration_valid = (duration % 30)
            coupon_valid = (coupon_type < 4)
            if (0 == duration_valid) and coupon_valid:
                # Coupon and Duration elements are valid
                parking_amount = (duration/30)*PARKING_PRICE[coupon_type]
                #Parking Timer
                parking_timer = (duration/30)
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
                        # Search for the timer thread.
                        # Update the timer count
                        timerthreads = threading.enumerate()
                        for timers in timerthreads:
                            if timers.getName() == str(veh_regnumber):
                                # Vehicle timer thread found update
                                # Update timer count
                                timers.args[0].timercount += parking_timer
                                response = 'Parking Coupon Renewed Successfully'
                                break
                            else:
                                # Timer not found
                                response = 'Parking Coupon Has Expired'
                else:
                    # Insufficient Amount
                    response = 'Insufficient Balance. Please Top up.'
            else:
                # Invalid coupon or duration
                response = 'Invalid Coupon or Duration.'
    return response
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
#  Timer call back
# ----------------------------------------------------------------------------------------
# Method to start the parking coupon
# Throw an error if vehicle/user is invalid.
def timerexpired_callback(*args, **kwargs):
    print "Timer Expired", time.time(), args[0].vehiclenumber, args[0].timercount
    logging.debug("Call Back triggered")
    timerthreads = threading.enumerate()
    for timers in timerthreads:
        print timers.getName()
        if str(timers.getName()) == str(args[0].vehiclenumber):
            print timers.getName()
            logging.debug("Inside callback", timers.getName())
            # Vehicle timer thread found
            # check timer counter
            if args[0].timercount > 0:
                # decrement the timer
                args[0].timercount -= 1

            # Check if timer is to restarted
            if args[0].timercount == 0:
                # stop the timer
                timers.cancel()
                #del args[0]
            else:
                # Restart the timer
                timers.start()

            # Log transaction
            vehicle_entity = models.Transaction.query(ndb.AND(models.Transaction.Trans_Regnumber == str(args[0].vehiclenumber),
                                                              models.Transaction.Trans_Timerstatus == int(TIMER_ACTIVE))).get()

            if not vehicle_entity:
                # No Active transaction detected
                # Log Error
                response = 'No Transaction'
                print "***************************************No Vehicle******************************"
            else:
                # Log
                print "***************************************Expired******************************"
                print vehicle_entity.Trans_Regnumber
                if not vehicle_entity.Trans_Stoptime:
                    # Log stop time
                    time_stamp = datetime.utcnow()
                    vehicle_entity.Trans_Stoptime = time_stamp
                    time_diff = time_stamp - vehicle_entity.Trans_Starttime
                    print time_diff.seconds
                    vehicle_entity.Trans_Duration = int(time_diff.seconds)
                    vehicle_entity.put()
                vehicle_entity.Trans_Timerstatus = int(TIMER_EXPIRED)
                vehicle_entity.put()
        else:
            # Timer not fount start new timer
            response = 'Invalid Call Back'
    return response
# ----------------------------------------------------------------------------------------

class backgroundthread_cbck(webapp2.RequestHandler):
    def post(self): # should run at most 1/s
        timercount = self.request.get('timercount')
        vehiclenumber = self.request.get('vehiclenumber')
        accountuser = self.request.get('accountuser')
        user_set = timerset_class()
        user_set.timercount = int(timercount)
        user_set.vehiclenumber = str(vehiclenumber)
        user_set.accountuser = str(accountuser)

        # bg_thread = threading.Thread(target=thread_cbck, args=(user_set,))
        # bg_thread.start()
        logging.debug("Thread Started")
        timer_entity = Timer(int(DEF_TIMER_VALUE), timerexpired_callback, (user_set,))
        timer_entity.setName(str(vehiclenumber))
        timer_entity.start()
    # key = self.request.get('key')
    # def txn():
    # counter = Counter.get_by_key_name(key)
    # if counter is None:
    # counter = Counter(key_name=key, count=1)
    # else:
    # counter.count += 1
    # counter.put()
    # db.run_in_transaction(txn)


def thread_cbck(*args, **kwargs): # should run at most 1/s
    # timercount = self.request.get('timercount')
    # vehiclenumber = self.request.get('vehiclenumber')
    # accountuser = self.request.get('accountuser')
    user_set = timerset_class()
    # user_set.timercount = int(timercount)
    # user_set.vehiclenumber = str(vehiclenumber)
    # user_set.accountuser = str(accountuser)
    user_set.timercount = int(args[0].timercount)
    user_set.vehiclenumber = str(args[0].vehiclenumber)
    user_set.accountuser = str(args[0].accountuser)
    timer_entity = Timer(int(DEF_TIMER_VALUE), timerexpired_callback, (user_set,))
    timer_entity.setName(str(user_set.vehiclenumber))
    timer_entity.start()
    logging.debug("Thread Timer Started")


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

app = webapp2.WSGIApplication([
('/worker', backgroundthread_cbck),
])