# ⚽ EPL Nerd: AI-Powered Premier League Analyst

This is built f or Final Project submission for LLMBased Tools and Gemini API Integration for Data Scientists course organized by Hacktiv8.

EPL Nerd is an intelligent conversational agent that allows you to query, analyze, and visualize English Premier League data using natural language. Built with **Streamlit**, **LangChain**, and powered by **Groq's Llama 3 models**, this app bridges the gap between complex database queries and simple human questions.

## 🚀 Key Features

* **Conversational SQL:** Ask questions like *"Who is the top scorer for 2024-25?"* and the AI will automatically generate and execute the SQL query for you.
* **Data Visualization:** Automatically renders bar charts when you ask for graphs or trends.
* **Conversational Memory:** Remembers your previous questions to provide context-aware answers.
* **Multilingual Support:** Responds fluently in casual Indonesian.
* **Season-Aware:** Smart filtering and aggregation for specific Premier League seasons.

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **AI Engine:** [Groq Cloud](https://groq.com/) (Llama 3.3-70b-versatile)
* **Orchestration:** [LangChain](https://www.langchain.com/)
* **Database:** [Supabase](https://supabase.com/) (PostgreSQL)
* **Data Processing:** [Pandas](https://pandas.pydata.org/)

## ⚙️ Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/epl-nerd.git
cd epl-nerd

```


2. **Install the dependencies:**
```bash
pip install -r requirements.txt

```


3. **Configure Secrets:**
Create a directory named `.streamlit` and a file named `secrets.toml` inside it:
```toml
# .streamlit/secrets.toml
DATABASE_URL = "postgresql://user:password@your-db-url:port/dbname"
GROQ_API_KEY = "gsk_your_groq_api_key_here"

```


> **Warning:** Never commit your `secrets.toml` file to GitHub! Add it to your `.gitignore` file immediately.


4. **Run the app:**
```bash
streamlit run app.py

```



## 💡 How to Use

Once the app is running, try asking:

* *"Siapa pencetak gol terbanyak musim 2024-25?"*
* *"Buatkan grafik 10 besar assist musim 2024-25"*
* *"Bandingkan jumlah gol antara Erling Haaland dan Mohamed Salah"*

## 📝 Troubleshooting

* **Rate Limits:** If you hit a 429 Error, it means you've reached your daily token limit on Groq. Switch to a smaller model (like `llama-3.1-8b-instant`) in your code or wait for your quota to reset.
* **Data Accuracy:** Ensure your database column names match the agent's schema. If you encounter issues, ask the bot: *"What tables do you have?"* to verify its current knowledge.

## 🤝 Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a pull request.

---

*Built with passion for football and code. ⚽*
