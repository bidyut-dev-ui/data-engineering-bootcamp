from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.schema import HumanMessage, SystemMessage

def demo_prompt_templates():
    """Demonstrate prompt templates"""
    print("=== Prompt Templates ===\n")
    
    # Simple template
    template = PromptTemplate(
        input_variables=["product", "audience"],
        template="Write a marketing tagline for {product} targeting {audience}."
    )
    
    prompt = template.format(product="eco-friendly water bottle", audience="millennials")
    print("Generated Prompt:")
    print(prompt)
    print()
    
    # Chat template
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful data analyst assistant."),
        ("human", "Explain {concept} in simple terms.")
    ])
    
    messages = chat_template.format_messages(concept="data normalization")
    print("Chat Messages:")
    for msg in messages:
        print(f"{msg.type}: {msg.content}")

def demo_few_shot():
    """Demonstrate few-shot prompting"""
    print("\n=== Few-Shot Prompting ===\n")
    
    examples = """
Example 1:
Input: "The sales increased by 50%"
Sentiment: Positive

Example 2:
Input: "We lost 3 major clients"
Sentiment: Negative

Example 3:
Input: "Revenue remained stable"
Sentiment: Neutral
"""
    
    template = PromptTemplate(
        input_variables=["text"],
        template=examples + "\nNow analyze:\nInput: \"{text}\"\nSentiment:"
    )
    
    prompt = template.format(text="Our new product launch exceeded expectations")
    print(prompt)

def demo_chain_of_thought():
    """Demonstrate chain-of-thought prompting"""
    print("\n=== Chain-of-Thought Prompting ===\n")
    
    template = PromptTemplate(
        input_variables=["question"],
        template="""
Let's solve this step by step:

Question: {question}

Step 1: Identify what we know
Step 2: Determine what we need to find
Step 3: Apply the appropriate method
Step 4: Calculate the result

Solution:
"""
    )
    
    prompt = template.format(
        question="If a dataset has 1000 rows and we use 80/20 train/test split, how many rows are in the test set?"
    )
    print(prompt)

def main():
    print("=== LangChain Basics (No LLM Required) ===\n")
    print("This tutorial demonstrates LangChain concepts without requiring an LLM API.\n")
    
    demo_prompt_templates()
    demo_few_shot()
    demo_chain_of_thought()
    
    print("\n✓ Tutorial complete!")
    print("\nNote: To use with actual LLMs, you would:")
    print("1. Install: pip install langchain-openai (or other provider)")
    print("2. Set API key: export OPENAI_API_KEY='your-key'")
    print("3. Create LLM: llm = ChatOpenAI()")
    print("4. Run chain: chain = LLMChain(llm=llm, prompt=template)")

if __name__ == "__main__":
    main()
