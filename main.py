from Database import Database

if __name__ == "__main__":
    database = Database("sqlite:///articles.db")
    database.populateDatabase()