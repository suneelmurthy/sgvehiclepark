"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""


import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
import config.models
import config.sgvehiclepark as sg

package="Registration"



class User(messages.Message):
    nric = messages.StringField(1)
    password = messages.StringField(1)

class NewUserRequest(messages.Message):
  message = messages.StringField(1)

class NewUserResponse(messages.Message):
  items = messages.MessageField(NewUserRequest, 1, repeated=True)

USER_RESPONSE = NewUserResponse(items=[])

MULTIPLY_METHOD_RESOURCE = endpoints.ResourceContainer(
    User
    )

@endpoints.api(name='user', version='v1')
class VehicleUsersApi(remote.Service):

  @endpoints.method(MULTIPLY_METHOD_RESOURCE, NewUserResponse,
                    path='adduser', http_method='POST',
                    name='')
  def user_registration(self, request):
    models.Customer_Table(Cust_Nric=request.nric, Cust_Handphone=request.handPhone, Cust_password  = request.password)
    models.Customer_Table.get_or_insert()

  sg.start("");
  ID_RESOURCE = endpoints.ResourceContainer(
      message_types.VoidMessage,
      id=messages.IntegerField(1, variant=messages.Variant.INT32))

  @endpoints.method(ID_RESOURCE, User,
                    path='user/{id}', http_method='GET',
                    name='getUser')
  def get_user(self, request):
    try:
      return User("Venkatesh")
    except (IndexError, TypeError):
      raise endpoints.NotFoundException('User %s not found.' %
                                        (request.id,))

@endpoints.api(name='user', version='v1')
class ParkingApi(remote.Service):

  @endpoints.method(MULTIPLY_METHOD_RESOURCE, NewUserResponse,
                    path='startParking', http_method='POST',
                    name='')
  def start_parking(self, request):
    return NewUserResponse("Hi there...")

  ID_RESOURCE = endpoints.ResourceContainer(
      message_types.VoidMessage,
      id=messages.IntegerField(1, variant=messages.Variant.INT32))

  @endpoints.method(ID_RESOURCE, User,
                    path='user/{id}', http_method='GET',
                    name='getUser')
  def stop_parking(self, request):
    try:
      return User("Venkatesh")
    except (IndexError, TypeError):
      raise endpoints.NotFoundException('User %s not found.' %
                                        (request.id,))



APPLICATION = endpoints.api_server([VehicleUsersApi, ParkingApi])