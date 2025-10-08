import random
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ExecutionTimeout
from bson import ObjectId
import pprint
from datetime import datetime

# -------------------------
# Database connection
# -------------------------

# Connection string for mongoDB 
MONGO_URI = "mongodb+srv://<studentNumber>_db_user:<password>@cluster0.lkmoqjo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)  # adjust if using Atlas
db = client["ecommerce_db"]      #  chosen DB name
users = db["users"]    # example users


# Pretty Printer for formatted output of documents
pp = pprint.PrettyPrinter(indent=2)

# -------------------------
# ADVANCED QUERYING FUNCTIONS
# -------------------------

products = db['products']
orders= db['orders']

def logical_query_and():
    """
    Find products using the $and operator
    E.g: Find products that are both in "Electronics" category and has a price less than $200 
    """
    try:
        qry = {"$and": [{"category": "Electronics"}, {"price": {"$lt": 200}}]}
        results = products.find(qry) 
        print("\n\t\tElectronics under $200:")
        for product in results:
            print(f"Product: {product.get('name','N/A')}, Price: ${product.get('price','N/A')}")
    except Exception as e:
        print(f"Error in $and query: {e}")

def logical_query_or():
    """
    Find products using $or operator
    E.g:Find products in the "Beauty" or "Clothing" categories
    """
    try:
        qry = {"$or":[{"category": "Beauty"}, {"category": "Clothing"}]}
        results = products.find(qry)
        print("\n\t\tBeauty OR Clothing products:")
        for product in results:
            print(f"Product: {product.get('name', 'N/A')}, Category:{product.get('category','N/A')}")
    except Exception as e:
        print(f"Error in $or query: {e}")
def logical_query_not():
    """
    Find products that are not in "Electronics" and "Toys"
    """
    try:
        qry =  {"category": {"$not": {"$in": ["Electronics", "Toys"]}}}
        results = products.find(qry)
        print("\n\t\tProducts that are not Electronics nor Toys:")
        for product in results:
            print(f"Product:{product.get('name','N/A')},Category: {product.get('category','N/A')}")
    except Exception as e:
        print(f"Error in $not query:{e}")

def comp_and_elem_queries():
    """
    Find products using comparison operators $gt and $lt
    E.g: Find products in Electronics between $200 and $1000
    """
    try:
        qry = {"category":"Electronics","price":{"$gt":200,"$lt":1000}}
        results = products.find(qry)
        print("\n\t\tElectronics priced between $200 and $1000:")
        cnt = 0
        for product in results:
            print(f"Product: {product.get('name', 'N/A')}, Price: {product.get('price','N/A')}")
            cnt+=1
        if cnt == 0:
            print("No products found in the Electronics category that are prices between $200 and $1000 ")
    except Exception as e:
        print(f"Error in comparison and Element query ($gt and $lt): {e}")

def in_query():
    """
    Find products using $in operator
    E.g: Find products in specific categories
    """
    try:
        qry = {"category": {"$in": ["Electronics", "Clothing", "Books"]}}
        results = products.find(qry)
        print("\n\t\tProducts in Electronics, Clothing, or Books:")
        for product in results:
            print(f"Product: {product.get('name', 'N/A')}, Category: {product.get('category', 'N/A')}")
    except Exception as e:
        print(f"Error in IN query: {e}")

def exists_query():
    """
    Find products using $exists operator
    E.g Find products that have a 'variants' field
    """
    try:
        qry = {"variants": {"$exists": True}}
        results = products.find(qry)
        print("\n\t\tProducts with the variants field:")
        for product in results:
            print(f"Product:{product.get('name','N/A')}, Variants: {product.get('variants')}")
    except Exception as e:
        print(f"Error in Exists query: {e}")
        
        
# -------------------------
# Array Functiuons
# -------------------------
def review_product(doc, product_name, products):
    """
    Add a review document to the specified product.
    """
    try:
       
        prod = products.find_one({"name": product_name})
        
        
        if prod is None:
            print("Product not found.")
            return
        
      
        products.update_one(
            {"_id": prod["_id"]},
            {"$push": {"reviews": doc}}
        )
        print(f"Review added successfully for product: {product_name}")
    
    except Exception as e:
        print(f"Error adding review: {e}")
        
def get_orders_size(size,orders ):
    if size<0 or type(size)!=int:
        return "invalid input"
    try:
        results= orders.find({"items":{"$size":size}})
        count =0
        for order in results:
            pprint.pprint(order["items"])
            count +=1
        if count ==0:
            print("No orders found matching that size")
    except Exception as e:
        print(f"Error while retrieving orders by size: {e}")

def get_filtered_comments(rating):
    if not isinstance(rating, (int, float)) or rating < 0:
        return "invalid input"

    try:
        # Correct use of $all with $elemMatch and $gt
        results = products.find({
            "reviews": {"$all": [{"$elemMatch": {"rating": {"$gt": rating}}}]}})

        count = 0
        for product in results:
            pprint.pprint(product.get("reviews", []))
            count += 1

        if count == 0:
            print("No reviews found greater than that rating.")
    except Exception as e:
        print(f"Error while retrieving reviews: {e}")
def remove_review(product_name, rating, products):
    """
    Remove a review from the specified product based on rating.
    """
    try:
        # Step 1: Find the product
        prod = products.find_one({"name": product_name})
        
        # Step 2: Handle if not found
        if prod is None:
            pprint("Product not found.")
            return
        
        # Step 3: Pull (remove) the review matching a specific rating
        products.update_one(
            {"_id": prod["_id"]},
            {"$pull": {"reviews": {"rating": rating}}}
        )
        print(f"Review with rating {rating} removed successfully for product: {product_name}")
    
    except Exception as e:
        print(f"Error removing review: {e}")

    
# -------------------------
# Aggregation
# -------------------------
def type_of_products(category,products=products):
    if type(category) != str:
        print("Invalid input")
        return
    try:
        cursor= products.aggregate([
            {"$match":{"category": category}},
            {"$project":{"name":1,"price":1,"tags":1,"features":1}}
        ])
        for doc in cursor:
            print(doc)
        return
    except(ServerSelectionTimeoutError, ExecutionTimeout) as e:
        # Retry if server times out
        print("Failed to create, \nTrying again...")
    except Exception as e:
        # Catch aall other execeptions
        print("Failed to create document.",e)
def all_proucts_cost():
    try:
        cursor = products.aggregate([
            {"$group": {
                "_id":"$category",
                "totalOfCategory": {"$sum":"$price"}
            }}
        ])
        for doc in cursor:
            print(doc)
        return
    except(ServerSelectionTimeoutError, ExecutionTimeout) as e:
        # Retry if server times out
        print("Failed to create, \nTrying again...")
    except Exception as e:
        # Catch aall other execeptions
        print("Failed to create document.",e)
     


# -------------------------
# CRUD Function Templates
# -------------------------

# Create: insert a single document into collection
def create_document(doc, users, attempts = 4):
    # Stop trying after max attempts
    if attempts ==0:
        print("Failed to create document.")
        return
    
    try:
        # Insert one document and print insterted _id
        print( "Document successfully created with id:", users.insert_one(doc).inserted_id)
        return
    except(ServerSelectionTimeoutError, ExecutionTimeout) as e:
        # Retry if server times out
        print("Failed to create, \nTrying again...")
        create_document(doc,users, attempts -1)
    except Exception as e:
        # Catch aall other execeptions
        print("Failed to create document.",e)


        

# Create: insert Multiple documents
def create_documents(doc,users, attempts = 4):
    if attempts ==0:
        print("Failed to create documents")
        return
    try:
        # Insert many documents and print the insterted IDs
        print( "Multiple documents created with id's:",(users.insert_many(doc, ordered=False)).inserted_ids)
        return
    except(ServerSelectionTimeoutError, ExecutionTimeout) as e:
        print("Failed to create, \nTrying again...")
        create_document(doc,users, attempts -1)
    except Exception as e:
        print("Failed to create document.")

# Read:Fetch All documents or only those matvhing a search
def read_all_documents(search = None):
    if (search is None):
        # No filter the retrieve all
        criteria = db.users.find()
        
    else:
        # Apply Filter
        criteria = db.users.find(search)

    # If no documents
    if len(criteria) == 0:
        print("No documents found")
        return
    # Print each document found
    for cust in criteria:
        print (cust)
     
# UPDATE: Update a single document
def update_document(find, replace, attempts = 4):
    if attempts == 0:
        print("Unsuccessful update of documents")
        return
    
    if db.users.find(find):      
        try:
            print( db.users.update_one(filter = find, update = replace))

        except(ServerSelectionTimeoutError, ExecutionTimeout) as e:
            print("Failed to update, \nTrying again...")
            create_document(find,replace, attempts -1)
        except Exception as e:
            print("Failed to update document.",e)
    
    else:
        # If No matvh is found, it then inserts a new document
        print("No document found for such, \ncreating new document")
        create_document(replace,users)
        

# Uodate multiple documents
def update_documents(find, replace, attempts = 4):
    if attempts == 0:
        print("Unsuccessful update of documents")
        return
    
    if db.users.find(find):      
        try:
            # Update all matching documents
            print( db.users.update_many(filter = find, update = replace))

        except(ServerSelectionTimeoutError, ExecutionTimeout) as e:
            print("Failed to update, \nTrying again...")
            create_document(find,replace, attempts -1)
        except Exception as e:
            print("Failed to update document.",e)
    
    else:
        print("No document found for such, \ncreating new document")
        create_document(replace,users)
   

# d5
# db.users.update_many(filter=find, update= replace))
# Delete: remove documents(single or all)
def delete_document(search = None):
    try:
        if search is None:
            print( db.users.delete_many({}))
        else:
            print( db.users.delete_one(search))
    except Exception as e:
        print("Unsuccessful execution of command",e)





# -------------------------
# Menu System
# -------------------------

def menu():
    while True:
        print("\n--- MongoDB Project Menu ---")
        print("1. Create Document")
        print("2. Create multiple documents")
        print("3. Read All documents")
        print("4. Read documents with...")
        print("5  Update all documents with... ")
        print("6  Update document with...")
        print("7. Delete ducuments with...")
        print("8. Delete ALL documents")
        print("9. AND Query: Electronics under $200")
        print("10. OR Query: Beauty OR Clothing")
        print("11. NOT Query: Not Electronics nor Toys")
        print("12. Comparison and element Query: Electronics priced between $200 and $1000")
        print("13. Products with variants field")
        print("14. In Query: Electronics/Clothing/Books")
        print("15. Review a product you have used")
        print("16. Get orders that are a certain size")
        print("17. Filter reviews")
        print("18. Remove review")
        print("19. Get All Products of a Certain Category")
        print("20. Get Total cost of all products by category")
        
        print("21. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter customer name: ")
            email = (input("Enter email: "))
            # print("Please enter your address: ")
            street = input("Please enter your street: ")
            city = input("Please enter your city: ")
            zip = input("Please input your zip code: ")
            country = input("Please input the country you reside in: ")


            create_document({"name": name, "email": email, "address":{"street":street, "city":city,"zip":zip,"country":country}},users)

        elif choice == "2":
            No_of_inputs = input("Enter the number of documents to input: ")
            # names = []
            # emails =[]
            documents = []
            for i in range(int(No_of_inputs)):
                name = input("Enter customer name: ")
                email = (input("Enter email: "))
                street = input("Please enter your street: ")
                city = input("Please enter your city: ")
                zip = input("Please input your zip code: ")
                country = input("Please input the country you reside in: ")
                # names.append(name)
                # emails.append(email)
                documents.append({"name": name, "email":email,"address":{"street":street, "city":city,"zip":zip,"country":country}})
            create_documents(documents,users)
        
        elif choice == "3":
            read_all_documents()
        
        elif choice == "4":
            name = input("Enter customer name: ")
            email = (input("Enter email: "))
            read_all_documents({"name": name, "email":email})
        
        elif choice =="5":
            find = {"name": input("Enter the name of the documents you're searching for: "), "email":input("Enter email of the one you're searching for: ")}
            replace = {"$set":{"name": input("Enter the name replacement name: "), "email":input("Enter email replacement: ")}}
            update_documents(find, replace)
        
        elif choice =="6":
            find = {"name": input("Enter the name of the document you're searching for: "), "email":input("Enter email of the one you're searching for: ")}
            replace = {"$set":{"name": input("Enter the name replacement name: "), "email":input("Enter email replacement: ")}} 
            update_document(find, replace)
        
        elif choice == "7":
            find = {"name": input("Enter the name of the documents you're searching for: "), "email":input("Enter email of the one you're searching for: ")}
            delete_document(find)

        elif choice == "8":
            delete_document({})

        elif choice == "9":
            logical_query_and()

        elif choice == "10":
            logical_query_or()

        elif choice == "11":
            logical_query_not()

        elif choice == "12":
            comp_and_elem_queries()

        elif choice == "13":
            exists_query()

        elif choice == "14":
            in_query()
        
        elif choice =="15":
            product = input("Enter price or name of product: ")
            rating = input("Please enter the rating: ")
            comment = input("Add a comment, please be respectful at all times: ")
            date = datetime.now()
            upvotes = random.randrange(0,15)
            review_product({"rating":int(rating),"comment":comment,"date":date,"upvotes":upvotes},product,products)
            
        elif choice=="16":
            size = input("Please enter the size of orders: ")
            get_orders_size(int(size),orders)
        elif choice=="17":
            rating = input("Please enter the ratings you want to check(ratings greater than): ")
            get_filtered_comments(int(rating))
        elif choice=="18":
            product = input("Enter the product name: ")
            rating = int(input("Enter the rating of the review to remove: "))
            remove_review(product, rating, products)
        elif choice == "19":
            product = input("Please enter the category of the product you are looking for: ")
            type_of_products(product)
        
        elif choice == "20":
            all_proucts_cost()
        elif choice == "21":
            print("Exiting...")
            quit()
        
        
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    menu()

