class LineItem():
    def __init__(self, order_id, name, sku, price, quantity, cost, profit):
        self.order_id = order_id
        self.name = name
        self.sku = sku
        self.price = price
        self.quantity = quantity
        self.cost = cost
        self.profit = profit

    def __str__(self):
        return "Lineitem(sku:"+str(self.sku)+" price:"+str(self.price)+" quantity:"+str(self.quantity)+" cost:"+str(self.cost)+" profit:"+str(self.profit) +")\n"
 