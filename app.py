import streamlit as st
from src.build_graph import app

st.title("Email Reply System")

email = st.text_area(
    label="Enter the Email",
    placeholder="""Hi, Bhavik!

It’s Day 2 of your automation adventure with Apify, and it's time to connect the dots! Integrating your Actors with other solutions you use opens up a world of possibilities, making your workflows smarter and your life easier.

Have fun!

The Bhavik Team
    """,
    height=400
)

# run the agent
inputs = {"initial_email": email,"research_info": None, "num_steps":0}

def run():
    if st.button("Email Reply"):
        for output in app.stream(inputs):
            for key, value in output.items():
                print(f"Finished running: {key}:")

        output = app.invoke(inputs)
        st.write(output['final_email'])

if __name__ == "__main__":
    run()