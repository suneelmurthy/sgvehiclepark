#  *************************************************************************
#  *
#  * Vps Pte Ltd, Singapore
#  * __________________
#  *
#  *  [2015] - [2015] Vps Pte Ltd Incorporated
#  *  All Rights Reserved.
#  *
# @(#)File:           urls.py$
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
# | 2015/07/26, 1.0  | Suneel N. G.				| Addition of URL References for API's	|
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

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'query$', 'config.sgvehiclepark.query'), #ending with url pattern should be used

    url(r'sgvpNewUserRegister', 'config.sgvehiclepark.sgvpnewuserregister'), #New User Registration
    url(r'sgvpUpdateUserInfo', 'config.sgvehiclepark.sgvpupdateuserinfo'), #Edit/Modify User Information
    url(r'sgvpDeleteUser', 'config.sgvehiclepark.sgvpsdeleteuser'), #Stop parking coupon
    url(r'sgvpUserAuthentication', 'config.sgvehiclepark.sgvpuserauthentication'), #User sign in
    url(r'sgvpUserTransactionHistory', 'config.sgvehiclepark.sgvpusertransactionhistory'), #User transaction history

    url(r'sgvpUpdateCreditCardInfo', 'config.sgvehiclepark.sgvpupdatecreditcardinfo'), #Add/Modify Creditcard Information
    url(r'sgvpDeleteCreditCard', 'config.sgvehiclepark.sgvpdeletecreditcard'), #Add/Modify Creditcard Information

    url(r'sgvpNewVehicleRegister', 'config.sgvehiclepark.sgvpnewvehicleregister'), #Add/Modify Vehicle Information
    url(r'sgvpDeleteVehicle', 'config.sgvehiclepark.sgvpdeletevehicle'), #Add/Modify Vehicle Information

    url(r'sgvpStartCoupon', 'config.sgvehiclepark.sgvpstartcoupon'), #Start parking coupon
    url(r'sgvpRenewCoupon', 'config.sgvehiclepark.sgvprenewcoupon'), #Renew parking coupon
    url(r'sgvpStopCoupon', 'config.sgvehiclepark.sgvpstopcoupon'), #Stop parking coupon

    url(r'sgvpUpdateCurrency', 'config.sgvehiclepark.sgvpupdatecurrency'), #Add currency to the account
    url(r'sgvpReadCurrency', 'config.sgvehiclepark.sgvpreadcurrency'), #Add currency to the account


    url(r'sgvptestuser', 'config.sgvehiclepark.sgvptestuser'), #Stop parking coupon
    url(r'sgvptestcard', 'config.sgvehiclepark.sgvptestcard'), #Stop parking coupon
)
