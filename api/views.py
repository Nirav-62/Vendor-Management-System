from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import PurchaseOrder,Vendor
from api.serializers import VendorSerializer,PurchaseOrderSerializer
from django.db.models import Q
from django.utils import timezone

class VendorAPI(APIView):

    def get(self, request, vendor_id=None, format=None):
        if vendor_id is not None:
            try:
                vendor = get_object_or_404(Vendor, pk=vendor_id)
                serializer = VendorSerializer(vendor)
                return Response(serializer.data)
            except Http404:
                return Response('Vendor Not Exists')

        query_set = Vendor.objects.all()
        serializer = VendorSerializer(query_set, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, vendor_id=None, format=None):
        # Restore authentication settings for secure methods

        if vendor_id is not None:
            try:
                vendor = get_object_or_404(Vendor, pk=vendor_id)
                req_api_key = request.data['api_key']

                if  req_api_key:
                   
                    if req_api_key == str(vendor.api_key):
    
                        serializer = VendorSerializer(vendor, data=request.data)
                        if serializer.is_valid():
                            serializer.save()
                            response_data = {
                                'message': 'Vendor updated successfully',
                                'data': serializer.data,
                            }
                            return Response(response_data)
                        
                        else:
                              return Response(serializer.errors)
                        
                    else:
                         response_data = {
                                'message': 'Please Enter Correct token or api_key values',
                                
                            }
                         return Response(response_data)
                   

            except Http404:

                return Response('Vendor Not Exists')
            
            except KeyError:

                response_data = {
                                'message' : 'Please Enter Provide api_key in request body for secure access',
                                'help' : 'To Obtain Your api_key hit this url api/obtain_keys/Your Id/  Id is Vender_codes  number part after V- ',
                                 }
                return Response(response_data)
            
        else:
                 return Response('Vendor ID not given')

    def delete(self, request, vendor_id=None, format=None):
        # Restore authentication settings for secure methods
       
        if id is not None:
            try:
                vendor = get_object_or_404(Vendor, pk=vendor_id)
                req_api_key = request.headers.get('apikey')
                print(req_api_key)
                if  req_api_key:
                   
                    if req_api_key == str(vendor.api_key):
                        vendor.delete()
                        return Response({'success':'Vendor Deleted successfully'},status=status.HTTP_200_OK)
                    

                    else:
                         response_data = {
                                'message': 'Please Enter Correct token or api_key values',
                                
                            }
                         return Response(response_data)
                else:
                    response_data = {
                                'message' : 'Please  Provide api_key in request header key=apikey value=your api key for secure access',
                                'help' : 'To Obtain Your api_key hit this url api/obtain_keys/Your Id/  Id is Vender_codes  number part after V- ',
                                 }
                    return Response(response_data)
                    
            except Http404:

                return Response({'Error':'Vendor Not Exists'},status=status.HTTP_404_NOT_FOUND)
            
            except KeyError:
                
                response_data = {
                                'message' : 'Please  Provide api_key for secure access',
                                'help' : 'To Obtain Your api_key hit this url api/obtain_keys/Your Id/  Id is Vender_codes  number part after V- ',
                                 }
                return Response(response_data)
            
        else:
            return Response({'Error':'Vendor ID not given'},status=status.HTTP_400_BAD_REQUEST)
        
 
 
@api_view(['GET'])        # this function is for obtain api key for particular user if user sends request for it than it returns key.
def obtain_key(request, vendor_id):
    try:
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        serializer = VendorSerializer(vendor)
        response_data = {
            'vendor' : serializer.data.get('name'),
            'api_key': serializer.data.get('api_key', None),
        }
        return Response(response_data)
    except Http404:
        return Response({'error': 'Vendor Not Exists With Given Id'}, status=404)
    
    
class PurchaseOrderAPI(APIView):

    def get(self, request,po_id=None,format=None):
        filter_vendor = request.query_params.get('vendor_id') # this is for  list all purchase orders with an option to filter by vendor 
        if filter_vendor:
            po_data = PurchaseOrder.objects.filter(vendor = filter_vendor)
            if po_data:
                serializer = PurchaseOrderSerializer(po_data , many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                response_data={
                    'message':'No data found for given Vendor id'
                }
                return Response(response_data)
        if po_id is not None:

            try:
                query_set = get_object_or_404(PurchaseOrder,po_number = po_id)
                serializer = PurchaseOrderSerializer(query_set)
                return Response(serializer.data , status=status.HTTP_200_OK)
            except Http404:
                    return Response('Purchase Order Not Exists with given Purchase Order Number')


        query_set = PurchaseOrder.objects.all()      
        serializer = PurchaseOrderSerializer(query_set , many = True)
        return Response(serializer.data , status=status.HTTP_200_OK)

    def post(self, request, format=None):
            try:
    
                req_api_key = request.data['api_key']
                req_vendor = request.data['vendor']
                vendor = Vendor.objects.get(pk=req_vendor)
                # items = request.data['items']
                # l=[item for item in request.data['items']] 
                # print(len(l))
                if  req_api_key:
                   
                    if req_api_key == str(vendor.api_key):
                        serializer = PurchaseOrderSerializer(data=request.data)
                        if serializer.is_valid():
                            serializer.save()
                        
                            response_data = {
                                    'message': 'Purchase Order Created successfully',
                                    'data' : serializer.data,
                                }
                            return Response(response_data,status=status.HTTP_201_CREATED)
                        else:
                            return Response(serializer.errors)
                        
                        
                    else:
                         response_data = {
                                'message': 'Please Enter Correct token or api_key values',
                                
                            }
                         return Response(response_data)
                   

           
            except KeyError:

                response_data = {
                                'message' : 'Please Enter Provide api_key in request body for secure access',
                                'help' : 'To Obtain Your api_key hit this url api/obtain_keys/Your Id/  Id is Vender_codes  number part after V- ',
                                 }
                return Response(response_data)
            
    def put(self , request , po_id = None , format = None):

            try:
    
                req_api_key = request.data['api_key']
                req_vendor = request.data['vendor']
                vendor = get_object_or_404(Vendor, pk=req_vendor)
                p_order = get_object_or_404(PurchaseOrder, po_number = po_id)

                if  req_api_key:
                   
                    if req_api_key == str(vendor.api_key):
                        serializer = PurchaseOrderSerializer(p_order , data=request.data)
                        if serializer.is_valid():
                            serializer.save()
                        
                            response_data = {
                                    'message': 'Purchase Order Updated successfully',
                                    'data' : serializer.data,
                                }
                            return Response(response_data,status=status.HTTP_201_CREATED)
                        else:
                            return Response(serializer.errors)
                        
                        
                    else:
                         response_data = {
                                'message': 'Please Enter Correct token or api_key values',
                                
                            }
                         return Response(response_data)
                   
            except Http404:

                return Response('Purchase Order Not Exists')
           
            except KeyError:

                response_data = {
                                'message' : 'Please Enter Provide api_key in request body for secure access',
                                'help' : 'To Obtain Your api_key hit this url api/obtain_keys/Your Id/  Id is Vender_codes  number part after V- ',
                                 }
                return Response(response_data)
            
    def patch(self , request ,po_id = None , format = None): # want to update any particular field not all than this patch request is used 

            try:
    
                req_api_key = request.data['api_key']
                req_vendor = request.data['vendor']
                vendor = get_object_or_404(Vendor, pk=req_vendor)
                p_order = get_object_or_404(PurchaseOrder, po_number = po_id)

                if  req_api_key:
                   
                    if req_api_key == str(vendor.api_key):
                        serializer = PurchaseOrderSerializer(p_order , data=request.data)
                        if serializer.is_valid():
                            serializer.save()
                        
                            response_data = {
                                    'message': 'Purchase Order Updated successfully',
                                    'data' : serializer.data,
                                }
                            return Response(response_data,status=status.HTTP_201_CREATED)
                        else:
                            return Response(serializer.errors)
                        
                        
                    else:
                         response_data = {
                                'message': 'Please Enter Correct token or api_key values',
                                
                            }
                         return Response(response_data)
                   
            except Http404:

                return Response('Purchase Order Not Exists')
           
            except KeyError:

                response_data = {
                                'message' : 'Please Enter Provide api_key in request body for secure access',
                                'help' : 'To Obtain Your api_key hit this url api/obtain_keys/Your Id/  Id is Vender_codes  number part after V- ',
                                 }
                return Response(response_data)   
    
            
    def delete (self , request , po_id = None ,format = None):
        
        try:
            if po_id is not None:
            
                
                p_order = get_object_or_404(PurchaseOrder, po_number = po_id)
                po_vendor=PurchaseOrder.objects.get(Q(po_number = po_id) & Q(vendor = p_order.vendor)) 
                req_api_key = request.headers.get('apikey')
                # print(req_api_key)
                if  req_api_key:
                   
                    if req_api_key == str(po_vendor.vendor.api_key):
                        p_order.delete()
                        return Response({'success':'Purchase Order Deleted successfully'},status=status.HTTP_200_OK)
                    

                    else:
                         response_data = {
                                'message': 'Please Enter Correct token or api_key values',
                                
                            }
                         return Response(response_data)
                else:
                    response_data = {
                                'message' : 'Please  Provide api_key in request header key=apikey value=your api key for secure access',
                                'help' : 'To Obtain Your api_key hit this url api/obtain_keys/Your Id/  Id is Vender_codes  number part after V- ',
                                 }
                    return Response(response_data)
            else:
                  return Response({'Error':'Purchase Order ID not given'},status=status.HTTP_400_BAD_REQUEST)
        
        except Http404:

                return Response({'Error':'Purchase Order Not Exists'},status=status.HTTP_404_NOT_FOUND)
        except KeyError:
                
            response_data = {
                                'message' : 'Please  Provide api_key for secure access',
                                'help' : 'To Obtain Your api_key hit this url api/obtain_keys/Your Id/  Id is Vender_codes  number part after V- ',
                                 }
            return Response(response_data)
@api_view(['POST'])       
def PurchaseOrderAcknowledge(request , po_id = None):    # this for vendors to acknowledge POs.

    if po_id is not None:
        try:
            po = get_object_or_404(PurchaseOrder , po_number = po_id)
            po.acknowledgment_date = timezone.now()
            po.save()
            return Response({'Success':'PurchaseOrder Acknowledge Successfully'})
        except Http404:
            return Response({'Error':'PurchaseOrder not found '})

    else:
        response_data = {
            'error':'Purchase Order id is not given'
        }
        return Response(response_data)
@api_view(['GET'] )
def showPerformance(request,vendor_id = None):
    if vendor_id is not None:
        try:
            po = get_object_or_404(Vendor , pk = vendor_id)
            serializer = VendorSerializer(po)
            Response_data={
                
                    "Name" :serializer.data['name'],
                    "On_time_Delivery_Rate" :serializer.data['on_time_delivery_rate'],
                    "Quality_Rating_Avg" :serializer.data['quality_rating_avg'],
                    "Average_Response_Time" :serializer.data['average_response_time'],
                    "Fulfillment_Rate" :serializer.data['fulfillment_rate']

            }
            
            return Response(Response_data,status=status.HTTP_200_OK)
        except Http404:
            return Response({'Error':'Vendor not found '})

    else:
        response_data = {
            'error':'Vendor  id is not given'
        }
        return Response(response_data)