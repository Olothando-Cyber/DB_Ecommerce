from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ExecutionTimeout
from bson import ObjectId
import pprint

# -------------------------
# Database connection
# -------------------------

# Connection string for mongoDB 
MONGO_URI = "mongodb+srv://g24m5008_db_user:Lucas@cluster0.lkmoqjo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)  # adjust if using Atlas
db = client["ecommerce_db"]      #  chosen DB name
users = db["users"]    # example users


# Pretty Printer for formatted output of documents
pp = pprint.PrettyPrinter(indent=2)

# -------------------------
# ADVANCED QUERYING FUNCTIONS
# -------------------------

products = db['products']

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
        print("15. Exit")

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

        elif choice == "15":
            print("Exiting...")
            quit()

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    menu()

