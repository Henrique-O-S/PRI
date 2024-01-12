nothing includes software solutions (examples)
# intro
Classic workflow and typical tasks.
- Data Ingestion
    - Collect data
    - Describe data
    - Move data
- Data Transformation
    - Data modeling
    - Data migration
    - Pipeline orchestration
- Data Optimization
    - Selection, export, assessment

Information Retrieval distinguishes itself from Data Retrieval in two central aspects:
- Not limited to exact matching (e.g. multiple words, synonyms)
- Is ordered by relevance, i.e. importance to the user’s query (a central concept in IR).


“Ad hoc” search is the most common type of search task.
- “Ad hoc” refers to an independent search episode to retrieve information for an isolated information need. Contrast with a search. 

Vertical search focuses on domain-specific information such as news, travel, music, sports, academic papers, etc.

Enterprise Search is designed to allow search across an enterprise’s content.

Desktop Search is a single-user system focused on searching the contents stored in a computer.

# Data collection

Data
- is a measurement of something on a scale;
- a fact known by direct observation.
Metadata
- is "data about data";
- not the content of data but data providing information about one or more aspects of the data, such
as description (date, time, author), structure (format, version), administrative (permissions), legal, etc.
Information
- is data with a context / meaning, thus enabling decision making;
- is data that has been processed, organized and structured

Life cycle of information:
    - Occurence
    - Transmission
    - Processing and Management
    - Usage

Value in Data
- Indirect value — data provides value by influencing of supporting decisions, e.g. risk analysis in insurance, purchase decisions in retail
- Direct value — data provides value by feeding automated systems, e.g. search system, product recommendation system

Data Stages
- Raw - focus on data discovery
- Refined - focus on data preparation for further exploration
- Production - focus is on integrating it into production processes or products

ETL pattern (recent evolution) - Extract Transform Load (!= ELT)

OSMN
- Obtain
- Scrub
- Explore
- Model
- Interpret

# Data Preparation (/wrangling)

ad hoc search task:
- standard retrieval task in which the user specifies his information need through a query which initiates a search (executed by the information system) for documents which are likely to be relevant to the user.
    - Google search
    - Desktop search
    - Email search

includes:
- Understand what data is available;
- Choose what data to use and at what level of detail;
- Understand how to combine multiple sources of data;
- Deciding how to distill the results to a size and shape that enables the follow-up steps.

Common tasks:
- Cleaning
- Transformation
    - Normalization
    - Scaling values to the same range
    - Non-linear transformations
    - Discretization/binning
- Synthesis (create new attributes from existing data)
- Integration
    - Combine data that originally exists in multiple sources
    - Linking the corresponding records is a central step of many tasks of this "area"
- Reduction or selection
    - Data filtering
        - Used to remove data from the dataset
        - Can be used just to test with more manageable data portion
        - Operations are deterministic in nature
    - Data Sampling
        - Takes a random subset of the data items of a requested size (important to make sure the resulting sample is representative)
            - May need to analyze data distribution before and after
        - Non deterministic
    - Data aggregation
        - Grouping data via the aggregation operator (mean, median, min, max, percentile)
        - May be used to reduce ecessive detail

Requires a good understanding of data properties --> data visualization also used
 - can be done before, during or after exploring properties of data

Data pipelines should be: --> should (really) be treated/viewed as software //// are software
- Reliable
- Scalable
- Maintainable

Makefiles
- used to automate software build processes, by defining targets and rules to execute
- abstraction of a dependency graph


Data documentation
- key element in various steps
- distinguishes between ad-hoc processes and repeatable, inspectable, shareable processes

Data Flow Diagrams (DFD):
- can be used to represent the flow of data from external entities into the system, show how data moves from one process to another, and data's logical storage
- squares - external entities
- rounded rectangles - processes
- arrows - data flows
- open-ended rectangles - data stores

# Data Processing

Document model vs Relational model vs graph model vs triple-store model
- Data models central in data processing

Document model advantages
- good when dealing with 1-1 or 1-N relations
- Schema flexibility
- locality (related data stored together) --> better performance
- data model might be closer to the application's data structures

Graph model advantages
- good when dealing with many-to-many relation
- Not limited to homogeneous data

Relational model advantages
- locality (related data stored together) --> better performance
- data model might be closer to the application's data structures

Triple-Store model
- Information stored in 3-part statements - (subject, predicate, object)


Interaction types
- Online systems - services:
    - Waits for requests from a client. When it does, handle it ASAP and send response. Performance = response time
- Offline systems - batch processing:
    - Takes a large input of data, runs job and produces output. Best for long jobs or async processes
- Stream processing systems:
    - Operate on inputs and produce output. Result of event happening

Data visualization can be divided into exploration and explanation ends


# Applied NLP for Information Retrieval

key NLP tasks for IR
- Tokenization
- Stemming and Lemmatization
- POS tagging
- NER
- Relation Extraction
- Sentiment analysis




recall -> percentagem dos relevantes para conceito que estao presentes na lista
precisao -> percentagem dos da lista que sao relevantes




