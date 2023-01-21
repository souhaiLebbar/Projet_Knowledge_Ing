import streamlit as st
import datetime
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph,Namespace
import json 

st.title("Doctor's visit")


with st.form("Patient form"):
   title = st.text_input('First name', '')
   title = st.text_input('Last name', '')
   title = st.text_input('NSS', '')
   d= st.date_input("Patient birthday",) 
   txt = st.text_area('How do your patient feel ?',"csv")
   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")

if submitted & (txt=="wiki"):
    st.title("Diagnostic report")
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    # Below we SELECT both the hot sauce items & their labels
    # in the WHERE clause we specify that we want labels as well as items
    sparql.setQuery("""
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX mc: <http://www.inria.org/entity/>
        PREFIX mp: <http://www.inria.org/property/>
        PREFIX owl:  <http://www.w3.org/2002/07/owl#>

        construct {
        ?id a mc:Disease ;
            owl:sameAs ?x ;
            mp:hasSyndrom ?idz ;
            mp:hasTherapy ?idy .

        ?idz owl:sameAs ?z .
        ?idy owl:sameAs ?y .
        } where {
        ?x wdt:P31 wd:Q12136 ;
            wdt:P2176 ?y ;
            wdt:P780 ?z ;
            wdt:P244 ?a .

        ?z wdt:P244 ?b .
        ?y wdt:P244 ?c .
        
        bind(iri(concat("http://www.inria.org/instance/", ?a)) as ?id)
        bind(iri(concat("http://www.inria.org/instance/", ?c)) as ?idy)
        bind(iri(concat("http://www.inria.org/instance/", ?b)) as ?idz)
        }
    """)
    sparql.setReturnFormat(JSON)
    wiki_results = sparql.query().convert()
    st.subheader("wikidata service result :")
    st.json(wiki_results)

if submitted & (txt=="csv"):
    st.title("Diagnostic report")
    # Load the turtle file into a graph
    g = Graph()
    g.parse("csv_lifting/output/dataset.ttl", format="turtle")
    g.parse("csv_lifting/output/symptom_Description.ttl", format="turtle")
    g.parse("csv_lifting/output/symptom_precaution.ttl", format="turtle")
    g.parse("csv_lifting/output/symptom_severity.ttl", format="turtle")
    # Create a namespace for the ontology
    ontology = Namespace("disease_owl.ttl")
    # Create a SPARQL endpoint from the graph
    # sparql = SPARQLWrapper(g)
    # Below we SELECT both the hot sauce items & their labels
    # in the WHERE clause we specify that we want labels as well as items
    qres = g.query("""
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX mc: <http://www.inria.org/entity/>
        PREFIX mp: <http://www.inria.org/property/>
        PREFIX owl:  <http://www.w3.org/2002/07/owl#>
        PREFIX schema: <http://schema.org/>

        SELECT ?diseaseName ?syndromName ?severity ?therapy WHERE {
            ?disease a mc:Disease;
                schema:name ?diseaseName;
                mp:hasSyndrom ?syndromName ;
                mp:hasTherapy ?therapy .
                ?syndrom schema:name ?syndromName;
                    mp:hasWeight ?severity .
            }

        """,
        initNs={"ontology": ontology},
        )
   
    #sparql.setReturnFormat(JSON)
    #csv_results = sparql.query().convert()
    st.subheader("CSV result :")
    # Convert the query results to JSON
    json_results = json.dumps([{'diseaseName':row[0], 'syndromName':row[1], 'severity':row[2], 'therapy':row[3] } for row in qres])

    # Print the results
    st.json(json_results)