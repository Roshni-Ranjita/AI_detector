import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import hiplot as hip
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import plotly.io as pio
from PIL import Image
import streamlit.components.v1 as components
import joblib
import pickle

#add navigation sidebar
st.sidebar.title("🔎Explore")
page = st.sidebar.selectbox("Select a page:", ["Homepage", "Evaluate Text", "Model & Insights"], index=0)
for _ in range(13):  # Change 10 to the number of empty lines you want
    st.sidebar.write("")
st.sidebar.write("View the code and dataset details at [STT811 GitHub](https://github.com/andrew-jxhn/STT811_StatsProject)")

#set page content
if page == "Homepage": 
    st.header('AI or Human? A Machine Learning Approach to Text Classification for Statistical Courses')
    st.write("")
    st.write("Welcome to the AI Detection app! Designed for faculty, this tool allows you to upload student responses and predict whether they are AI-generated.")
    st.write("**Why?** With the rise of large language models (LLMs) like ChatGPT, distinguishing between human and AI-generated text has become increasingly important in academic settings. This tool helps maintain academic integrity by providing insights into the authenticity of student submissions.") 
    st.write("")
    st.write("**App Layout:**")
    st.write("**Upload and Evaluate Text**: Navigate to the ‘Evaluate Text’ page (from the left-hand menu) to submit text and verify its authenticity.")
    st.write("**Learn About the Model and Key Trends**: Visit the ‘Model & Insights’ page to explore critical patterns and a detailed breakdown of the model employed for the analysis.")
    
elif page == "Evaluate Text":
    user_input = st.text_input("Enter Text:")
    # apply novel model on user_input >> should return class (AI or human)
    # probability of AI if AI class predicted
    if user_input:
        st.write(f"You entered: {user_input}")
        #if result == "AI":
            #st.write("This text is AI generated:()")
            #st.write("AI percentage: xx")
        #if result == "Human":
            #st.write("This text is written by a human:)")

elif page == "Model & Insights":
    st.subheader("Understanding the Model's Inner Workings")
    st.write("Identifying AI generated text is the primary focus and the BERT model trained on derived data is used for this problem.")
    st.write("Nagivate to the tabs below to gain a deeper understanding of the key insights and model's structure.")
    tab1, tab2, tab3 = st.tabs(["Data Overview", "Analysis & Insights", "Modelling & Results"])
    st.write("")
    
    with tab1:
        st.write("**Dataset details:**")
        st.write("[AI classifier dataset](https://data.mendeley.com/datasets/mh892rksk2/4) contains responses to 116 statistics related questions, with contributions from both human and AI sources. It has 2239 instances across 3 attributes, and the attributes have string data types. The attribute summary is as follows:")
        st.write("**Question**: The original question asked")
        st.write("**Human**: Response written by a randomly chosen human")
        st.write("**AI**: Response generated by an LLM")
        data = pd.read_csv("aidata_clean_avg.csv")
        st.dataframe(data.iloc[:5, :3].head())
        st.write("Major topics covered in the dataset:")
        imageida0 = Image.open("Streamlit/visualizations/Trigrams.png")
        st.image(imageida0, use_column_width=True)
        st.write("Since the dataset cannot be used in its raw form for model training, it has undergone an exhaustive feature engineering process (highlighted below).")
        st.write("----------------------------------------------------------------------------")
        st.write("**Pre-Processing & Feature Engineering:**")
        imagepp1 = Image.open("Streamlit/visualizations/missing_heatmap.png")
        st.image(imagepp1, use_column_width=True)
        st.write("Rows with all 3 variables missing were dropped. This reduced our dataset to 1993 rows.")
        st.write("Numeric columns derived from the original data were generated. These included: Question_length, Human_length, AI_length, Question_special_count, Human_special_count, AI_special_count, avg_special_char_diff.")
        st.write("To prepare for modelling, we:")
        st.markdown("""
        ✅ Combined AI and human responses to create target variable 'Is_AI'  
        ✅ Prepared processed text by<br>
        &nbsp;&nbsp;&nbsp;&nbsp;- Changing text to lowercase<br>
        &nbsp;&nbsp;&nbsp;&nbsp;- Removing punctuation and special characters from responses<br>
        &nbsp;&nbsp;&nbsp;&nbsp;- Tokenizing words and removing stopwords<br>
        ✅ Combined similar columns to be consistent with the new dataset structure (with target)  
        ✅ Scaled numeric columns using z-score scaling
        """, unsafe_allow_html=True)
        st.write("The transformed dataset is of the form:")
        imagepp2 = Image.open("Streamlit/visualizations/dataset.png")
        st.image(imagepp2, use_column_width=True)
        st.write("")
        st.write("CountVectorizer() is used to convert preprocessed_text into numeric data by converting the text into a matrix of token (word) counts. We now have a sparse matrix of shape (3986, 6933), i.e. (n_samples, n_features).")
        st.write("We have built our model on a 80-20 train-test split for the vectorized matrix. To reduce the number of dimensions from 6933, Principle Component Analysis (PCA) is employed. The 95% rule is applied and it is found that 482 components are required to explain 95% of the variance in the dataset.")
        imagepp3 = Image.open("Streamlit/visualizations/scree_plot.png")
        st.image(imagepp3, use_column_width=True)
        st.write("Proportion of variance explained by first 5 components:")
        st.markdown("""
        🔹 PC1: 0.0928  
        🔹 PC2: 0.0729  
        🔹 PC3: 0.0598  
        🔹 PC4: 0.0549  
        🔹 PC5: 0.0335  
        ➡️ 9.28 + 7.29 + 5.98 + 5.49 + 3.35 ≈ 31.39%  
        """, unsafe_allow_html=True)
        st.write("Hence, no single component dominates, and variance is spread out across many components.")
        with open("Streamlit/visualizations/pca_plot.json", "r") as f:
            pca_plot_json = f.read()
            fig1 = pio.from_json(pca_plot_json)
        st.plotly_chart(fig1, use_container_width=True)
        

    with tab2:
        imageida4 = Image.open("Streamlit/visualizations/human_cloud.png")
        imageida5 = Image.open("Streamlit/visualizations/AI_CLOUD.png")
        imageida7 = Image.open("Streamlit/visualizations/TOPwordshuman.png")
        imageida8 = Image.open("Streamlit/visualizations/TOPwordsai.png")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h6 style='text-align: center;'>Top Words for Humans</h6>", unsafe_allow_html=True)
            st.image(imageida4, use_column_width=True)
            st.image(imageida7, use_column_width=True)
        with col2:
            st.markdown("<h6 style='text-align: center;'>Top Words for AI</h6>", unsafe_allow_html=True)
            st.image(imageida5, use_column_width=True)
            st.image(imageida8, use_column_width=True)
        st.write("")
        st.write("")
        st.write("**Distribution of Text Lengths (in Characters)**")
        col1, col2 = st.columns(2)
        imageida1 = Image.open("Streamlit/visualizations/AI_length_hist.png")
        with col1:
            st.image(imageida1, use_column_width=True)
        imageida2 = Image.open("Streamlit/visualizations/Human_length_hist.png")
        with col2:
            st.image(imageida2, use_column_width=True)
        st.write("Does a relation exist with the length of the question? Will 'question length' be a good distinguishing feature?")
        col1, col2 = st.columns(2)
        imageida3 = Image.open("Streamlit/visualizations/pairplot.png") 
        imageida6 = Image.open("Streamlit/visualizations/corr_heatmap.png")
        with col2:
            st.image(imageida3, use_column_width=True)
        with col1:
            st.image(imageida6, use_column_width=True)
        st.write("")
        st.write("")
        st.write("**Deep Diving into Human vs AI Similarity**")
        st.write("**Sentiment-Gap Analysis**: Are human responses more simple and those of AI more complex? Is there a difference in tone? Or perhaps a difference in how confident the answer sounds?")
        imageida9 = Image.open("Streamlit/visualizations/sent_dist.png") 
        imageida10 = Image.open("Streamlit/visualizations/sent_plot.png")
        col1, col2 = st.columns(2)
        with col1:
            st.image(imageida9, use_column_width=True)
        with col2:
            st.image(imageida10, use_column_width=True)
        st.write("")
        st.write("Is the human response easier to read than the AI one? We've used Readability and Lexical metrics like total words, total syllables and total sentences to compute the **Flesch Reading Ease Score**.") 
        imageida11 = Image.open("Streamlit/visualizations/FLesh_score.png")
        st.image(imageida11, use_column_width=True)
        st.write("")
        st.write("Employing the **Text-Similarity Analysis** to see if AI tends to say the same things people do. How close the words are between pairs of texts? More importantly, which type of response follows the original question's wording more closely?") 
        imageida12 = Image.open("Streamlit/visualizations/ANS_sim.png") 
        imageida13 = Image.open("Streamlit/visualizations/Q_sim.png")
        col1, col2 = st.columns(2)
        with col1:
            st.image(imageida12, use_column_width=True)
        with col2:
            st.image(imageida13, use_column_width=True)
        st.write("")


    with tab3:
        st.write("For comprehensive results, the performance of traditional classifiers and the deep neural network model BERT (Bidirectional Encoder Representations from Transformers) is evaluated on the training dataset.")
        st.write("**Best Model Overall:** BERT for accurately distinguising between the two classes with an accuracy of ...")
        tab1, tab2 = st.tabs(["Baseline Models: Traditional Classifiers", "Novel Model: BERT"])
        st.write("")  

        with tab1:  
            with open("Streamlit/model_results.pkl", "rb") as f:
                results = pickle.load(f)
            st.write("Seven classifiers were evaluated on the training set. Namely: **Logistic Regression, Linear SVM, Decision Tree, Random Forest, Gradient Boosting, K-Nearest Neighbors, Multi-layer Perceptron**.")
            st.write("Each model underwent hyperparameter tuning for the regularization strength, regularization parameter, maximum depth of tree, number of trees, number of boosting stages, learning rate, number of neighbors, size of hidden layers and L2 regularization term.")
            st.write("This was implemented with 5-fold cross validation to get the best parameters.")
            st.write("The results for each model are displayed below. The evaluation metrics used are accuracy, precision, recall, F1-score, with the mean accuracy and 95% confidence interval for the cross validation results.")
            imagemod1 = Image.open("Streamlit/visualizations/model_accuracy_plot.png")
            st.image(imagemod1, use_column_width=True)
            st.write("")
            selected_model = st.selectbox("**Selected Model**", list(results.keys()))
            model_result = results[selected_model]
            st.write("**Best Parameters:**", model_result["Best Parameters"])
            st.write(f"**Best Cross-Validation Accuracy:** {model_result['Best Cross-Validation Score']:.4f}")
            st.write(f"**Mean Accuracy (CV):** {model_result['Mean Accuracy']:.4f}")
            ci = model_result["95% Confidence Interval"]
            st.write(f"**95% Confidence Interval:** ({ci[0]:.4f}, {ci[1]:.4f})")
            st.write("**Test Set Classification Report**")
            test_df = pd.DataFrame(model_result["Test Report"]).transpose()
            st.dataframe(test_df.style.format({
                "precision": "{:.2f}",
                "recall": "{:.2f}",
                "f1-score": "{:.2f}",
                "support": "{:.0f}"
            }))
            st.write("**Train Set Classification Report**")
            train_df = pd.DataFrame(model_result["Train Report"]).transpose()
            st.dataframe(train_df.style.format({
                "precision": "{:.2f}",
                "recall": "{:.2f}",
                "f1-score": "{:.2f}",
                "support": "{:.0f}"
            }))

        with tab2:  
            st.write("novel model deets")
