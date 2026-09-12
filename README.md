# 🤖 InternPilot AI

### AI-Powered Internship Discovery, Evaluation & Tracking Assistant

> Built for the **AWS Agents for Humans Hackathon**

Internship searching is often scattered across multiple websites, difficult to evaluate, and time-consuming.

**InternPilot AI** is an AI-powered internship assistant that helps students **find, evaluate, rank, and track internship opportunities** through one intelligent workflow.

Instead of manually searching through hundreds of listings, students can enter what they are looking for and let InternPilot AI handle the discovery and evaluation process.

---

## 🚀 Links

👉 **[Live Demo](https://internpilot-ai.onrender.com)**

👉 **[GitHub Repository](https://github.com/shashikumarsinghai/InternPilot-AI)**

## 🎯 The Problem

Students often face several challenges while searching for internships:

- Internship opportunities are scattered across different websites.
- Students spend hours searching manually.
- It is difficult to determine whether an internship matches their skills.
- Comparing multiple opportunities takes time.
- Students lose track of applications after applying.

InternPilot AI brings these tasks together into a single workflow.

---

## 💡 The Solution

InternPilot AI combines:

- 🔎 **Web Search**
- 🤖 **AI Agent**
- 🧠 **Skill Evaluation**
- 📊 **Internship Ranking**
- 📌 **Application Tracking**
- 💬 **Natural-Language AI Assistant**

The goal is simple:

> **Search smarter. Apply better. Track everything.**

---

# 🚀 Key Features

## 1. 🔎 Intelligent Internship Search

InternPilot AI searches the web for current internship opportunities using **Tavily Search**.

The search can dynamically consider information such as:

- Internship role
- Location
- Skills
- Experience level
- Current internship opportunities

The system retrieves internship listings and presents them to the student.

---

## 2. 🧠 AI-Based Internship Evaluation

Each internship can be evaluated against the student's profile.

InternPilot AI analyzes:

- Required skills
- Student skills
- Location compatibility
- Experience requirements
- Overall compatibility

The system calculates a **match score** to help students understand how suitable an internship is.

### Example

```text
Internship: Python Developer Intern

Student Skills:
Python, Flask, Git, SQL

Required Skills:
Python, Flask, Django, SQL

Match Score: 76%

Matched Skills:
Python
Flask
SQL

Missing Skills:
Django

```

---

## 3. 📊 Internship Ranking

After evaluating internships, InternPilot AI ranks them based on their match score.

### Example

| Rank | Internship | Match Score |
|------|------------|-------------|
| 🥇 1 | Python Developer Intern | 92% |
| 🥈 2 | Backend Developer Intern | 84% |
| 🥉 3 | Software Engineer Intern | 76% |
| 4 | Web Developer Intern | 61% |

This allows students to focus on the most relevant opportunities first.

---

## 4. 📌 Internship Tracker

Students can save internship opportunities and track their application progress.

### Supported statuses include:

- Saved
- Applied
- Interview
- Offer
- Rejected

### Example Workflow

```text
Internship Found
      ↓
    Saved
      ↓
   Applied
      ↓
  Interview
      ↓
    Offer
```

The tracker helps students maintain their internship application pipeline in one place.

---

## 5. 🤖 AI Internship Assistant

InternPilot AI also provides a natural-language AI assistant.

### Students can ask questions such as:

```text
Find Python internships in Bangalore
```

or

```text
Find frontend internships for students with JavaScript skills
```

The AI agent understands the request and can search for relevant internship opportunities.

The assistant is powered by:

- **Strands Agents SDK**
- **Mistral AI**
- **Tavily Search**

---

# 🏗️ How the AI Agent Works

The core workflow of InternPilot AI is:

```text
Student
   ↓
Web Interface
   ↓
Flask Backend
   ↓
Strands AI Agent
   ↓
Mistral Model
   ↓
Internship Search Tool
   ↓
Tavily Web Search
   ↓
Internship Results
   ↓
Evaluation
   ↓
Ranking
   ↓
Student
```

The AI agent can decide when to use the internship search tool based on the student's request.

This makes the system more than a simple chatbot: it performs an actual task by searching for real internship opportunities.

---

# ☁️ AWS & Strands Agents

InternPilot AI was built for the **AWS Agents for Humans Hackathon** and uses the **Strands Agents SDK** for its AI-agent workflow.

## Strands Agents

The Strands Agents SDK is used to create the AI agent that can:

1. Understand the student's request.
2. Decide when an internship search is required.
3. Call the internship search tool.
4. Receive search results.
5. Return the results to the student.

## AI Model

The project uses:

```text
Mistral — ministral-3b-2512
```

## Web Search

Internship discovery is powered by:

```text
Tavily Search API
```

The combination of **Strands Agents + Mistral + Tavily** allows InternPilot AI to perform a real-world internship discovery workflow.

---

# 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend and application logic |
| Flask | Web application backend |
| HTML | Frontend structure |
| CSS | Frontend styling |
| JavaScript | Frontend interactions |
| Bootstrap | Responsive UI components |
| Strands Agents SDK | AI agent framework |
| Mistral AI | Large language model |
| Tavily | Web search and internship discovery |
| JSON | Internship tracking data |
| Git | Version control |
| GitHub | Source code hosting |

---

# 📁 Project Structure

```text
InternPilot-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── tracked_internships.json
│
├── services/
│   ├── __init__.py
│   ├── agent.py
│   ├── evaluator.py
│   ├── ranker.py
│   ├── search.py
│   └── tracker.py
│
├── templates/
│   └── index.html
│
└── static/
    ├── script.js
    └── style.css
```

---

# 📄 Important Files

| File | Purpose |
|------|---------|
| `app.py` | Flask application and API routes |
| `services/agent.py` | Strands AI agent and search tool |
| `services/search.py` | Internship web search |
| `services/evaluator.py` | Internship skill and profile evaluation |
| `services/ranker.py` | Internship ranking |
| `services/tracker.py` | Internship saving and application tracking |
| `templates/index.html` | Main web interface |
| `static/style.css` | Application styling |
| `static/script.js` | Frontend logic and API communication |
| `tracked_internships.json` | Saved internship tracking data |

---

# 🔄 Application Workflow

```text
1. Student opens InternPilot AI
              ↓
2. Student enters internship preferences
              ↓
3. Flask receives the request
              ↓
4. Strands AI Agent processes the request
              ↓
5. Agent uses the internship search tool
              ↓
6. Tavily searches the web
              ↓
7. Internship opportunities are collected
              ↓
8. Internships are evaluated against the student profile
              ↓
9. Internships are ranked by match score
              ↓
10. Results are displayed to the student
              ↓
11. Student can save and track applications
```

---

# 💻 Running the Project Locally

## 1. Clone the Repository

```bash
git clone https://github.com/shashikumarsinghai/InternPilot-AI.git
cd InternPilot-AI
```

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
TAVILY_API_KEY=your_tavily_api_key
MISTRAL_API_KEY=your_mistral_api_key
AWS_REGION=us-east-1
```

Do not commit your `.env` file to GitHub.

## 5. Run the Application

```powershell
python app.py
```

The application will run locally at:

```text
http://127.0.0.1:5000
```

Open the address in your browser.

---

# 🧪 Example

A student can search for:

```text
Role: Python Developer Intern
Location: Bangalore
Skills: Python, Flask, SQL, Git
Experience: Beginner
```

InternPilot AI searches for relevant internships and evaluates the opportunities.

### Example Result

```text
Python Backend Intern

Match Score: 92%

Matched Skills:
Python
Flask
SQL
Git

Location Score:
100%

Recommendation:
Excellent Match
```

The student can then:

```text
View Internship
      ↓
Save Internship
      ↓
Apply
      ↓
Update Status
```

---

# 🎯 Why We Built It

We built InternPilot AI because finding an internship should not require students to spend hours searching through scattered opportunities.

Students should be able to:

> **Tell an AI agent what they are looking for and let it do the searching and evaluation work.**

InternPilot AI focuses on turning internship discovery into a more intelligent and organized workflow.

The project also gave us an opportunity to explore how AI agents can perform practical tasks instead of only generating text.

---

# 👥 Team

Built by our team of four:

1. **Shashi Kumar Singh** — @shashisingh72048
2. **Krish Kumar Pathak** — @krishpandit780
3. **PRIYANSHU** — @boyp48440
4. **Shivam Kumar Pathak** — @sp0242108

---

# 🏆 Hackathon

This project was built for the:

## AWS Agents for Humans Hackathon

The project focuses on building an AI agent that performs useful real-world work using the **Strands Agents SDK**.

## Our Goal

To demonstrate how an AI agent can help students with a practical problem:

> **Finding and managing internship opportunities.**

---

# 🔐 Security

Sensitive API keys are stored in environment variables.

The project uses:

```text
.env
```

for local secrets.

The `.gitignore` file prevents sensitive files such as `.env` and the virtual environment from being committed to GitHub.

**Never share API keys publicly.**

---

# 📜 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

# ❤️ Final Note

InternPilot AI is built with one simple idea:

> **Finding an internship should be easier, smarter, and more organized.**

Instead of manually searching, comparing, and tracking opportunities across different platforms, InternPilot AI brings the workflow together with an AI agent.

## InternPilot AI

**Search smarter. Apply better. Track everything. 🚀**