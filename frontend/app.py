import streamlit as st
import httpx
import asyncio


API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Scientific Calculator", page_icon="🧮")
st.title("Scientific Calculator")
st.title("🧮 Scientific Calculator (Async)")

# ---------- ASYNC CALL ----------
async def calculate(operation, payload):
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{API_URL}/calculate",
            params={"operation": operation},
            json=payload
        )
        return res


async def fetch_history():
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{API_URL}/history")
        return res.json()


async def clear_history():
    async with httpx.AsyncClient() as client:
        await client.delete(f"{API_URL}/history")



#
# st.markdown(
#     """
#     <style>
#     div.stButton > button {
#         background-color: #4CAF50;
#         color: white;
#         border-radius: 10px;
#         height: 3em;
#         width: 100%;
#     }
#
#     input {
#         border-radius: 8px !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# ---------- UI ----------
operation = st.selectbox(
    "Select Operation",
    ["add", "subtract", "multiply", "divide", "power", "sqrt"]
)

if operation == "sqrt":
    a = st.number_input("Enter number", value=0.0)
    payload = {"a": a}
else:
    a = st.number_input("Enter first number", value=0.0)
    b = st.number_input("Enter second number", value=0.0)
    payload = {"a": a, "b": b}

if st.button("Calculate"):
    response = asyncio.run(calculate(operation, payload))

    if response.status_code == 200:
        st.success(f"Result: {response.json()['result']}")
    else:
        st.error(response.json()["detail"])


st.divider()
st.subheader("📜 Calculation History")

if st.button("Load History"):
    history = asyncio.run(fetch_history())
    st.table(history)

if st.button("Clear History"):
    asyncio.run(clear_history())
    st.success("History cleared")
