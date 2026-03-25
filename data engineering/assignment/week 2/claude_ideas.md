Great question! Week 2 is different from Week 1 — there's **no AWS clicking required**. Here's exactly how to approach it:

**The key thing to understand first:** Week 2 is a *design and documentation* project. You are not building anything in AWS — you are acting like a data engineer who plans and documents a pipeline before it gets built.

Think of it like an architect drawing blueprints before construction starts.

---

**Here's how to start, in order:**

**Step 1 — Re-read the scenario (5 mins)**
Open your Week 2 brief. The company is now MarketFlow Property Intelligence receiving *daily* data feeds. Ask yourself: "Why can't someone just manually press run every day?" — that's the problem you're solving.

**Step 2 — Draw your DAG diagram first**
This is Deliverable 1 and it's the foundation everything else builds on. Go to **app.diagrams.net** (free, no account needed) and create 5 boxes connected by arrows:

> 📥 Validate Data → 🧹 Clean Data → ⚙️ Transform → 💾 Store Parquet → 🔍 Trigger Analytics

Label each box with the exact task names from the brief (e.g. `task_1_validate_data`). Label each arrow with the dependency reason.

**Step 3 — Write your Pipeline Workflow document**
Using your diagram as a guide, write a short document covering: DAG name, schedule (daily at 6am), and 2-3 sentences on what each task node does. Your Week 2 guide has a template for this.

**Step 4 — Write your Validation Logic**
Describe the 3 checks — Null Values, Duplicates, and Format Validation. For each one write: what it checks, the SQL logic, and what happens if it fails. The SQL examples are all in your guide.

**Step 5 — Write your Monitoring Plan**
Create a simple table covering the 3 alert types: Pipeline Failure, Missing Data, and Job Execution Error.

---

**Practical tip:** Start with the diagram today — once you can *see* the pipeline, writing about it becomes much easier. The whole project should take around 3-4 hours spread across a few sessions.

Would you like help creating the DAG diagram, or shall I help you draft the written documentation for any of the tasks?