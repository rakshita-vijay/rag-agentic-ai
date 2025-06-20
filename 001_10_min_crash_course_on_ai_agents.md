## 3 things: LLMs, AI Workflows, AI Agents

---

when we ask LLMs to give us an answer to something, if it not available to them (personal info/company data), then we can provide access to this info by introducing a 'control logic'
  - 'control logic': allows access to specified sites/external things to search for the response there

but at the end of the day, we cannot give access to everything in the world
<br>although vast, it is a 'limited' access

---

- thus, we use RAG (Retrieval Augmented Generation)
  - helps AI models 'look things up' before they answer
  - it is AI workflow, basically

---

the human gives the input to the ai, defining steps: A, B, C
but, what if:
- we ask a question to an AI
- then THE AI DEFINES STEPS ABC
- ai executes said self-defined steps
- gives us the final responses without the intermediate (the ai does it all for us)
- 
--> "thinking", "doing" things by itself

---

## ReAct (framework) = Reason + Act

---

instead of human iterating over the responses it gets from performing 20 user-defined steps, the agent will include a "critique bot" of sorts to critque its own work, then send to the user
                                                                                                                    (maybe until a set of "best practices" criteria are met)
so reasoning + acting + iterating
