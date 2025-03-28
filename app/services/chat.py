
from ..constants import *
from ..repository import base
from ..models import User, Chat
from ..helpers import add_record_to_database
import zlib
import jsonpickle
from langchain_core.messages import HumanMessage
from langgraph.graph.state import CompiledStateGraph 
from .graph import get_graph

def get_user_chats(id: int):
    chats = base.get_records_by_field(Chat, "user_id", id)
    return {'chats' : [chat.serialize_without_graph() for chat in chats]}

def start_chat(request):
    stock = request.get('stock')
    user_id = request.get("user_id")

    graph = get_graph()

    state = graph.invoke({'messages' : [HumanMessage(content=f"{stock}")]})

    analysis = state['messages'][-1].content

    # c = compress_data(graph)
    # print(compress_data(c))
    # e = jsonpickle.decode(zlib.decompress(c).decode("utf-8"))
    # print(type(e))

    if user_id:
        chat = Chat(user_id=user_id, title=stock, graph=compress_data(graph), memory=compress_data([{'AI': analysis}]))
        add_record_to_database(chat)
        return {"analysis": analysis, "chat_id": chat.id, "predicted_prices": state['predicted_prices'], "stock_prices":state['stock_prices'] }

    return {"analysis": analysis}

   
def continue_chat(request):
    query = request.get('query')
    chat_id = request.get("chat_id")

    chat = base.get_record_by_field(Chat, "id", chat_id)

    serialized_chat = chat.serialize()

    graph = serialized_chat['graph']

    state = graph.invoke({'messages' : [HumanMessage(content=query)], 'follow_up': query, 'end_chat': False})

    response = state['messages'][-2].content

    updated_memory = serialized_chat['memory'].append([{'User': query}, {'AI': response}])

    chat.update_memory(updated_memory)
    chat.update_graph(graph)

    return{"response": response, "chat_history": updated_memory}
    

def get_graph_configuration(thread_id: int):
    return {"configurable": {"thread_id": f"{thread_id}"}}

def compress_data(data):
    string_data = jsonpickle.encode(data).encode()
    return zlib.compress(string_data)
    
    

