# PRI - Information Processing and Retrieval

## Group G88
| Name             | Number    | E-Mail             |
| ---------------- | --------- | ------------------ |
| Diogo Silva        | 202004288 | up202004288@edu.fe.up.pt   |
| Henrique Silva     | 202007242 | up202007242@edu.fe.up.pt   |
| João Araújo        | 202004293 | up202004293@edu.fe.up.pt   |
| Tiago Branquinho   | 202005567 | up202005567@edu.fe.up.pt   |


---

## Table of Contents

- [Brief Description](#brief-description)
- [Project Milestones](#project-milestones)
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)


---

## Brief Description

The goal of this project that is going to run the whole semester is to develop an information search engine, which includes work on data collection and preparation, information querying and retrieval, and retrieval evaluation.

## Project Milestones

- [ ] Milestone 1 - **Data Collection and Preparation**. The first milestone is achieved with the preparation and characterisation of the datasets selected for the project. The datasets are the foundation for the project and the goal of the first task is to prepare and explore them. This task is heavily dependent on the datasets, which may require some extraction actions such as crawling or scraping.

- [ ] Milestone 2 - **Information Retrieval**. The second milestone is achieved with the implementation and use of an information retrieval tool on the project datasets and its exploration with free-text queries. This task makes use of state-of-the-art retrieval tools and involves the view of the datasets as collections of documents, the identification of a document model for indexing, and the design of queries to be executed on the indexed information.

- [ ] Milestone 3 - **Search System**. The third milestone is achieved with the development of the final version of the search system. This version is an improvement over the previous milestone, making use of features and techniques with the goal of improving the quality of the search results. For this milestone, we are expected to explore innovative approaches and ideas, and will heavily depend on the context and data. Additionally, an extended evaluation of the results and a comparison with the previous version of the search system is also expected.

---

## Milestone 1 - Data Collection and Preparation

### Datasets

The datasets used in this project are the following:

- [CNBC News - Site map](https://www.cnbc.com/site-map/). The dataset scraped from CNBC contains news articles from the CNBC website, which is a world leader in business news and real-time financial market coverage. The dataset is proven to be reliable and trustworthy, as it is a well-known news website. The dataset is composed of **XXXXX+** news articles regarding the "Market Insider" topic, starting from 2020 to the present days.

- [CNBC NEWS - Quotes](https://www.cnbc.com/quotes/). This dataset contains quotes from the CNBC website for every stock in the market. The desired quotes are obtained from the previous dataset, as it contains the stock symbol for each news article. The dataset is composed of **XXXXXX** companies.

### Data Characterization

- The utilized data can be divided into two groups: articles and companies information.
- The articles contain:
    - Structured data: list of authors, published and edited date, title, topic
    - Unstructured data: main text, key points
- The companies information contain:
    - Structured data: name, tag
    - Unstructured data: description

### Exploratory Data Analysis

- In this section patterns and outliers were recognized among the two types of data, which were essential to achieve insightful decision-making.
- Some keywords were also extracted from some analysis, in order to ease finding future relations between data.

### Data Processing Pipeline
- The detailed description of both pipelines was made, detailing the steps done regarding both the scrapping and the storage of data.

<figure>
    <img src="img/companies_pipeline.png" alt="Companies Pipeline" />
    <figcaption>Companies Pipeline</figcaption>
</figure>

<figure>
    <img src="img/articles_pipeline.png" alt="Articles Pipeline" />
</figure>
<figure>
    <img src="img/articles_pipeline2.png" alt="Articles Pipeline" />
    <figcaption>Articles Pipeline</figcaption>
</figure>

### Data Domain Model

- INSERT MODELS

### Documents Classification

- At an intermediary stage in the pipeline, there are two document
collections, prepared and created after the scraping process. In
both cases, the documents are JSON objects and the collections
themselves JSON files.

- At a final stage, there are these main document collections, each one being a table in a SQLite database (in articles.db)
    - Company
    - Article
    - CompanyArticleAssociation

<figure>
    <img src="img/uml.png" alt="Database articles.db UML" />
    <figcaption>Database articles.db UML</figcaption>
</figure>

## Usage



## Milestone 2 - Information Retrieval

TODO

## Milestone 3 - Search System

TODO

