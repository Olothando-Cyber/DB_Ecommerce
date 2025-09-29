import os
from pymongo import MongoClient
from faker import Faker
from datetime import datetime, timedelta
import random
from bson.objectid import ObjectId

# --- MongoDB Connection ---
# Students, insert your MongoDB connection URI here
# For example: "mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority"

MONGO_URI = "mongodb+srv://g24n9666_db_user:M4rk4ev3r@cluster0.lkmoqjo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

DB_NAME = "ecommerce_db"

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
except Exception as e:
    print("Connection error")
# --- Faker Initialization ---
fake = Faker('en_US')

# --- Configuration ---
NUM_PRODUCTS = 100
NUM_USERS = 50
MIN_ORDERS_PER_USER = 1
MAX_ORDERS_PER_USER = 5
MIN_ITEMS_PER_ORDER = 1
MAX_ITEMS_PER_ORDER = 5
MIN_REVIEWS_PER_PRODUCT = 0
MAX_REVIEWS_PER_PRODUCT = 10
def generate_products(num_products):
    products = []
    categories = ["Electronics", "Books", "Home Goods", "Clothing", "Sports & Outdoors", "Beauty", "Toys"]
    
    for _ in range(num_products):
        category = random.choice(categories)
        
        product = {
            "_id": ObjectId(),
            "name": fake.unique.bs(),
            "description": fake.paragraph(nb_sentences=3),
            "price": round(random.uniform(10.0, 1000.0), 2),
            "category": category,
            "tags": random.sample(fake.words(nb=5), k=random.randint(1, 3)),
            "features": [
                {"name": "Material", "value": fake.word()},
                {"name": "Color Options", "value": random.sample(['Red', 'Blue', 'Green', 'Black', 'White'], k=random.randint(1, 3))},
            ],
            "reviews": [],
        }

        if random.random() < 0.7:
            product["variants"] = [
                {
                    "color": random.choice(['Red', 'Blue', 'Green', 'Black', 'White']),
                    "size": random.choice(['S', 'M', 'L', 'XL']) if category == "Clothing" else None,
                    "sku": f"{fake.unique.random_number(digits=6)}",
                    "stock": random.randint(0, 100)
                } for _ in range(random.randint(1, 3))
            ]
        else:
            product["variants"] = []

        products.append(product)
    
    print(f"Generated {len(products)} products.")
    return products


def generate_users(num_users):
    users = []
    for _ in range(num_users):
        user = {
            "_id": ObjectId(),
            "name": fake.name(),
            "email": fake.unique.email(),
            "address": {
                "street": fake.street_address(),
                "city": fake.city(),
                "zip": fake.postcode(),
                "country": fake.country(),
            },
            "order_history": [],
            "payment_methods": [
                {
                    "type": "Credit Card",
                    "last4": str(fake.random_number(digits=4)),
                    "expiry": fake.credit_card_expire(),
                }
            ]
        }
        users.append(user)
    print(f"Generated {len(users)} users.")
    return users

def generate_orders(users, products):
    orders = []
    for user in users:
        num_orders = random.randint(MIN_ORDERS_PER_USER, MAX_ORDERS_PER_USER)
        for _ in range(num_orders):
            order_date = fake.date_time_between(start_date="-2y", end_date="now")
            items = []
            total_amount = 0
            num_items = random.randint(MIN_ITEMS_PER_ORDER, MAX_ITEMS_PER_ORDER)
            
            selected_products_for_order = random.sample(products, k=min(num_items, len(products)))

            for prod in selected_products_for_order:
                quantity = random.randint(1, 3)
                price_at_purchase = prod["price"]
                total_amount += quantity * price_at_purchase
                item = {
                    "product_id": prod["_id"],
                    "product_name": prod["name"],
                    "quantity": quantity,
                    "price_at_purchase": price_at_purchase,
                }
                items.append(item)

            order = {
                "_id": ObjectId(),
                "user_id": user["_id"],
                "order_date": order_date,
                "total_amount": round(total_amount, 2),
                "items": items,
                "shipping_address": user["address"],
                "status_history": [
                    {"status": "Pending", "date": order_date},
                    {"status": random.choice(["Processing", "Shipped"]), "date": order_date + timedelta(days=random.randint(0, 5))}
                ]
            }
            orders.append(order)
            db.users.update_one({"_id": user["_id"]}, {"$push": {"order_history": {"order_id": order["_id"], "order_date": order_date}}})
    print(f"Generated {len(orders)} orders.")
    return orders

def populate_product_reviews(products, users):
    for product in products:
        num_reviews = random.randint(MIN_REVIEWS_PER_PRODUCT, MAX_REVIEWS_PER_PRODUCT)
        for _ in range(num_reviews):
            reviewer = random.choice(users)
            review_date = fake.date_time_between(start_date=product["_id"].generation_time.replace(tzinfo=None), end_date="now")
            review = {
                "user_id": reviewer["_id"],
                "rating": random.randint(1, 5),
                "comment": fake.paragraph(nb_sentences=2),
                "date": review_date,
                "upvotes": random.randint(0, 20)
            }
            db.products.update_one({"_id": product["_id"]}, {"$push": {"reviews": review}})
    print("Populated product reviews.")

def main():
    print(f"Connecting to MongoDB at {MONGO_URI}...")
    db.products.drop()
    db.users.drop()
    db.orders.drop()
    print("Dropped existing collections.")

    products_data = generate_products(NUM_PRODUCTS)
    users_data = generate_users(NUM_USERS)

    db.products.insert_many(products_data)
    db.users.insert_many(users_data)
    
    orders_data = generate_orders(users_data, products_data)
    db.orders.insert_many(orders_data)

    populate_product_reviews(products_data, users_data)

    print("\nDataset generation complete!")
    client.close()
    print("MongoDB connection closed.")

if __name__ == "__main__":
    main()