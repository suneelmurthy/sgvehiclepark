#  *************************************************************************
#  *
#  * Vps Pte Ltd, Singapore
#  * __________________
#  *
#  *  [2015] - [2015] Vps Pte Ltd Incorporated
#  *  All Rights Reserved.
#  *
# @(#)File:           $sgvehiclepark_api.py$
# @(#)Version:        $1.0$
# @(#)Last changed:   $Date: 2015/08/08 01:33:00 $
# @(#)Purpose:        This file contains the google end point api function handling.
#                     This shall call the methods defined in file sgvehiclepark.py
# @(#)Author:         Suneel N.G.
# @(#)Copyright:      (C) Vps Pte Ltd 2015
# ----------------------------------------------------------------------------------------
# | Version Number   |  		User   			|    			Changes made 			|
# ----------------------------------------------------------------------------------------
# |                  |              			|                           			|
# ----------------------------------------------------------------------------------------
# | 2015/08/16, 1.0  | Suneel N. G.				| API's definitions                 	|
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
import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
import config.models
import config.sgvehiclepark
import json

# ----------------------------------------------------------------------------------------
#  Package definitions
# ----------------------------------------------------------------------------------------
package="Registration"


# ----------------------------------------------------------------------------------------
#  Container parameter definition section
# ----------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------
#  End Points Definition
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
#  Account Related Api's
#  The Account API Endpoint shall include the following API's
#  1) sgvpNewUserRegister
#  2) sgvpUpdateUserInfo
#  3) sgvpDeleteUser
#  4) sgvpUserAuthentication
#  5) sgvpUserTransactionHistory
#  6) sgvpUpdateCreditCardInfo
#  7) sgvpDeleteCreditCard
#  8) sgvpNewVehicleRegister
#  9) sgvpDeleteVehicle
#  10) sgvpReadCurrency
#  11) sgvpUserCheck
# ----------------------------------------------------------------------------------------

# *************************************************************************
# Class Definition
# *************************************************************************
# sgvpNewUserRegister
class sgvpNewUserRegisterRequestMsg(messages.Message):
    Cust_Nric = messages.StringField(1)
    Cust_Handphone = messages.IntegerField(2)
    Cust_Password = messages.StringField(3)

class sgvpNewUserRegisterResponseMsg(messages.Message):
    ResponseMsg = messages.StringField(1)

# sgvpGetUserInfo
class sgvpVehicleTable(messages.Message):
    Veh_Regnumber = messages.StringField(1)
    Veh_Type = messages.StringField(2)
    Veh_Chassisnumber = messages.StringField(3)
    Veh_Enginenumber = messages.StringField(4)

class sgvpGetUserInfoRequestMsg(messages.Message):
    Cust_Nric = messages.StringField(1)

class sgvpGetUserInfoResponseMsg(messages.Message):
    ResponseMsg = messages.StringField(1)
    Cust_Nric = messages.StringField(2)
    Cust_Handphone = messages.IntegerField(3)
    Cust_Amount = messages.FloatField(4)
    Cust_FirstName = messages.StringField(5)
    Cust_LastName = messages.StringField(6)
    Cust_Email = messages.StringField(7)
    Cust_Vehicle = messages.MessageField(sgvpVehicleTable,8,repeated=True)

# sgvpUpdateUserInfo
class sgvpUpdateUserInfoRequestMsg(messages.Message):
    Cust_Nric = messages.StringField(1)
    Cust_FirstName = messages.StringField(2)
    Cust_LastName = messages.StringField(3)
    Cust_Email = messages.StringField(4)

class sgvpUpdateUserInfoResponseMsg(messages.Message):
    ResponseMsg = messages.StringField(1)


# sgvpDeleteUser
class sgvpDeleteUserRequestMsg(messages.Message):
    Cust_Nric = messages.StringField(1)
    Cust_Password = messages.StringField(2)

class sgvpDeleteUserResponseMsg(messages.Message):
    ResponseMsg = messages.StringField(1)


# sgvpUserAuthentication
class sgvpUserAuthenticationRequestMsg(messages.Message):
    Cust_Nric = messages.StringField(1)
    Cust_Password = messages.StringField(2)

class sgvpUserAuthenticationResponseMsg(messages.Message):
    ResponseMsg = messages.StringField(1)


# sgvpUserTransactionHistory
class sgvpTransactionHistoryTable(messages.Message):
    Date = messages.StringField(1)
    Regnumber = messages.StringField(2)
    Amount = messages.StringField(3)
    Nric = messages.StringField(4)
    Starttime = messages.StringField(5)
    Stoptime = messages.StringField(6)
    Stopduration = messages.StringField(7)
    Location = messages.StringField(8)

class sgvpUserTransactionHistoryRequestMsg(messages.Message):
    Cust_Nric = messages.StringField(1)

class sgvpUserTransactionHistoryResponseMsg(messages.Message):
    ResponseData = messages.MessageField(sgvpTransactionHistoryTable,1,repeated = True)
    ResponseMsg = messages.StringField(2)

# sgvpTransactionHistory
class sgvpTransactionHistoryResponseMsg(messages.Message):
    ResponseData = messages.MessageField(sgvpTransactionHistoryTable,1,repeated = True)
    ResponseMsg = messages.StringField(2)



# sgvpUpdateCreditCardInfo
class sgvpUpdateCreditCardInfoRequestMsg(messages.Message):
    Cust_Nric = messages.StringField(1)
    Card_Number = messages.IntegerField(2)
    Card_Name = messages.StringField(3)
    Card_Expiry = messages.StringField(4)

class sgvpUpdateCreditCardInfoResponseMsg(messages.Message):
    ResponseMsg = messages.StringField(1)


# sgvpDeleteCreditCard
class sgvpDeleteCreditCardRequestMsg(messages.Message):
    Cust_Nric = messages.StringField(1)
    Card_Number = messages.IntegerField(2)

class sgvpDeleteCreditCardResponseMsg(messages.Message):
    ResponseMsg = messages.StringField(1)


# sgvpNewVehicleRegister
class sgvpNewVehicleRegisterRequestMsg(messages.Message):
    Cust_Nric = messages.StringField(1)
    Veh_Regnumber = messages.StringField(2)
    Veh_Type = messages.StringField(3)
    Veh_Chassisnumber = messages.StringField(4)
    Veh_Enginenumber = messages.StringField(5)

class sgvpNewVehicleRegisterResponseMsg(messages.Message):
    ResponseMsg = messages.StringField(1)


# sgvpDeleteVehicle
class sgvpDeleteVehicleRequestMsg(messages.Message):
    Cust_Nric = messages.StringField(1)
    Veh_Regnumber = messages.StringField(2)

class sgvpDeleteVehicleResponseMsg(messages.Message):
    ResponseMsg = messages.StringField(1)

# sgvpReadVehicle
class sgvpReadVehicleTable(messages.Message):
    Veh_Regnumber = messages.StringField(2)
    Veh_Type = messages.StringField(3)
    Veh_Chassisnumber = messages.StringField(4)
    Veh_Enginenumber = messages.StringField(5)

class sgvpReadVehicleRequestMsg(messages.Message):
    Cust_Nric = messages.StringField(1)

class sgvpReadVehicleResponseMsg(messages.Message):
    ResponseMsg = messages.StringField(1)
    ResponseData = messages.MessageField(sgvpReadVehicleTable,2,repeated=True)

# sgvpReadCurrency
class sgvpReadCurrencyRequestMsg(messages.Message):
    Cust_Nric = messages.StringField(1)

class sgvpReadCurrencyResponseMsg(messages.Message):
    ResponseMsg = messages.StringField(1)
    Amount = messages.FloatField(2)


# sgvpUserCheck
class sgvpUserCheckRequestMsg(messages.Message):
    Cust_Nric = messages.StringField(1)

class sgvpUserCheckResponseMsg(messages.Message):
    ResponseMsg = messages.StringField(1)


# *************************************************************************
#  Container parameter definition section
# *************************************************************************
SGVPNEWUSERREGISTER_REQCONTAINER = endpoints.ResourceContainer(
    sgvpNewUserRegisterRequestMsg
    )

SGVPUPDATEUSERINFO_REQCONTAINER = endpoints.ResourceContainer(
    sgvpUpdateUserInfoRequestMsg
    )

SGVPGETUSERINFO_REQCONTAINER = endpoints.ResourceContainer(
    sgvpGetUserInfoRequestMsg
    )

SGVPDELETEUSER_REQCONTAINER = endpoints.ResourceContainer(
    sgvpDeleteUserRequestMsg
    )

SGVPUSERAUTHENTICATION_REQCONTAINER = endpoints.ResourceContainer(
    sgvpUserAuthenticationRequestMsg
    )

SGVPUSERTRANSACTIONHISTORY_REQCONTAINER = endpoints.ResourceContainer(
    sgvpUserTransactionHistoryRequestMsg
    )

SGVPUPDATECREDITCARDINFO_REQCONTAINER = endpoints.ResourceContainer(
    sgvpUpdateCreditCardInfoRequestMsg
    )

SGVPDELETECREDITCARD_REQCONTAINER = endpoints.ResourceContainer(
    sgvpDeleteCreditCardRequestMsg
    )

SGVPNEWVEHICLEREGISTER_REQCONTAINER = endpoints.ResourceContainer(
    sgvpNewVehicleRegisterRequestMsg
    )

SGVPDELETEVEHICLE_REQCONTAINER = endpoints.ResourceContainer(
    sgvpDeleteVehicleRequestMsg
    )

SGVPREADVEHICLE_REQCONTAINER = endpoints.ResourceContainer(
    sgvpReadVehicleRequestMsg
    )

SGVPREADCURRENCY_REQCONTAINER = endpoints.ResourceContainer(
    sgvpReadCurrencyRequestMsg
    )

SGVPUSERCHECK_REQCONTAINER = endpoints.ResourceContainer(
    sgvpUserCheckRequestMsg
    )

SGVPUSERTRANSACTIONHISTORY_REQCONTAINER = endpoints.ResourceContainer(
    sgvpUserTransactionHistoryRequestMsg
    )

# *************************************************************************
#  API Definitions
# *************************************************************************
@endpoints.api(name='parkingusersapi', version='v1')
class ParkingUsersApi(remote.Service):

    # ******************************************************************* #
    # Method sgvpNewUserRegister
    # ******************************************************************* #
    @endpoints.method(SGVPNEWUSERREGISTER_REQCONTAINER, sgvpNewUserRegisterResponseMsg,
                      path='', http_method='POST',
                      name='sgvpNewUserRegister')

    # Method Definition
    def sgvpNewUserRegister(self, request):
        response = sgvpNewUserRegisterResponseMsg()
        msg = config.sgvehiclepark.sgvpnewuserregister(request)
        response.ResponseMsg = msg
        return response
    # ******************************************************************* #


    # ******************************************************************* #
    # Method sgvpGetUserInfo
    # ******************************************************************* #
    @endpoints.method(SGVPGETUSERINFO_REQCONTAINER, sgvpGetUserInfoResponseMsg,
                      path='', http_method='POST',
                      name='sgvpGetUserInfo')

    # Method Definition
    def sgvpGetUserInfo(self, request):
        response = sgvpGetUserInfoResponseMsg()
        response_msg = config.sgvehiclepark.sgvpgetuserinfo(request)

        if not response_msg:
            # No valid entry found
            response.ResponseMsg = "Invalid User"
        else:
            # Valid entry found
            response.ResponseMsg = "Data Found"
            response.Cust_Nric = response_msg.Cust_Nric
            response.Cust_Handphone = response_msg.Cust_Handphone
            response.Cust_Amount = response_msg.Cust_Amount
            response.Cust_FirstName = response_msg.Cust_FirstName
            response.Cust_LastName = response_msg.Cust_LastName
            response.Cust_Email = response_msg.Cust_Email
            for each_veh in response_msg.Cust_Vehicle:
                vehicle_data = sgvpVehicleTable()
                vehicle_data.Veh_Chassisnumber = str(each_veh.Veh_Chassisnumber)
                vehicle_data.Veh_Enginenumber = str(each_veh.Veh_Enginenumber)
                vehicle_data.Veh_Regnumber = str(each_veh.Veh_Regnumber)
                vehicle_data.Veh_Type = str(each_veh.Veh_Type)
                response.Cust_Vehicle.append(vehicle_data)

        return response
    # ******************************************************************* #


    # ******************************************************************* #
    # Method sgvpUpdateUserInfo
    # ******************************************************************* #
    @endpoints.method(SGVPUPDATEUSERINFO_REQCONTAINER,
                      sgvpUpdateUserInfoResponseMsg,
                      path='', http_method='POST',
                      name='sgvpUpdateUserInfo')
    # ******************************************************************* #
    # Method Definition
    # ******************************************************************* #
    def sgvpUpdateUserInfo(self, request):
        response = sgvpUpdateUserInfoResponseMsg()
        msg = config.sgvehiclepark.sgvpupdateuserinfo(request)
        response.ResponseMsg = msg
        return response


    # ******************************************************************* #
    # Method sgvpDeleteUser
    # ******************************************************************* #
    @endpoints.method(SGVPDELETEUSER_REQCONTAINER,
                      sgvpDeleteUserResponseMsg,
                      path='', http_method='POST',
                      name='sgvpDeleteUser')
    # ******************************************************************* #
    # Method Definition
    # ******************************************************************* #
    def sgvpDeleteUser(self, request):
        response = sgvpDeleteUserResponseMsg()
        msg = config.sgvehiclepark.sgvpsdeleteuser(request)
        response.ResponseMsg = msg
        return response


    # ******************************************************************* #
    # Method sgvpUserAuthentication
    # ******************************************************************* #
    @endpoints.method(SGVPUSERAUTHENTICATION_REQCONTAINER,
                      sgvpUserAuthenticationResponseMsg,
                      path='', http_method='POST',
                      name='sgvpUserAuthentication')
    # ******************************************************************* #
    # Method Definition
    # ******************************************************************* #
    def sgvpDeleteUser(self, request):
        response = sgvpUserAuthenticationResponseMsg()
        msg = config.sgvehiclepark.sgvpuserauthentication(request)
        response.ResponseMsg = msg
        return response


    # ******************************************************************* #
    # Method sgvpUpdateCreditCardInfo
    # ******************************************************************* #
    @endpoints.method(SGVPUPDATECREDITCARDINFO_REQCONTAINER,
                      sgvpUpdateCreditCardInfoResponseMsg,
                      path='', http_method='POST',
                      name='sgvpUpdateCreditCardInfo')
    # ******************************************************************* #
    # Method Definition
    # ******************************************************************* #
    def sgvpUpdateCreditCardInfo(self, request):
        response = sgvpUpdateCreditCardInfoResponseMsg()
        msg = config.sgvehiclepark.sgvpupdatecreditcardinfo(request)
        response.ResponseMsg = msg
        return response


    # ******************************************************************* #
    # Method sgvpDeleteCreditCard
    # ******************************************************************* #
    @endpoints.method(SGVPDELETECREDITCARD_REQCONTAINER,
                      sgvpDeleteCreditCardResponseMsg,
                      path='', http_method='POST',
                      name='sgvpDeleteCreditCard')
    # ******************************************************************* #
    # Method Definition
    # ******************************************************************* #
    def sgvpDeleteCreditCard(self, request):
        response = sgvpDeleteCreditCardResponseMsg()
        msg = config.sgvehiclepark.sgvpdeletecreditcard(request)
        response.ResponseMsg = msg
        return response


    # ******************************************************************* #
    # Method sgvpNewVehicleRegister
    # ******************************************************************* #
    @endpoints.method(SGVPNEWVEHICLEREGISTER_REQCONTAINER,
                      sgvpNewVehicleRegisterResponseMsg,
                      path='', http_method='POST',
                      name='sgvpNewVehicleRegister')
    # ******************************************************************* #
    # Method Definition
    # ******************************************************************* #
    def sgvpNewVehicleRegister(self, request):
        response = sgvpNewVehicleRegisterResponseMsg()
        msg = config.sgvehiclepark.sgvpnewvehicleregister(request)
        response.ResponseMsg = msg
        return response


    # ******************************************************************* #
    # Method sgvpDeleteVehicle
    # ******************************************************************* #
    @endpoints.method(SGVPDELETEVEHICLE_REQCONTAINER,
                      sgvpDeleteVehicleResponseMsg,
                      path='', http_method='POST',
                      name='sgvpDeleteVehicle')
    # ******************************************************************* #
    # Method Definition
    # ******************************************************************* #
    def sgvpDeleteVehicle(self, request):
        response = sgvpDeleteVehicleResponseMsg()
        msg = config.sgvehiclepark.sgvpdeletevehicle(request)
        response.ResponseMsg = msg
        return response


    # ******************************************************************* #
    # Method gvpReadVehicle
    # ******************************************************************* #
    @endpoints.method(SGVPREADVEHICLE_REQCONTAINER,
                      sgvpReadVehicleResponseMsg,
                      path='', http_method='POST',
                      name='sgvpReadVehicle')
    # ******************************************************************* #
    # Method Definition
    # ******************************************************************* #
    def sgvpReadVehicle(self, request):
        response = sgvpReadVehicleResponseMsg()
        response_data = sgvpReadVehicleTable()
        response_msg = config.sgvehiclepark.sgvpreadvehicle(request)

        if not response_msg:
            # No valid entry found
            response.ResponseMsg = "No Vehicles found"
        else:
            # Valid entry found
            response.ResponseMsg = "Vehicle Found"
            for each_msg in response_msg:
                response_data.Veh_Chassisnumber = str(each_msg.Veh_Chassisnumber)
                response_data.Veh_Enginenumber = str(each_msg.Veh_Enginenumber)
                response_data.Veh_Regnumber = str(each_msg.Veh_Regnumber)
                response_data.Veh_Type = str(each_msg.Veh_Type)
                response.ResponseData.append(response_data)
        return response


    # ******************************************************************* #
    # Method sgvpReadCurrency
    # ******************************************************************* #
    @endpoints.method(SGVPREADCURRENCY_REQCONTAINER,
                      sgvpReadCurrencyResponseMsg,
                      path='', http_method='POST',
                      name='sgvpReadCurrency')
    # ******************************************************************* #
    # Method Definition
    # ******************************************************************* #
    def sgvpReadCurrency(self, request):
        response = sgvpReadCurrencyResponseMsg()
        msg = config.sgvehiclepark.sgvpreadcurrency(request)
        data = json.loads(msg)
        response.Amount = data['Amount']
        response.ResponseMsg = data['ResponseMsg']
        return response


    # ******************************************************************* #
    # Method sgvpReadCurrency
    # ******************************************************************* #
    @endpoints.method(SGVPUSERCHECK_REQCONTAINER,
                      sgvpUserCheckResponseMsg,
                      path='', http_method='POST',
                      name='sgvpUserCheck')
    # ******************************************************************* #
    # Method Definition
    # ******************************************************************* #
    def sgvpUserCheck(self, request):
        response = sgvpUserCheckResponseMsg()
        msg = config.sgvehiclepark.sgvpusercheck(request)
        response.ResponseMsg = msg
        return response


    # ******************************************************************* #
    # Method sgvpUserTransactionHistoryRequestMsg
    # ******************************************************************* #
    @endpoints.method(SGVPUSERTRANSACTIONHISTORY_REQCONTAINER,
                      sgvpUserTransactionHistoryResponseMsg,
                      path='', http_method='POST',
                      name='sgvpUserTransactionHistory')
    # ******************************************************************* #
    # Method Definition
    # ******************************************************************* #
    def sgvpUserTransactionHistory(self, request):
        response = sgvpUserTransactionHistoryResponseMsg()
        response_msg = config.sgvehiclepark.sgvpusertransactionhistory(request)

        if not response_msg:
            # No valid entry found
            response.ResponseMsg = "No Valid Data Available"
        else:
            # Valid entry found
            response.ResponseMsg = "Valid Data Available"
            for each_msg in response_msg:
                response_data = sgvpTransactionHistoryTable()
                response_data.Amount = str(each_msg.Trans_Amount)
                response_data.Date = str(each_msg.Trans_Date)
                response_data.Location = str(each_msg.Trans_Location)
                response_data.Nric = str(each_msg.Trans_Nric)
                response_data.Regnumber = str(each_msg.Trans_Regnumber)
                response_data.Starttime = str(each_msg.Trans_Starttime.time())
                response_data.Stoptime = str('Running') if not each_msg.Trans_Stoptime else str(each_msg.Trans_Stoptime.time())
                response_data.Stopduration = str('Running') if not each_msg.Trans_Stopduration else str(each_msg.Trans_Stopduration)
                response.ResponseData.append(response_data)
        return response


    # ******************************************************************* #
    # Method sgvpTransactionHistory
    # ******************************************************************* #
    @endpoints.method(message_types.VoidMessage,
                      sgvpTransactionHistoryResponseMsg,
                      path='', http_method='GET',
                      name='sgvpTransactionHistory')
    # ******************************************************************* #
    # Method Definition
    # ******************************************************************* #
    def sgvpTransactionHistory(self, unused_request):
        response = sgvpTransactionHistoryResponseMsg()
        response_msg = config.sgvehiclepark.sgvptransactionhistory()

        if not response_msg:
            # No valid entry found
            response.ResponseMsg = "No Valid Data Available"
        else:
            # Valid entry found
            response.ResponseMsg = "Valid Data Available"
            for each_msg in response_msg:
                response_data = sgvpTransactionHistoryTable()
                response_data.Amount = str(each_msg.Trans_Amount)
                response_data.Date = str(each_msg.Trans_Date)
                response_data.Location = str(each_msg.Trans_Location)
                response_data.Nric = str(each_msg.Trans_Nric)
                response_data.Regnumber = str(each_msg.Trans_Regnumber)
                response_data.Starttime = str(each_msg.Trans_Starttime.time())
                response_data.Stoptime = str('Running') if not each_msg.Trans_Stoptime else str(each_msg.Trans_Stoptime.time())
                response_data.Stopduration = str('Running') if not each_msg.Trans_Stopduration else str(each_msg.Trans_Stopduration)
                response.ResponseData.append(response_data)
        return response

# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
#  Parking Related Api's
#  The Account API Endpoint shall include the following API's
#  1) sgvpStartCoupon
#  2) sgvpStopCoupon
#  3) sgvpRenewCoupon
# ----------------------------------------------------------------------------------------

# *************************************************************************
# Class Definition
# *************************************************************************
# sgvpStartCoupon
class sgvpStartCouponRequestMsg(messages.Message):
    Cust_Nric = messages.StringField(1)
    Veh_Regnumber = messages.StringField(2)
    Park_Duration = messages.IntegerField(3)
    Park_Coupon = messages.IntegerField(4)
    Park_Loclat = messages.FloatField(5)
    Park_Loclong = messages.FloatField(6)

class sgvpStartCouponResponseMsg(messages.Message):
    ResponseMsg = messages.StringField(1)


# sgvpStopCoupon
class sgvpStopCouponRequestMsg(messages.Message):
    Cust_Nric = messages.StringField(1)
    Veh_Regnumber = messages.StringField(2)

class sgvpStopCouponResponseMsg(messages.Message):
    ResponseMsg = messages.StringField(1)


# sgvpRenewCoupon
class sgvpRenewCouponRequestMsg(messages.Message):
    Cust_Nric = messages.StringField(1)
    Veh_Regnumber = messages.StringField(2)
    Park_Duration = messages.IntegerField(3)
    Park_Coupon = messages.IntegerField(4)

class sgvpRenewCouponResponseMsg(messages.Message):
    ResponseMsg = messages.StringField(1)


# sgvpReadActiveCouponRequestMsg
class sgvpReadActiveCouponRequestMsg(messages.Message):
    Cust_Nric = messages.StringField(1)

class sgvpReadActiveCouponResponseMsg(messages.Message):
    ResponseData = messages.MessageField(sgvpTransactionHistoryTable,1,repeated = True)
    ResponseMsg = messages.StringField(2)

# *************************************************************************
#  Container parameter definition section
# *************************************************************************
SGVPSTARTCOUPON_REQCONTAINER = endpoints.ResourceContainer(
    sgvpStartCouponRequestMsg
    )

SGVPSTOPCOUPON_REQCONTAINER = endpoints.ResourceContainer(
    sgvpStopCouponRequestMsg
    )

SGVPRENEWCOUPON_REQCONTAINER = endpoints.ResourceContainer(
    sgvpRenewCouponRequestMsg
    )

SGVPREADACTIVECOUPON_REQCONTAINER = endpoints.ResourceContainer(
    sgvpReadActiveCouponRequestMsg
    )

# *************************************************************************
#  API Definitions
# *************************************************************************
@endpoints.api(name='parkingcouponsapi', version='v1')
class ParkingCouponsApi(remote.Service):

    # ******************************************************************* #
    # Method sgvpNewUserRegister
    # ******************************************************************* #
    @endpoints.method(SGVPSTARTCOUPON_REQCONTAINER,
                      sgvpStartCouponResponseMsg,
                      path='', http_method='POST',
                      name='sgvpStartCoupon')

    # Method Definition
    def sgvpStartCoupon(self, request):
        response = sgvpStartCouponResponseMsg()
        msg = config.sgvehiclepark.sgvpstartcoupon(request)
        response.ResponseMsg = msg
        return response
    # ******************************************************************* #


    # ******************************************************************* #
    # Method sgvpUpdateUserInfo
    # ******************************************************************* #
    @endpoints.method(SGVPSTOPCOUPON_REQCONTAINER,
                      sgvpStopCouponResponseMsg,
                      path='', http_method='POST',
                      name='sgvpStopCoupon')
    # ******************************************************************* #
    # Method Definition
    # ******************************************************************* #
    def sgvpStopCoupon(self, request):
        response = sgvpStopCouponResponseMsg()
        msg = config.sgvehiclepark.sgvpstopcoupon(request)
        response.ResponseMsg = msg
        return response


    # ******************************************************************* #
    # Method sgvpRenewCoupon
    # ******************************************************************* #
    @endpoints.method(SGVPRENEWCOUPON_REQCONTAINER,
                      sgvpRenewCouponResponseMsg,
                      path='', http_method='POST',
                      name='sgvpRenewCoupon')
    # ******************************************************************* #
    # Method Definition
    # ******************************************************************* #
    def sgvpRenewCoupon(self, request):
        response = sgvpRenewCouponResponseMsg()
        msg = config.sgvehiclepark.sgvprenewcoupon(request)
        response.ResponseMsg = msg
        return response


    # ******************************************************************* #
    # Method sgvpReadActiveCoupon
    # ******************************************************************* #
    @endpoints.method(SGVPREADACTIVECOUPON_REQCONTAINER,
                      sgvpReadActiveCouponResponseMsg,
                      path='', http_method='POST',
                      name='sgvpReadActiveCoupon')
    # ******************************************************************* #
    # Method Definition
    # ******************************************************************* #
    def sgvpReadActiveCoupon(self, request):
        response = sgvpReadActiveCouponResponseMsg()
        response_msg = config.sgvehiclepark.sgvpreadactivecoupon(request)
        if not response_msg:
            # No valid entry found
            response.ResponseMsg = "No Valid Data Available"
        else:
            # Valid entry found
            response.ResponseMsg = "Valid Data Available"
            for each_msg in response_msg:
                response_data = sgvpTransactionHistoryTable()
                response_data.Amount = str(each_msg.Trans_Amount)
                response_data.Date = str(each_msg.Trans_Date)
                response_data.Location = str(each_msg.Trans_Location)
                response_data.Nric = str(each_msg.Trans_Nric)
                response_data.Regnumber = str(each_msg.Trans_Regnumber)
                response_data.Starttime = str(each_msg.Trans_Starttime.time())
                response_data.Stoptime = str('Running') if not each_msg.Trans_Stoptime else str(each_msg.Trans_Stoptime.time())
                response_data.Stopduration = str('Running') if not each_msg.Trans_Stopduration else str(each_msg.Trans_Stopduration)
                response.ResponseData.append(response_data)
        return response


# *************************************************************************



# ----------------------------------------------------------------------------------------
#  Application definitions
# ----------------------------------------------------------------------------------------
APPLICATION = endpoints.api_server([ParkingUsersApi, ParkingCouponsApi])


# ----------------------------------------------------------------------------------------