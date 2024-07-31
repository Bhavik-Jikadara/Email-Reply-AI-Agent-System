# Email Reply AI Agent System

Email Reply System AI Agent streamlines email management by automating repetitive tasks, prioritizing incoming messages, and providing intelligent responses, ultimately saving users time and enhancing productivity.

<div align="center"><img src="https://i.ytimg.com/vi/fKMHKlO-sE4/sddefault.jpg"></div>

---

## Notes: This step is very import:

### click below links to set two API_KEYs in the Environment Variable, and use this link as a reference.

- [TAVILY_API_KEY](https://app.tavily.com/)  
   $ TAVILY_API_KEY="Your-API-key"

- [GROQ_API_KEY](https://console.groq.com/keys)  
   $ GROQ_API_KEY="Your-API-key"

---

### Step 1: Clone the repository

```
    $ git clone https://github.com/Bhavik-Jikadara/Email-Reply-System.git
    $ cd Email-Reply-System/
```

### Step 2: Create a virtualenv (windows user)

```
    $ pip install virtualenv
    $ virtualenv venv
    $ source venv/Scripts/activate
```

### Step 3: Rename of .env.example filename to .env file and add api keys

```
    $ GROQ_API_KEY=""
    $ TAVILY_API_KEY=""
```

### Step 4: Install the requirements libraries using pip

```
    $ pip install -r requirements.txt
```

### Step 5: Run the project:

```
    $ streamlit run app.py
```
