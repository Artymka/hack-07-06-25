from langchain_gigachat import GigaChat
from sqlalchemy import create_engine, text, MetaData, inspect
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore
from langchain_core.runnables.config import RunnableConfig
from langgraph.constants import Send
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote
import re

from IPython.display import Image, display

from jinja2 import Template
from pydantic import BaseModel, Field
from typing import Annotated, Any, Optional, List, Literal
from typing_extensions import TypedDict
import os
import operator
import uuid
import builtins

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


llm = GigaChat(
    model='GigaChat-2-Max',
    credentials = 'OWU5ZDgyMWItZDc4MS00ODZiLTg0M2UtZWVlMTEyMGIyZDhiOjU1MDg5ZTZhLTQyZjQtNDNjOS1hMTVjLTdlN2Q4ODI2ZjM3NA==',
    verify_ssl_certs=False
)

class State(TypedDict):
    messages: list
    message_type: str | None        
    access: str | None              
    web_search_context: str | None
    nl2sql_context: str | None

class MessageClassifier(BaseModel):
    message_type: Literal['formal', 'informal'] = Field(
        ...,
        description = 'Классификация'
   )

class MessageClarifier(BaseModel):
    message_type: Literal['NO', 'YES'] = Field(
        ...,
        description = 'Классификация'
   )

parser_classify = PydanticOutputParser(pydantic_object=MessageClassifier)
parser_clarify = PydanticOutputParser(pydantic_object=MessageClarifier)