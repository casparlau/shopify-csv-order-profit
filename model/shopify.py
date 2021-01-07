class Shopify():
    def __init__(self, order_id, status, shipping, shipping_country, bill_country, refund_amt, discount_amt, payment,total, line_item, product_cost, order_profit):
        self.order_id = order_id
        self.status = status
        self.shipping = shipping
        self.shipping_country = shipping_country
        self.bill_country = bill_country
        self.refund_amt = refund_amt
        self.discount_amt = discount_amt
        self.payment = payment
        self.total = total
        self.line_item = line_item
        self.product_cost = product_cost
        self.order_profit = order_profit

    def __str__(self):
        items = ""
        for line in self.line_item:
            items += str(line)
        return "\nShopify("+str(self.order_id)+")\nstatus:"+str(self.status) +"\nshipping:"+str(self.shipping)+"\nshipping_country:"+str(self.shipping_country)+"\nbill_country:"+str(self.bill_country)+"\nrefund_amt:"+str(self.refund_amt)+"\ndiscount_amt:"+str(self.discount_amt)+"\npayment:"+str(self.payment)+"\ntotal:"+str(self.total)+"\nline_item:\n"+items+"product_cost:"+str(self.product_cost)+"\norder_profit:"+str(self.order_profit)
 