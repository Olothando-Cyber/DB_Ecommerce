from pymongo import MongoClient
from bson import ObjectId
import pprint

# -------------------------
# Database connection
# -------------------------
client = MongoClient("mongodb://localhost:27017/")  # adjust if using Atlas
db = client["ecommerce_db"]      #  chosen DB name
collection = db["customers"]    # example collection

pp = pprint.PrettyPrinter(indent=2)


# -------------------------
# CRUD Function Templates
# -------------------------

def create_document(doc, collection):
    
        if len(doc) >1:
            return "Multiple documents created with id's:",(db.collection.insert_many(doc, ordered=False)).insterted_ids
        else:
            db.collection.insert_one(doc)
            return "Document successfully created with id:",doc["_id"]


def read_all_documents(search = None):
    if (search is None):
        criteria = db.collection.find()
    else:
        criteria = db.collection.find(search)
    for cust in criteria:
        print (cust)
     

def update_document(find, replace):
    if(len(find[0]>1)):
        return db.collection.update_many(filter=find, update= replace)
    return db.collection.update_one(filter = find, update = replace)

def delete_document(search = None):
    if search is None:
        return db.collection.delete_many(search)   
    return db.collection.delete_one(search)






# -------------------------
# Menu System
# -------------------------

def menu():
    while True:
        print("\n--- MongoDB Project Menu ---")
        print("1. Create Document")
        print("2. create multiple documents")
        print("3. Read All Documents")
        print("4. Read all documents with...")
        print("5 Update all documents ")
        print("6. Delete all ducuments with...")
        print("7. Delete ALL documents")
        print("9. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter student name: ")
            email = (input("Enter email: "))
            create_document({"name": name, "email": email})

        elif choice == "2":
            No_of_inputs = input("Enter the number of documents to input: ")
            names = []
            emails =[]
            for i in No_of_inputs:
                name = input("Enter student name: ")
                email = (input("Enter email: "))
                names[i] = name
                emails[i] =email
            create_document({"name": names, "email":emails})
        
        elif choice == "3":
            read_all_documents()
        
        elif choice == "4":
            name = input("Enter student name: ")
            email = (input("Enter email: "))
            read_all_documents({"name": name, "email":email})
        
        elif choice =="5":
            find = {"name": input("Enter the name of the documents you're searching for: "), "email":input("Enter email of the one you're searching for: ")}
            replace = {"$set":{"name": input("Enter the name you'll be replacing: "), "email":input("Enter email of the one you'll be replacing: ")}}
            update_document(find, replace)
        
        elif choice == "6":
            find = {"name": input("Enter the name of the documents you're searching for: "), "email":input("Enter email of the one you're searching for: ")}
            delete_document(find)

        elif choice == "7":
            delete_document()

        elif choice == "9":
            print("Exiting...")
            quit()

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    menu()

