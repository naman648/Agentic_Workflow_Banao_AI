# 🤖 LangGraph Agentic Workflow Playground

A powerful agentic workflow powered by **LangGraph**, **Groq's LLaMA 3**, and **Streamlit**. This app demonstrates how agents can collaborate to plan, execute, and reflect on user queries in a visually interactive manner.

---

## 📸 Demo

<!-- Add your GIF or image demo -->
![Workflow Demo](demo.gif)

---

## 🚀 Features

- 🌐 Agentic workflow using LangGraph  
- ⚡ Lightning-fast inference via Groq API (LLaMA 3)  
- 🧠 Plan ➡️ 🛠️ Execute ➡️ 🪞 Reflect loop  
- 🎨 Light/Dark theme toggle (in-progress)*
- 👥 Avatars for agents and interactive Streamlit UI  
- 📊 Debug output and expandable logs  

---

## 🛠️ Technologies Used

- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Groq](https://console.groq.com/)
- [Streamlit](https://streamlit.io/)
- [Python 3.10+](https://www.python.org/downloads/release/python-3132/)

---

## 🧰 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/langgraph-agentic-workflow.git
cd langgraph-agentic-workflow
```
### 2. Create a Virtual Environment
```bash
python -m venv venv
# Activate the environment:
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```
### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
### 4. Add Your Groq API Key
Create a .env file in the root directory with the following:
```bash
GROQ_API_KEY="your_groq_api_key_here"
```
---
### 🧪 Run the App

```bash
streamlit run app.py
```
Visit http://localhost:8501 in your browser.

---

### 🗺️ Workflow Overview
```bash
    A[User Query] --> B(PlanAgent 🧠);
    B --> C{ToolAgent 🛠️};
    C --> D[ReflectionAgent 💡];
    D --> E(Repeat (Max 3x)) | Yes | B;
    D --> F[Stop | E[Final Feedback]];
```
---

### 📂 Folder Structure

```bash
├── app.py               # Main Streamlit app
├── .env                 # Contains your GROQ_API_KEY
├── requirements.txt     # Python dependencies
├── README.md            # You're here!
```
---

### 📌 Notes

- The workflow loops up to 3 times through Plan ➡️ Tool ➡️ Reflect.
- You can modify the LLM model (llama3-8b-8192) inside the ask_groq() function.
- Customize agents or workflow edges by modifying app.py.

---

### 📄 License
This project is licensed under the MIT License. Feel free to fork and build upon it!

---

### 💡 Author
Crafted with ❤️ by Naman Verma
