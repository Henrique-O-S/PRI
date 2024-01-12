# Notes

Consists of random notes, thoughts which could be useful for the final exam.

## 1. [Introduction](./pri2324-01-intro.pdf)

The information life cycle is the **continuous** process of creating/generating, collecting, recording/storing, processing, distributing/transmitting, consuming/using and disposing of information.

Information Retrieval is the CS field focused on: finding information that is **relevant** --> to a user's **need**.

Information Access:
- We cannot simply use pattern matching and structured queries (e.g. SQL) to find information.
- **Information Retrieval** != Data Retrieval:
    - Not limited to exact matching (e.g. multiple words, synonyms, etc.);
    - Is ordered by relevance, i.e. the most relevant documents are shown first according to the user's query.

**Ad Hoc Search** is the most common type of search, where the user is looking for information on a specific topic.

**Vertical Search** focuses on a specific domain, e.g. searching for a specific product on Amazon. The results aren't limited to "documents", e.g. a game result, a product, etc.

**Enterprise Search** is a type of search that is performed on a company's intranet, e.g. searching for a document.

**Desktop Search** is a type of search that is performed on the user's computer, e.g. searching for a file.

## 2. [Data Collection](./pri2324-02-data-collection.pdf)

Starting with the terminology:
- **Data**: is a collection of facts; measurement of something on a scale;
- **Metadata**: is data about data, e.g. the date of creation of a file, author, etc.;
- **Information**: is data that has been processed and has meaning --> it is useful;

Regarding the **value** in **Data**, it is considered to be the new Oil, i.e. it is a valuable resource that can be used to generate value. Also, we can **increase** the value of data by combining, cleaning, processing... etc.:
- **Indirect Value**: provides insights into the user's behavior, e.g. purchasing habits;
- **Direct Value**: the data itself is valuable, e.g. a product recommendation system;

The primary blocks in data-intensive systems include:
- Where and how to store the data efficiently (databases);
- Cache expensive operations;
- Enable search and filtering (indexing);
- Stream messages between systems;
- Periodically process data (batch processing);


