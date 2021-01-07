class Order():
    def __init__(self, order, status, profit, product_cost, payment_cost, shipping_cost, refund_amt, discount_amt, payment_type, total, products):
        self.order = order
        self.status = status
        self.profit = profit
        self.product_cost = product_cost
        self.payment_cost = payment_cost
        self.shipping_cost = shipping_cost
        self.refund_amt = refund_amt
        self.discount_amt = discount_amt
        self.payment_type = payment_type
        self.total = total
        self.products = products