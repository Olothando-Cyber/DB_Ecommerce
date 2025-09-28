from pymongo import MongoClient
from bson import ObjectId
import pprint

# -------------------------
# Database connection
# -------------------------
MONGO_URI = "mongodb+srv://g24h9724_db_user:g24h9724@cluster0.lkmoqjo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)  # adjust if using Atlas
db = client["ecommerce_db"]      #  chosen DB name
users = db["users"]    # example users

pp = pprint.PrettyPrinter(indent=2)


# -------------------------
# CRUD Function Templates
# -------------------------

def create_document(doc, users):
    print( "Document successfully created with id:", users.insert_one(doc).inserted_id)

def create_documents(doc,users):
    print( "Multiple documents created with id's:",(users.insert_many(doc, ordered=False)).inserted_ids)


def read_all_documents(search = None):
    if (search is None):
        criteria = db.users.find()
    else:
        criteria = db.users.find(search)
    for cust in criteria:
        print (cust)
     

def update_document(find, replace):
    if(len(find[0]>1)):
        print( db.users.update_many(filter=find, update= replace))
    else:
        print( db.users.update_one(filter = find, update = replace))

def delete_document(search = None):
    if search is None:
        print( db.users.delete_many(search))
    else:
        print( db.users.delete_one(search))






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
                # names.append(name)
                # emails.append(email)
                documents.append({"name": name, "email":email})
            create_documents(documents,users)
        
        elif choice == "3":
            read_all_documents()
        
        elif choice == "4":
            name = input("Enter customer name: ")
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

