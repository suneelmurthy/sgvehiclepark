#  *************************************************************************
#  *
#  * DisQour Pte Ltd, Singapore
#  * __________________
#  *
#  *  [2015] - [2015] DisQour Pte Ltd Incorporated
#  *  All Rights Reserved.
#  *
# @(#)File:           $models.py$
# @(#)Version:        $4.0$
# @(#)Last changed:   $Date: 2015/07/26 01:33:00 $
# @(#)Purpose:        Update of Header section
# @(#)Author:         Suneel N.G.
# @(#)Copyright:      (C) DisQour Pte Ltd 2015
# ----------------------------------------------------------------------------------------
# | Version Number   |  		User   			|    			Changes made 			|
# ----------------------------------------------------------------------------------------
# |                  |              			|                           			|
# ----------------------------------------------------------------------------------------
# | 2015/07/26, 4.0  | Suneel N. G.				| Update of Header section				|
# ----------------------------------------------------------------------------------------
# | 2015/07/26, 3.0  | Suneel N. G.				| Addition of Block_Table Model			|
# ----------------------------------------------------------------------------------------
#  * DisQour Pte Ltd CONFIDENTIAL
#  * NOTICE:  All information contained herein is, and remains
#  * the property of DisQour Pte Ltd Incorporated and its suppliers,
#  * if any.  The intellectual and technical concepts contained
#  * herein are proprietary to DisQour Pte Ltd Incorporated
#  * and its suppliers and may be covered by Singapore and Foreign Patents,
#  * patents in process, and are protected by trade secret or copyright law.
#  * Dissemination of this information or reproduction of this material
#  * is strictly forbidden unless prior written permission is obtained
#  * from DisQour Pte Ltd Incorporated.
# ----------------------------------------------------------------------------------------


from google.appengine.ext import ndb
import datetime
from google.appengine.ext import db
from google.appengine.api import users

# Create your models here.
# Address_Table
class Address(ndb.Model):
	Add_Type = ndb.StringProperty(required=True) # E.g., 'home', 'delivery'
  	Add_Unit = ndb.StringProperty(required=True)
  	Add_Postalcode = ndb.IntegerProperty(required=True)


# CreditCard_Table
class Creditcard(ndb.Model):
  	Card_Type = ndb.StringProperty(required=True)
  	Card_Name = ndb.StringProperty(required=True)
  	Card_Number = ndb.IntegerProperty(required=True)
  	Card_Expiry = ndb.StringProperty(required=True)

# Customer_Table for Customer Details
class Customer_Table (ndb.Model) :
	Cust_PostalCode = ndb.IntegerProperty(required=True)
	Cust_FirstName = ndb.StringProperty()
	Cust_LastName = ndb.StringProperty()
	Cust_Address = ndb.StructuredProperty(Address, repeated=True)
	Cust_Phone = ndb.StringProperty()
	Cust_Email = ndb.StringProperty()
	Cust_Password = ndb.StringProperty()
	Cust_Creditcard = ndb.StructuredProperty(Creditcard, repeated=True)

# Product_Table for product listing
class Product_Table(ndb.Model):
  	Prd_Productname = ndb.StringProperty(required=True)
  	Prd_Color = ndb.StringProperty()
  	Prd_Unitprice = ndb.IntegerProperty(required=True)
  	Prd_Size = ndb.StringProperty()
	Prd_Weight = ndb.StringProperty()
  	Prd_Color = ndb.StringProperty()
  	Prd_Modelno = ndb.StringProperty(required=True)
  	Prd_Brand = ndb.StringProperty(required=True)
  	Prd_Description = ndb.StringProperty()
  	Prd_Discount = ndb.StringProperty()
  	Prd_Rating = ndb.StringProperty()
  	Prd_Review = ndb.StringProperty()
  	Prd_Stock = ndb.StringProperty()
  	Prd_Category = ndb.StringProperty(required=True)
  	Prd_Categorytype = ndb.StringProperty(required=True)
  	Prd_Image = ndb.BlobProperty()
  	Prd_Minqty = ndb.StringProperty()

# Foodmenu_Table for food listing
class Foodmenu_Table(ndb.Model):
  	Fd_Itemname = ndb.StringProperty(required=True)
  	Fd_Itemcategory = ndb.StringProperty(required=True)
  	Fd_Description = ndb.StringProperty()
	Fd_Servings = ndb.StringProperty()
  	Fd_Size = ndb.StringProperty()
  	Fd_Price = ndb.IntegerProperty()
  	Fd_Image = ndb.BlobProperty()

# Attraction_Table for tourist attraction listing.
class Attraction_Table(ndb.Model):
  	Atn_Name = ndb.StringProperty(required=True)
  	Atn_Category = ndb.StringProperty(required=True)
  	Atn_Description = ndb.StringProperty()
  	Atn_Address = ndb.IntegerProperty(required=True)
  	Atn_Phone = ndb.StringProperty()
	Atn_Email = ndb.StringProperty()
  	Atn_Website = ndb.StringProperty()
  	Atn_Operatinghours = ndb.StringProperty(required=True)
  	Atn_Age = ndb.StringProperty()
  	Atn_Priceadult = ndb.IntegerProperty()
  	Atn_Pricechild = ndb.IntegerProperty()
  	Atn_Pricesenior = ndb.IntegerProperty()
  	Atn_Discount = ndb.IntegerProperty()
  	Atn_Rating = ndb.IntegerProperty()
  	Atn_Image = ndb.BlobProperty()
  	Atn_Ticketsource = ndb.StringProperty(required=True)

# Blockdirectory_Table for details about block (mall/shop)
class Blockdirectory_Table(ndb.Model):
  	Bd_Name = ndb.StringProperty(required=True)
  	Bd_Level = ndb.StringProperty(required=True)
  	Bd_Unit = ndb.StringProperty(required=True)
  	Bd_Description = ndb.StringProperty()
	Bd_Category = ndb.StringProperty()
  	Bd_Phone = ndb.StringProperty()
  	Bd_Website = ndb.StringProperty()
  	Bd_Map = ndb.BlobProperty()
	Bd_Product = ndb.StructuredProperty(Product_Table, repeated=True)

#Cinema_Table
class Cinema_Table(ndb.Model):
  	Cin_Cinema = ndb.StringProperty(required=True)
  	Cin_Moviename = ndb.StringProperty(required=True)
  	Cin_Moviecategory = ndb.StringProperty(required=True)
  	Cin_Description = ndb.StringProperty()
  	Cin_Rating = ndb.IntegerProperty()
	Cin_Showtime = ndb.StringProperty(required=True)
  	Cin_Cinematype = ndb.StringProperty(required=True)
  	Cin_Censorrating = ndb.IntegerProperty(required=True)
  	Cin_Image = ndb.BlobProperty()

#Busstop_Table
class Busstop_Table(ndb.Model):
  	Bst_Number = ndb.StringProperty(required=True)
  	Bst_Name = ndb.StringProperty(required=True)
  	Bst_Position = ndb.GeoPtProperty(required=True)

#Busroute_Table
class Busroute_Table(ndb.Model):
  	Brt_Serviceno = ndb.StringProperty(required=True)
  	Brt_Serviceroute1 = ndb.GeoPtProperty(repeated=True)
  	Brt_Serviceroute2 = ndb.GeoPtProperty(repeated=True)

#Primary Table for Block Details based on Pincode
class Block_Table (ndb.Model) :
	Blk_PostalCode = ndb.IntegerProperty(required=True)
	Blk_Name = ndb.StringProperty()
	Blk_BuildingType = ndb.StringProperty()
	Blk_Description = ndb.StringProperty(required=True)
	Blk_GeoLocation = ndb.GeoPtProperty(required=True)
	Blk_Address = db.StringProperty(multiline=True)
  	Blk_Phone = ndb.StringProperty()
	Blk_Email = ndb.StringProperty()
	Blk_Url = ndb.StringProperty()
	Blk_Image = ndb.BlobProperty()
	Blk_Levels = ndb.StringProperty()
	Blk_Map = ndb.BlobProperty()
	Blk_Size = ndb.StringProperty()
	Blk_Food = ndb.StructuredProperty(Foodmenu_Table, repeated=True)
	Blk_Attraction = ndb.StructuredProperty(Attraction_Table, repeated=True)
	Blk_Cinema = ndb.StructuredProperty(Cinema_Table, repeated=True)


class Mall (db.Model) :
	pinCode = db.StringProperty(required=True)
	location = db.GeoPtProperty()
	address = db.StringProperty(multiline=True)
	contactInfo = db.StringProperty();
	blockType = db.StringProperty()
	category = db.StringProperty()
	#products = db.StructuredProperty(Product, repeated = True)

class Shop(db.Model):
	  name = db.StringProperty(required=True)
	  category = db.StringProperty(required=False)
	  imageUrl = db.StringProperty()
	  address = db.StringProperty(multiline=True)
	  location = db.GeoPtProperty()
	  #products = db.StructuredProperty()

class Product(db.Model):
	  name = db.StringProperty(required=True)
	  category = db.StringProperty(required=False)
	  price = db.FloatProperty()
	  address = db.StringProperty(multiline=True)
	  location = db.GeoPtProperty()
