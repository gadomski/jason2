from jason2.product import Product

products = {
    "gdr": Product("gdr", "native", directory_name="gdr_d"),
    "sgdr": Product("sgdr", "sensor", directory_name="sgdr_d", zipped=True),
}
