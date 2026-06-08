import gradio as gr

print("Starting app...")

try:
    from query import ask
    print("Query module loaded")
except Exception as e:
    import traceback
    print("ERROR loading query module:")
    traceback.print_exc()
    raise

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"- {s}" for s in result["sources"])
    return result["answer"], sources

print("Building interface...")

with gr.Blocks(title="Howard Housing Guide") as demo:
    gr.Markdown("# Howard University Off-Campus Housing Guide")
    gr.Markdown("Ask anything about off-campus housing near Howard based on real student reviews and Reddit threads.")
    
    inp = gr.Textbox(label="Your question", placeholder="e.g. Is Trellis House worth it?")
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=3)
    
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

print("Launching...")
demo.launch(debug=True)