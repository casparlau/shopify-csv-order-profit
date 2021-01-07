import csv
import pprint
from decimal import Decimal, ROUND_HALF_UP
from pymongo import MongoClient
from model.order import Order
from model.cost import Cost
from model.shopify import Shopify
from model.line_item import LineItem

def get_row_count(filename):
    with open(filename, newline='') as csvfile:
        rows = csv.reader(csvfile)
        total_row_count = 0
        total_row_count = sum(1 for row in rows)
        return total_row_count

# header = ['Name', 'Email', 'Financial Status', 'Paid at', 'Fulfillment Status', 'Fulfilled at', 'Accepts Marketing', 'Currency', 'Subtotal', 'Shipping', 'Taxes', 'Total', 'Discount Code', 'Discount Amount', 'Shipping Method', 'Created at', 'Lineitem quantity', 'Lineitem name', 'Lineitem price', 'Lineitem compare at price', 'Lineitem sku', 'Lineitem requires shipping', 'Lineitem taxable', 'Lineitem fulfillment status', 'Billing Name', 'Billing Street', 'Billing Address1', 'Billing Address2', 'Billing Company', 'Billing City', 'Billing Zip', 'Billing Province', 'Billing Country', 'Billing Phone', 'Shipping Name', 'Shipping Street', 'Shipping Address1', 'Shipping Address2', 'Shipping Company', 'Shipping City', 'Shipping Zip', 'Shipping Province', 'Shipping Country', 'Shipping Phone', 'Notes', 'Note Attributes', 'Cancelled at', 'Payment Method', 'Payment Reference', 'Refunded Amount', 'Vendor', 'Outstanding Balance', 'Employee', 'Location', 'Device ID', 'Id', 'Tags', 'Risk Level', 'Source', 'Lineitem discount', 'Tax 1 Name', 'Tax 1 Value', 'Tax 2 Name', 'Tax 2 Value', 'Tax 3 Name', 'Tax 3 Value', 'Tax 4 Name', 'Tax 4 Value', 'Tax 5 Name', 'Tax 5 Value', 'Phone', 'Receipt Number']
FILENAME = './csv/orders_export_oct_2020.csv' # [[LOCATION TO PUT YOUR EXPORTED SHOPIFY CSV]]
# GATEWAY CHARGES CONSTANT
RATE_SHOPIFY_PAYMENTS_HK = 0.033
RATE_SHOPIFY_PAYMENTS_OTHER = 0.039
RATE_PAYPAL = 0.039
CHARGES_CUSTOM = 5
CHARGES_SHOPIFY_EXTRA = 2.35
# SHIPPING - SF EXPRESS CONSTANT
SHIPPING_SF_HK_COST = 30
SHIPPING_SF_MO_COST = 37
# variables
orders = []
exceptions = []
partially_refunded = []
overseas_orders = []
loss_order = []

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

def csv_parsing(product_cost):
    map_dict = {}
    with open(FILENAME, newline='') as csvfile:
        rows = csv.reader(csvfile)
        current_order = None
        row_count = 0
        for row in rows:
            if row_count == 0:
                row_index = 0
                for key in row:
                    map_dict[key] = row_index
                    row_index += 1
            else:

                order_id = row[map_dict["Name"]].strip()
                financial_status = row[map_dict["Financial Status"]].strip()

                if financial_status == "paid" or financial_status == "partially_refunded":

                    if financial_status == "partially_refunded":
                        partially_refunded.append(Exception("Partially Refunded Order:", order_id))

                    if current_order is not None and current_order.order_id != order_id:
                        orders.append(current_order)

                    sku = row[map_dict["Lineitem sku"]]
                    line_quantity = row[map_dict["Lineitem quantity"]]
                    line_price = Decimal(row[map_dict["Lineitem price"]])
                    line_fulfillment_status = row[map_dict["Lineitem fulfillment status"]]
                    line_cost = product_cost[sku]
                    if line_cost is None:
                        line_cost = 0
                    line_cost =  Decimal(line_cost)
                    line_profit = (line_price - line_cost) * Decimal(line_quantity)

                    line_item = LineItem(order_id
                    , [map_dict["Lineitem name"]]
                    , [sku]
                    , [line_price]
                    , [line_quantity]
                    , line_cost
                    , line_profit)

                    #handle returned product for example #2509
                    line_item_array = [line_item]

                    if line_fulfillment_status == "pending":
                        line_item_array = []
                        line_cost = 0
                        line_profit = 0

                    current_order = Shopify(order_id
                    ,financial_status
                    ,row[map_dict["Shipping"]]
                    ,row[map_dict["Shipping Country"]].strip()
                    ,row[map_dict["Billing Country"]].strip()
                    ,row[map_dict["Refunded Amount"]]
                    ,row[map_dict["Discount Amount"]]
                    ,row[map_dict["Payment Method"]].strip()
                    ,row[map_dict["Total"]]
                    ,line_item_array
                    ,line_cost
                    ,line_profit)

                else:
                    current_line_item = current_order.line_item
                    sku = row[map_dict["Lineitem sku"]]
                    line_quantity = row[map_dict["Lineitem quantity"]]
                    line_price = Decimal(row[map_dict["Lineitem price"]])
                    line_fulfillment_status = row[map_dict["Lineitem fulfillment status"]]

                    if line_fulfillment_status == "fulfilled":
                        if sku in product_cost:
                            line_cost = product_cost[sku]
                        else:
                            line_cost = 0
                            exceptions.append(Exception("Line Item Cost Missing, SKU:", sku))

                        line_cost =  Decimal(line_cost)
                        line_profit = (line_price - line_cost) * Decimal(line_quantity)

                        line_item = LineItem(order_id
                        , [map_dict["Lineitem name"]]
                        , [sku]
                        , [line_price]
                        , [line_quantity]
                        , line_cost
                        , line_profit)

                        current_line_item.append(line_item)

                        current_order.product_cost += line_cost
                        current_order.order_profit += line_profit

            if current_order is not None:
                print("order:",current_order.order_id,", product_cost:", current_order.product_cost, ", order_profit", current_order.order_profit)
            row_count += 1
            total_row_count = get_row_count(FILENAME)
            if row_count == total_row_count:
                orders.append(current_order)
                print ("shopify csv parsing done")

def print_shopify_order():
    for order in orders:
        print (order) 

def total_order_gross():
    total_profit = Decimal(0)
    for order in orders:
        customer_paid_shipping = Decimal(order.shipping) #customer paid shipping fee
        expenses = Decimal(0)
        payment_cost = Decimal(0)
        shipping_cost = Decimal(0)
        discount_amt = Decimal(order.discount_amt)
        refund_amt = Decimal(order.refund_amt) 
        #Payment Cost
        payment = order.payment
        shipping_country = order.shipping_country
        total = Decimal(order.total)
        if payment == "Shopify Payments":
            total = total - refund_amt
            if shipping_country == "HK":
                payment_cost = total * Decimal(RATE_SHOPIFY_PAYMENTS_HK) + Decimal(CHARGES_SHOPIFY_EXTRA)
            else:
                payment_cost = total * Decimal(RATE_SHOPIFY_PAYMENTS_OTHER) + Decimal(CHARGES_SHOPIFY_EXTRA)
        elif payment == "PayPal Express Checkout":
            total = total - refund_amt
            payment_cost = total * Decimal(RATE_PAYPAL) + Decimal(CHARGES_SHOPIFY_EXTRA)
        else:
            payment_cost = Decimal(CHARGES_CUSTOM)
        #Shipping Cost
        if shipping_country == "HK":
            shipping_cost = Decimal(SHIPPING_SF_HK_COST)
        elif shipping_country == "MO":
            shipping_cost = Decimal(SHIPPING_SF_MO_COST)
        else:
            shipping_cost = Decimal(0)
            overseas_orders.append(Exception("Order Shipping Country Exception, id:", order.order_id))

        if payment == "custom":
            expenses = customer_paid_shipping - discount_amt - refund_amt - shipping_cost - payment_cost
        else:
            expenses = customer_paid_shipping - payment_cost - shipping_cost - discount_amt

        expenses = expenses.quantize(Decimal('.00'), ROUND_HALF_UP)
        gross = order.order_profit + expenses

        if gross <= 0:
            loss_order.append(Exception("Order with no profit, id:", order.order_id))


        total_profit += gross

        print("order:",order.order_id,",order_profit:", order.order_profit, ",payment_cost:", payment_cost.quantize(Decimal('.00'), ROUND_HALF_UP), ",expenses:", expenses,",gross:" + str(gross),",total_gross:" + str(total_profit))

# try:
costs = cost_table()
csv_parsing(costs)
print_shopify_order()
total_order_gross()
if len(exceptions) > 0:
    for error in exceptions:     
        print (error)

if len(partially_refunded) > 0:
    for error in partially_refunded:     
         print (error)

if len(overseas_orders) > 0:
    for error in overseas_orders:     
         print (error)


if len(loss_order) > 0:
    for error in loss_order:     
         print (error)


# except Exception as error:
#     print (error)


