***FastAPI: Miscellaneous Notes***
async: signals python function to be run *asynchronously*, i.e. run in the background
* equivalent to Golang go keyword to signal goroutine

**Request Body**
Clients may need to send data to your API - they send this data in a *request body*.  
* Response body - data send from your API to the client.

Use **Pydantic** models to declare a request body.
* Protocols for sending data: POST, PUT, DELETE, PATCH

**Types of parameters**
* Query: parameters appended to the end of the URL path  
    * Ex: items/3?q1=1&q2=2  
* Path: parameters defining the path to which the request is directed  
    * Ex: items/{item_id}  
* Body: parameters expected in the request body

