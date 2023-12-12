#Vendor Management System with Performance Metrics
 
 Welcome to the Vendor Management System (VMS) with Performance Metrics. This system is developed using Django and Django REST Framework and is designed to manage vendor profiles, track purchase orders, and calculate vendor performance metrics.

The Vendor Management System provides the following functionalities:

- **Vendor Management:** Allows you to create, retrieve, update, and delete vendor profiles.

- **Purchase Order Tracking:** Enables you to manage and track purchase orders, including acknowledging orders.

- **Performance Metrics:** Calculates and stores performance metrics for vendors.

## Getting Started
To set up and run the Vendor Management System, follow the steps below.

1. Clone the repository:`git clone <repository-url>` and open in vs code editor.
2. Install Python :`python.org`.
3. Create a virtual environment: `python -m venv venv`
4. Install all dependencies using `pip install -r requirements.txt`.
5. Apply database migrations using `python manage.py migrate`.
6. Create a superuser using `python manage.py createsuperuser`.
7. Run the development server using `python manage.py runserver`.


## API Testing with Postman

[Postman](https://www.postman.com/) is a  API testing tool that makes it easy to test and interact with  APIs.

### Using Postman for API Testing

1. **Install Postman:**
   Download and install Postman from [https://www.postman.com/](https://www.postman.com/).
   Access the API at `http://localhost:8000/api/




## POSTMAN COLLECTION LINK 
`https://api.postman.com/collections/31749598-5838f0ab-a18d-4a6d-8048-34275eab73dc?access_key=PMAT-01HHESF70MB5DZ1H64ME1QSH8T`

`https://api.postman.com/collections/31749598-5838f0ab-a18d-4a6d-8048-34275eab73dc?access_key=PMAT-01HHESF70MB5DZ1H64ME1QSH8T`







## ALL API Endpoints for Vendor.

`GET` `http://localhost:8000/api/vendors/`  

`POST` `http://localhost:8000/api/vendors/`  

`GET` `http://localhost:8000/api/vendors/<int:vendor_id>/`

`PUT` `http://localhost:8000/api/vendors/<int:vendor_id>/`

`DELETE` `http://localhost:8000/api/vendors/<int:vendor_id>/`



##  API Endpoint  for Retrive Performance of specific vendor

`GET` `http://localhost:8000/api/vendors/<int:vendor_id>/performance`


##  API Endpoint for Obtain api key for specific vendor


`GET` `http://localhost:8000/api/obtain_key/<int:vendor_id>/`  



## ALL API Endpoints fOR Purchase Order.

`GET` `http://localhost:8000/api/purchase_orders/? vendor_id="pass vendor id" `

`GET` `http://localhost:8000/api/purchase_orders/`  

`POST` `http://localhost:8000/api/purchase_orders/`  

`GET` `http://localhost:8000/api/purchase_orders/<int:po_id>/`

`PUT` `http://localhost:8000/api/purchase_orders/<int:po_id>/`

`PATCH` `http://localhost:8000/api/purchase_orders/<int:po_id>/`

`DELETE` `http://localhost:8000/api/purchase_orders/<int:po_id>/`

##  API Endpoint for  Purchase Order Acknowledge.


`POST` `http://localhost:8000/api/purchase_orders/<int:po_id>/acknowledge`


## According to Request Change Method of Request

#### Retrieve a Vendor

- **Description**: Get details of a specific vendor.
- **Method**: GET
- **Endpoint**: `http://localhost:8000/api/vendors/<int:vendor_id>/`
- **Parameters**: `vendor_id` (integer) - The ID of the vendor.
- **Response Format**: JSON

#### List Vendors

- **Description**: Get a list of all vendors.
- **Method**: GET
- **Endpoint**: `http://localhost:8000/api/vendors/`
- **Response Format**: JSON

#### Create a Vendor

- **Description**: Create a new vendor.
- **Method**: POST
- **Endpoint**: `http://localhost:8000/api/vendors/`
- **Request Format**: JSON
- **Request Body**: `{ "name": "Vendor Name", "contact_details": "Contact Details", "Address":"Physical address of the vendor." }` sample data
- **Response Format**: JSON

#### Update a Vendor

- **Description**: Update details of a specific vendor.
- **Method**: PUT
- **Endpoint**: `http://localhost:8000/api/vendors/<int:vendor_id>/`
- **Parameters**: `vendor_id` (integer) - The ID of the vendor.
- **Request Format**: JSON
- **Request Body**: `{ "name": "Updated Vendor Name", "contact_details": "Updated Contact Details", "address" :"Updated address","api_key":"api_key of vendor for secure acccess"}`
- **Response Format**: JSON

#### Delete a Vendor

- **Description**: Delete a specific vendor.
- **Method**: DELETE
- **Endpoint**: `http://localhost:8000/api/vendors/<int:vendor_id>/`
- **Parameters**: `vendor_id` (integer) - The ID of the vendor.
- **Request Header**: `{ "apikey" : "apikey of vendor"}`
- **Response Format**: JSON


--------------------------------------------------------------------------------------------------------
### Obtain Vendor Key

#### Obtain API Key

- **Description**: Get the API key for a specific vendor.
- **Method**: GET
- **Endpoint**: `http://localhost:8000/api/obtain_key/<int:vendor_id>/`
- **Parameters**: `vendor_id` (integer) - The ID of the vendor.
- **Response Format**: JSON


--------------------------------------------------------------------------------------------------------


#### Retrive Vendor Performance

- **Description**: Get the Vendor Performance for a specific vendor.
- **Method**: GET
- **Endpoint**:  `http://localhost:8000/api/vendors/<int:vendor_id>/performance`
- **Parameters**: `vendor_id` (integer) - The ID of the vendor.
- **Response Format**: JSON


--------------------------------------------------------------------------------------------------------

#### All purchase orders with an option to filter by vendor
 
- **Description**: Get details of a specific Purchase Order filter by Vendor.
- **Method**: GET
- **Endpoint**: `http://localhost:8000/api/purchase_orders/<int:po_id>/?vendor_id=<Vendor id>`
- **Parameters**: `po_id` (integer) - The ID of the  Purchase Order.
- **Response Format**: JSON


#### Retrieve a Specific Purchase Order

- **Description**: Get details of a specific Purchase Order.
- **Method**: GET
- **Endpoint**: `http://localhost:8000/api/purchase_orders/<int:po_id>/`
- **Parameters**: `po_id` (integer) - The ID of the  Purchase Order.
- **Response Format**: JSON

#### List Purchase Order

- **Description**: Get a list of all Purchase Order.
- **Method**: GET
- **Endpoint**: `http://localhost:8000/api/purchase_orders/`
- **Response Format**: JSON

#### Create a Purchase Order

- **Description**: Create a Purchase Order.
- **Method**: POST
- **Endpoint**: `http://localhost:8000/api/purchase_orders/`
- **Request Format**: JSON
- **Request Body**: `{
    "vendor" : vendor id for whom order is created ,
    "api_key" : vendor api key,
    "items": [  
        {
            "name": "Protin",
            "quantity": 10,
            "price": 500
        },
        {
            "name": "Milk",
            "quantity": 20,
            "price": 50
        }
    ]
}` 
- **Response Format**: JSON

#### Update a Purchase Order.

- **Description**: Update details of a specific Purchase Order.
- **Method**: PUT
- **Endpoint**: `PUT` `http://localhost:8000/api/purchase_orders/<int:po_id>/`
- **Parameters**: `po_id` (integer) - The ID of the Purchase Order.
- **Request Format**: JSON
- **Request Body**: `{
    "vendor" : vendor id for whom order is updated ,
    "api_key" : vendor api key,
    "items": [  
        {
            "name": "Protin",
            "quantity": 50,
            "price": 500
        },
        {
            "name": "Milk",
            "quantity": 20,
            "price": 50
        }
    ],
    "status" : "completed"

}` 
- **Response Format**: JSON

#### Delete a Purchase Order.

- **Description**: Delete a specific Purchase Order.
- **Method**: DELETE
- **Endpoint**: `DELETE` `http://localhost:8000/api/purchase_orders/<int:po_id>/`
- **Parameters**: `po_id` (integer) - The ID of the Purchase Order.
- **Request Header**: `{ "apikey" : "apikey of vendor"}`
- **Response Format**: JSON


https://api.postman.com/collections/31749598-5838f0ab-a18d-4a6d-8048-34275eab73dc?access_key=PMAT-01HHESF70MB5DZ1H64ME1QSH8T
https://api.postman.com/collections/31749598-5838f0ab-a18d-4a6d-8048-34275eab73dc?access_key=PMAT-01HHESF70MB5DZ1H64ME1QSH8T