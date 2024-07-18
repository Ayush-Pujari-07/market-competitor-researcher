import os
import json
import logging

from exa_py import Exa
from dotenv import load_dotenv, find_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.passthrough import RunnablePassthrough

os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")


GPT3 = "gpt-3.5-turbo-0125"
GPT4 = "gpt-4o"


logger = logging.getLogger(__name__)


WRITER_SYSTEM_PROMPT = """As the AI-assisted strategy designer for an companies brand strategy framework, your task is to create an in-depth competitor analysis report. Begin with a clear snapshot of the current market landscape tailored for a specific industry or business. Follow these protocols strictly to ensure a high-quality analysis:

1. **Define the Purpose:**
   - What is the purpose of the research?
   - What specific questions does the research intend to answer?

2. **Clarity and Focus:**
   - Ensure the research defines its purpose upfront.
   - Be clear about what the research aims to uncover or validate.

3. **Comprehensive Analysis:**
   - Create a detailed and extensive competitor analysis.
   - Include all relevant elements in a balanced manner.
   - Provide deep, actionable insights.
   - Consider external factors influencing the market.

4. **Ethical Considerations:**
   - Ensure clear ethical considerations are included.

5. **Effective Communication:**
   - Communicate findings compellingly and accessibly.
   - Use clear, concise, and well-structured language.

6. **Utilize Resources:**
   - Leverage your vast knowledge base.
   - Browse online resources to gather up-to-date information.

Your report should be long, comprehensive, and cover all these elements effectively. Rethink and revise your analysis as needed to ensure it meets these standards and provides valuable insights for companies strategy framework."""


COMPETITOR_ANALYSIS_REPORT_TEMPLATE = """Information:
--------
{research_summary}
--------
Using the above information, write a detailed competitor analysis report on the following question or topic:
"{question}"

-- 
The report should be:

1. **Well-structured:** Organize the report logically with clear headings and subheadings.
2. **Informative and In-depth:** Provide comprehensive insights with relevant facts, numbers, and statistics.
3. **Verbose and Lengthy:** Aim for a report length of at least 2000 tokens, but strive to include all relevant and necessary information to make it as long and thorough as possible.
4. **Analytical:** Continuously review and analyze your content to ensure high-quality performance.
5. **Self-critical:** Constructively self-criticize to improve the overall quality of the report.
6. **Markdown Syntax:** Write the report using markdown syntax for clear formatting.

**Key Points to Cover:**
- Your concrete and valid opinion based on the given information.
- Avoid general and meaningless conclusions.
- Ensure the report is directly answering the question or addressing the topic with depth and clarity.

This report is crucial for my career, so please put in your best effort to deliver an outstanding analysis."""

SUMMARY_TEMPLATE = """{text}

----------
Using the above text, answer the following question:

> {question}

----------
If the question cannot be answered using the text, provide a comprehensive summary of the text.
Ensure to include the following details if available:
- All factual information, including numbers and statistics.
- Key drivers and restraints influencing the market.
- Current size and projected growth of the specific market/industry.
- Leading players in the market and what sets them apart.
- Emerging challengers or disruptors showing potential.
- Key differentiators among the top contenders in the market.

Create summaries considering all the mentioned conditions. Ensure the summaries are no less than 1000 tokens in length.
"""


def web_search(query: str):
    exa = Exa(api_key=os.environ.get("EXA_API_KEY"))
    exa_response = exa.search_and_contents(query, num_results=2)

    return [result.text for result in exa_response.results]


SUMMARY_PROMPT = ChatPromptTemplate.from_template(SUMMARY_TEMPLATE)
logger.debug(f"Summary prompt: {SUMMARY_PROMPT}")

# Updated scrape_and_summarize_chain to handle text directly
scrape_and_summarize_chain = RunnablePassthrough.assign(
    summary=RunnablePassthrough.assign(
        text=lambda x: x["text"][:3000])  # Directly use the text from exa
    | SUMMARY_PROMPT
    | ChatOpenAI(model=GPT3, temperature=1)
    | StrOutputParser()
) | (lambda x: f"TEXT: {x['text']}\n\nSUMMARY: {x['summary']}")

# Updated web_search_chain to handle texts instead of URLs
web_search_chain = (
    RunnablePassthrough.assign(texts=lambda x: web_search(x["question"]))
    | (lambda x: [{"question": x["question"], "text": t} for t in x["texts"]])
    | scrape_and_summarize_chain.map()
)


SEARCH_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "user",
            "Create 3 targeted Google search queries to gather information and form an objective opinion on the following topic: {question}\n"
            "Please respond with a list of strings in the following format: "
            '["query 1", "query 2", "query 3"].',
        ),
    ]
)


search_question_chain = SEARCH_PROMPT | ChatOpenAI(
    model=GPT4, temperature=0) | StrOutputParser() | json.loads

full_research_chain = search_question_chain | (
    lambda x: [{"question": q} for q in x]) | web_search_chain.map()

logger.debug(f"Full research chain: {full_research_chain}")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", WRITER_SYSTEM_PROMPT),
        ("user", COMPETITOR_ANALYSIS_REPORT_TEMPLATE),
    ]
)

logger.debug(f"Prompt: {prompt}")


def collapse_list_of_lists(list_of_lists):
    """
    Collapses a list of lists into a single list of strings, where each string represents a concatenation of the elements in a sublist, separated by two newline characters.

    Args:
        list_of_lists (list of lists): The list of lists to collapse.

    Returns:
        list of str: The collapsed list of strings.
    """
    return ["\n\n".join(sublist) for sublist in list_of_lists]


chain = (
    RunnablePassthrough.assign(
        research_summary=full_research_chain | collapse_list_of_lists)
    | prompt
    | ChatOpenAI(model=GPT4, temperature=0.9)
    | StrOutputParser()
)
logger.debug(f"Chain: {chain}")
