# shopify-csv-order-profit
A simple python program to calculate the profit of operating a contact lens shop on Shopify.

## How it works?
Get the order csv file from shopify, this python will start to parse the csv into Shopify Object.
After connecting to my own MongoDB, which contains the cost of our own product. 
We can start to calculate the profit.
*on main python program, predefined the using S.F. Express for product shipping and the cost of shipping are $30 HKD to Hong Kong and $37 HKD to Macau.
*for our Shopify Payment Charges, our paln is 3.3% for local cards and 3.9% for foreign cards. +2.35 HKD shopify extra charges.

## Customized Logic
Be aware of in our Shopify Shop, we configured the custom payment as PayMe or FPS to enjoy $5 HKD discount.

## Usage
1. Export the order csv file from Shopify
2. Put the csv file into csv folder
3. Configure the csv filename on profit.py
4. Configure the mongoDB url on profit.py
5. Define your own product cost method on cost_table() method
6. Run main program profit.py

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
