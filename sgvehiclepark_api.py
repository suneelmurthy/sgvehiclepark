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
class sgvpUserTransactionHistoryRequestMsg(messages.Message):
    Cust_FirstName = messages.StringField(1)
    Cust_LastName = messages.IntegerField(3)
    Cust_Email = messages.StringField(2)

class sgvpUserTransactionHistoryResponseMsg(messages.Message):
    ResponseMsg = messages.StringField(1)


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


# sgvpReadCurrency
class sgvpReadCurrencyRequestMsg(messages.Message):
    Cust_Nric = messages.StringField(1)

class sgvpReadCurrencyResponseMsg(messages.Message):
    ResponseMsg = messages.StringField(1)
    Amount = messages.IntegerField(2)


ID_RESOURCE = endpoints.ResourceContainer(
              message_types.VoidMessage,
              id=messages.StringField(1))

# *************************************************************************
#  Container parameter definition section
# *************************************************************************
SGVPNEWUSERREGISTER_REQCONTAINER = endpoints.ResourceContainer(
    sgvpNewUserRegisterRequestMsg
    )

SGVPUPDATEUSERINFO_REQCONTAINER = endpoints.ResourceContainer(
    sgvpUpdateUserInfoRequestMsg
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

SGVPREADCURRENCY_REQCONTAINER = endpoints.ResourceContainer(
    sgvpReadCurrencyRequestMsg
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
# *************************************************************************



# ----------------------------------------------------------------------------------------
#  Application definitions
# ----------------------------------------------------------------------------------------
APPLICATION = endpoints.api_server([ParkingUsersApi, ParkingCouponsApi])


# ----------------------------------------------------------------------------------------