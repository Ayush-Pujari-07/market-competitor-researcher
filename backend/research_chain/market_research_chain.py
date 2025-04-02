import os
import json
import logging

from exa_py import Exa
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.passthrough import RunnablePassthrough


os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

GPT_MINI = "gpt-4o-mini"
GPT4 = "gpt-4o"


logger = logging.getLogger(__name__)

WRITER_SYSTEM_PROMPT = """
As the AI-assisted strategy designer for a companies brand strategy framework, your task is to conduct an in-depth market research report tailored for a specific industry or business. Follow the protocols below to ensure a comprehensive and insightful report:

1. **Purpose of the Research**: Clearly define the purpose of the research. What specific questions are you aiming to answer?
2. **Clarity of Objectives**: State the research objectives upfront. What are the key areas you aim to uncover or validate?
3. **Market Landscape**: Provide a detailed snapshot of the current market landscape relevant to the specific industry or business.
4. **Actionable Insights**: Deliver deep, actionable insights that can inform strategic decisions.
5. **External Factors**: Consider and analyze external factors that may impact the market.
6. **Ethical Considerations**: Ensure the research follows ethical guidelines and standards.
7. **Communication of Findings**: Present the findings in a compelling and accessible manner.

Utilize your extensive knowledge base and available online resources to produce a thorough market research report that addresses all the elements above effectively.
"""


RESEARCH_REPORT_TEMPLATE = """
Information:
--------
{research_summary}
--------
Using the above information, answer the following question or topic in a detailed report:
"{question}"

-- \
The report should focus on the answer to the question, should be well structured, informative, \
in-depth, with facts and numbers if available, long report that is very verbose and not less than 3,000 tokens or 4,000 words.
You should strive to write the report as long as you can using all relevant and necessary information provided.
Continuously review and analyze your actions to ensure you are performing to the best of your abilities.
Constructively self-criticize your big-picture behavior constantly.
You must write the report with markdown syntax.
You MUST determine your own concrete and valid opinion based on the given information. Do NOT defer to general and meaningless conclusions.
Write all used source URLs at the end of the report, and make sure to not add duplicated sources, but only one reference for each.
You must write the report in apa format.
Please do your best, this is very important to my career.
No Talking."""

SUMMARY_TEMPLATE = """
{text}

----------
Using the above text, answer the following question:

> {question}

----------
If the question cannot be answered using the text, provide a comprehensive summary instead.

**Summary Requirements:**

1. **Factual Information**: Include all available facts, numbers, and statistics.
2. **Customer Pain Points**: Identify and summarize the key pain points of customers in this domain.
3. **Market Influencers**: Highlight the key drivers and restraints influencing this market.
4. **Market Size and Growth**: Provide information on the current size and projected growth of the [specific market/industry].
5. **Market Leaders**: Identify the leading players in the market and what sets them apart.
6. **Emerging Challengers**: Note any emerging challengers or disruptors showing potential.
7. **Key Differentiators**: Summarize the key differentiators among the top contenders in the market.

Ensure the summary considers all the mentioned conditions and is at least 1,000 tokens in length.

No Talking.
"""


def web_search(query: str):
    exa = Exa(api_key=os.environ.get("EXA_API_KEY"))
    # can change the number of results, if we are using 10 the final input tokens are 57k
    exa_response = exa.search_and_contents(query, num_results=2)

    return [result.text for result in exa_response.results]


SUMMARY_PROMPT = ChatPromptTemplate.from_template(SUMMARY_TEMPLATE)
logger.debug(f"Summary prompt: {SUMMARY_PROMPT}")

# Updated scrape_and_summarize_chain to handle text directly
scrape_and_summarize_chain = RunnablePassthrough.assign(
    summary=RunnablePassthrough.assign(
        text=lambda x: x["text"][:5000]
    )  # Here also 5000 can be chaneged based on the token input and response generation length
    | SUMMARY_PROMPT
    | ChatOpenAI(model=GPT_MINI, temperature=1)
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
            "Write 3 google search queries to search online that form an "
            "objective opinion from the following: {question}\n"
            "You must respond with a list of strings in the following format: "
            '["query 1", "query 2", "query 3"].',
        ),
    ]
)


search_question_chain = (
    SEARCH_PROMPT
    | ChatOpenAI(model=GPT4, temperature=0)
    | StrOutputParser()
    | json.loads
)

full_research_chain = (
    search_question_chain
    | (lambda x: [{"question": q} for q in x])
    | web_search_chain.map()
)

logger.debug(f"Full research chain: {full_research_chain}")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", WRITER_SYSTEM_PROMPT),
        ("user", RESEARCH_REPORT_TEMPLATE),
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
        research_summary=full_research_chain | collapse_list_of_lists
    )
    | prompt
    | ChatOpenAI(model=GPT4, temperature=0.9)
    | StrOutputParser()
)
logger.debug(f"Chain: {chain}")
