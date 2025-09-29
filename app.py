from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ExecutionTimeout
from bson import ObjectId
import pprint

# -------------------------
# Database connection
# -------------------------

# Connection string for mongoDB 
MONGO_URI = "mongodb+srv://g24h9724_db_user:g24h9724@cluster0.lkmoqjo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)  # adjust if using Atlas
db = client["ecommerce_db"]      #  chosen DB name
users = db["users"]    # example users

# Pretty Printer for formatted output of documents
pp = pprint.PrettyPrinter(indent=2)


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
        print("2. create multiple documents")
        print("3. Read All documents")
        print("4. Read documents with...")
        print("5  Update all documents with... ")
        print("6  Update document with...")
        print("7. Delete ducuments with...")
        print("8. Delete ALL documents")
        print("9. Exit")

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
            print("Exiting...")
            quit()

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    menu()

