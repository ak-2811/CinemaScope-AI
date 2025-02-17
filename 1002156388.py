import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

indexName = "all_products"

try:
    elastic_search = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "gNTtlx22gyZzG89iA89r"),
    ca_certs="C:/Users/aksha/OneDrive - UT Arlington/Desktop/ML_MS/elasticsearch-8.13.1/config/certs/http_ca.crt"
    )
except ConnectionError as e:
    print("Connection Error:", e)
    
if elastic_search.ping():
    print("Succesfully connected to ElasticSearch!!")
else:
    print("Oops!! Can not connect to Elasticsearch!")




def search(input_keyword):
    model = SentenceTransformer('all-mpnet-base-v2')
    vector_of_input_keyword = model.encode(input_keyword)

    query = {
        "field": "title_genre_vector",
        "query_vector": vector_of_input_keyword,
        "k": 5,
        "num_candidates": 999
    }
    res = elastic_search.knn_search(index="all_products"
                        , knn=query 
                        , source=["Series_Title","Genre","Director","IMDB_Rating","Star1", "Star2", "Star3","Star4"]
                        )
    results = res["hits"]["hits"]

    return results

def main():
    st.title("Search Series Title")

    # Input: User enters search query
    search_query = st.text_input("Enter your search query")

    # Button: User triggers the search
    if st.button("Search"):
        if search_query:
            # Perform the search and get results
            results = search(search_query)

            # Display search results
            st.subheader("Search Results")
            for result in results:
                with st.container():
                    if '_source' in result:
                        try:
                            st.header(f"{result['_source']['Series_Title']}")
                        except Exception as e:
                            print(e)
                        
                        try:
                            st.write(f"Genre: {result['_source']['Genre']}")
                        except Exception as e:
                            print(e)

                        try:
                            st.write(f"Director: {result['_source']['Director']}")
                        except Exception as e:
                            print(e)

                        try:
                            st.write(f"Ratings: {result['_source']['IMDB_Rating']}")
                        except Exception as e:
                            print(e)
                        
                        try:
                            st.write(f"Star Name: {result['_source']['Star1']}")
                        except Exception as e:
                            print(e)

                        try:
                            st.write(f"Star Name: {result['_source']['Star2']}")
                        except Exception as e:
                            print(e)

                        try:
                            st.write(f"Star Name: {result['_source']['Star3']}")
                        except Exception as e:
                            print(e)

                        try:
                            st.write(f"Star Name: {result['_source']['Star4']}")
                        except Exception as e:
                            print(e)
                        # st.divider()

                    
if __name__ == "__main__":
    main()