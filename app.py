import gradio as gr
from query import ask

def handle_query(question):
    if not question.strip():
        return "", ""
    result = ask(question)
    sources = "\n".join(f"  {s}" for s in result["sources"])
    return result["answer"], sources

with gr.Blocks(title="UCLA Dining Guide") as demo:
    gr.Markdown("## UCLA Unofficial Dining Guide\nAsk anything about UCLA dining halls, meal plans, and food options.")
    inp = gr.Textbox(label="Your question", placeholder="e.g. Which dining hall is best for vegetarians?")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=4)
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch(share=True)