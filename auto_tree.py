import os
os.environ["PATH"] += os.pathsep + '/opt/homebrew/bin'
import re
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv("api.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import ast
from graphviz import Digraph

def get_ai_feedback(code):
    print("Analyzing code.....")
    
    prompt = f"""
    Analyze the following Python code for errors. 
    Return ONLY a comma-separated list of line numbers that have issues.
    If there are no errors, return 0.
    
    Code:
    {code}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role": "user", "content": prompt}],
            temperature=0 #to get consistency in outputs due to hallucinations
        )
        
        # Extract the text answer (e.g., "3")
        result_text = response.choices[0].message.content.strip()

        print(f"AI Response: {result_text}")
        line_numbers = re.findall(r'\d+', result_text)

        return [int(n) for n in line_numbers]
        
    except Exception as e:
        print(f"Brain Error: {e}")
        return []
def draw_ast(code):
    tree=ast.parse(code)
    dot=Digraph(comment="Automated AST")
    error_lines = get_ai_feedback(code)
    def add_node(node):
        node_id=str(id(node))
        label=type(node).__name__
        line_no=getattr(node,'lineno','none')
        color="lightblue"
        if line_no in error_lines:
            color='red'
            label+=f'\n (Line:{line_no})'
        dot.node(node_id,label,style='filled',fillcolor=color)
        for child in ast.iter_child_nodes(node):
            child_id=str(id(child))
            add_node(child)
            dot.edge(node_id,child_id)
    add_node(tree)
    dot.render('auto_ast_result', format='png', cleanup=True)
    print("Look for a file named 'auto_ast_result.png' now!")

if __name__ == "__main__":
    
    my_code = """def calculate(x, y):
    z = x + y
    result = x / y  # Division by zero if y=0
    unused_var = 10
    return result

calculate(5, 0)
print(undefined_variable)"""
   

    
  

    draw_ast(my_code)







