#  *************************************************************************
#  *
#  * Vps Pte Ltd, Singapore
#  * __________________
#  *
#  *  [2015] - [2015] Vps Pte Ltd Incorporated
#  *  All Rights Reserved.
#  *
# @(#)File:           $models.py$
# @(#)Version:        $1.0$
# @(#)Last changed:   $Date: 2015/08/08 01:33:00 $
# @(#)Purpose:        Addition of database Table Model
# @(#)Author:         Suneel N.G.
# @(#)Copyright:      (C) Vps Pte Ltd 2015
# ----------------------------------------------------------------------------------------
# | Version Number   |  		User   			|    			Changes made 			|
# ----------------------------------------------------------------------------------------
# |                  |              			|                           			|
# ----------------------------------------------------------------------------------------
# | 2015/07/26, 1.0  | Suneel N. G.				| Addition of database Table Model			|
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


from google.appengine.ext import ndb
import datetime
from google.appengine.ext import db
from google.appengine.api import users

# Create your models here.
# Vehicle
class Vehicle(ndb.Model):
	Veh_Regnumber = ndb.StringProperty(required=True)
  Veh_Type = ndb.StringProperty(required=True)
  Veh_Chassisnumber = ndb.StringProperty(required=True)
	Veh_Enginenumber = ndb.StringProperty(required=True)

# CreditCard
class Creditcard(ndb.Model):
  	Card_Name = ndb.StringProperty(required=True)
  	Card_Number = ndb.IntegerProperty(required=True)
  	Card_Expiry = ndb.StringProperty(required=True)

# Transaction
class Transaction(ndb.Model):
  	Trans_Datetime = ndb.DateTimeProperty(required=True)
  	Trans_Type = ndb.StringProperty(required=True)
  	Trans_Regnumber = ndb.StringProperty(required=True)
  	Trans_Chassisnumber = ndb.StringProperty(required=True)
  	Trans_Enginenumber = ndb.StringProperty(required=True)
  	Trans_Duration = ndb.TimeProperty(required=True)
  	Trans_Amount = ndb.IntegerProperty(required=True)

# Customer for Customer Details
class Customer (ndb.Model) :
	Cust_Nric = ndb.StringProperty(required=True)
	Cust_Handphone = ndb.IntegerProperty(required=True)
	Cust_Password = ndb.StringProperty(required=True)
	Cust_Amount = ndb.IntegerProperty(required=True)
	Cust_FirstName = ndb.StringProperty()
	Cust_LastName = ndb.StringProperty()
	Cust_Email = ndb.StringProperty()
	Cust_Creditcard = ndb.StructuredProperty(Creditcard, repeated=True)
	Cust_Vehicle = ndb.StructuredProperty(Vehicle, repeated=True)
	Cust_Transaction = ndb.StructuredProperty(Transaction, repeated=True)

# Product for product listing
class Userpattern(ndb.Model):
  	Usrpat_Datetime = ndb.DateTimeProperty(required=True)
  	Usrpat_Parkingtype = ndb.StringProperty(required=True)
  	Usrpat_Geolocation = ndb.GeoPtProperty(required=True)
  	Usrpat_Duration = ndb.TimeProperty()
	Usrpat_Nric = ndb.StringProperty(required=True)
  	Usrpat_Regnumber = ndb.StringProperty(required=True)

