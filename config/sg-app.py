#  *************************************************************************
#  *
#  * DisQour Pte Ltd, Singapore
#  * __________________
#  *
#  *  [2015] - [2015] DisQour Pte Ltd Incorporated
#  *  All Rights Reserved.
#  *
# @(#)File:           sgvpstest.py$
# @(#)Version:        $4.0$
# @(#)Last changed:   $Date: 2015/07/26 01:33:00 $
# @(#)Purpose:        Addition of Header section
# @(#)Author:         Suneel N.G.
# @(#)Copyright:      (C) DisQour Pte Ltd 2015
# ----------------------------------------------------------------------------------------
# | Version Number   |  		User   			|    			Changes made 			|
# ----------------------------------------------------------------------------------------
# |                  |              			|                           			|
# ----------------------------------------------------------------------------------------
# | 2015/07/26, 4.0  | Suneel N. G.				| Addition of Header section			|
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

PRODUCT_INDEX = "ProductIndex"
SHOP_INDEX = "ShopIndex"
BLOCKTABLE_INDEX = "BlockTableIndex"

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


def readLocation(file):
    with open(file, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        gp=None
        for row in reader :
            gp = db.GeoPt(float(row[0]), float(row[1]))
    return gp

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

def blocktableupdate(request):
    #Variables Definition
     response = http.HttpResponse()
     BlockTableData = []
     index=1
     response.write('Database Update in Progress...')

     #Creating the Index Table
     BlockTableIndex = search.Index(name=BLOCKTABLE_INDEX)
     with open('data/PostalCode/BlockTable.csv', 'rU') as csvfile:
         reader = csv.reader(csvfile)
         for row in reader :
            entry = models.Block_Table(Blk_PostalCode=int(row[0]), Blk_Name=row[1], Blk_BuildingType=row[2], Blk_Description=row[3], Blk_GeoLocation = db.GeoPt(float(row[4]), float(row[5])), Blk_Address = row[6], Blk_Phone = row[7], Blk_Email = row[8], Blk_Url=row[9], Blk_Image=row[10], Blk_Levels=row[11], Blk_Map=row[12], Blk_Size=row[13])
            entry.put()
            BlockTableData.append(search.Document(
            fields=[
                search.TextField(name='Blk_PostalCode', value=row[0]),
                search.TextField(name='Blk_Name', value=row[1]),
                search.TextField(name='Blk_Address', value=row[5]),
                search.TextField(name='Blk_Phone', value=row[6]),
                search.TextField(name='Blk_Email', value=row[7]),
                ]))

            try:
                if index % 200 == 0:
                   print "Commiting index for " + str(index)
                   BlockTableIndex.put(BlockTableData)
                   BlockTableData = []
            except search.Error:
                print "error while indexing.."
            index +=1
         index = 0
     return http.HttpResponse();

def refreshRoute(request):
     r = [];
     with open('data/route2.csv', 'rU') as csvfile:
         reader = csv.reader(csvfile)
         for row in reader :
            r.append({'lat': row[0], 'long' : row[1]});
     root = {
        'data' : r
     };
     data= json.dumps(root)
     return http.HttpResponse(data);

def searchByDistance(user_location):

    index = search.Index(PRODUCT_INDEX)

    #user_location = (-33.857, 151.215)
    query = "distance(location, geopoint(%f, %f)) < %f" % (
        user_location[0], user_location[1], 5000)

    loc_expr = "distance(location, geopoint(%f, %f))" % (
        user_location[0], user_location[1])

    sortexpr = search.SortExpression(
        expression=loc_expr,
        direction=search.SortExpression.ASCENDING, default_value=5001)

    search_query = search.Query(
        query_string=query,
        options=search.QueryOptions(
            sort_options=search.SortOptions(expressions=[sortexpr])))

    results = index.search(search_query)

    return results