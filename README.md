# shopify-csv-order-profit
A simple python program to calculate the profit of operating a contact lens shop on Shopify.

## Installation
please install the follow package before execute the main profit.py
```bash
pip install pymongo
```

## How it works?
Get the order csv file from shopify, this python will start to parse the csv into Shopify Object.

After connecting to my own MongoDB, which contains the cost of our own product. 

We can start to calculate the profit.

*on main python program, predefined the using S.F. Express for product shipping and the cost of shipping are $30 HKD to Hong Kong and $37 HKD to Macau.

*for our Shopify Payment Charges, our paln is 3.3% for local cards and 3.9% for foreign cards. +2.35 HKD shopify extra charges.

## Customized Logic
Be aware of in our Shopify Shop, we configured the custom payment as PayMe or FPS to enjoy $5 HKD discount.
```python
if payment == "custom":
    expenses = customer_paid_shipping - discount_amt - refund_amt - shipping_cost - payment_cost
```

## Usage
1. Export the order csv file from Shopify
2. Put the csv file into csv folder
3. Configure the csv filename on profit.py
```python
FILENAME = './csv/orders_export_oct_2020.csv' # [[LOCATION TO PUT YOUR EXPORTED SHOPIFY CSV]]
```
4. Configure the mongoDB url on profit.py
```python
#DEFINE YOUR OWN COST TABLE, I GET IT FROM MY MONGO ATLAS
client = MongoClient(YOUR_MONGO_DB)
```
5. Define your own product cost method on cost_table() method
```python
def cost_table():
    #DEFINE YOUR OWN COST TABLE, I GET IT FROM MY MONGO ATLAS
    client = MongoClient(YOUR_MONGO_DB)
    database = client.YOUR_DATEBASE
    collection = database.Cost 
    results = collection.find()
    cost_dict = {}
    for cost in results:
        sku = cost['sku']
        cost_dict[sku] = cost['cost']

    if len(cost_dict) == 0:
        raise Exception("Cost Table Empty, Please check the connection or database.")

    return cost_dict
```
6. Run main program profit.py

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
