import streamlit as st
from real_time_scheduling import Task, rm_schedule, create_gantt_chart

def main():
    st.title("Rate Monotonic Scheduling Simulator")
    st.markdown("### Input Task Parameters")
    
    task_data = []
    num_tasks = st.number_input("Number of Tasks", min_value=1, max_value=10, value=3)
    for i in range(num_tasks):
        period = st.number_input(f"Period (P{i+1})", min_value=1, value=5)
        execution_time = st.number_input(f"Execution Time (C{i+1})", min_value=1, value=2)
        task_data.append(Task(i+1, period, execution_time))
    
    simulation_time = st.number_input("Simulation Duration", min_value=1, value=20)
    
    if st.button("Run Simulation"):
        timeline = rm_schedule(task_data, simulation_time)
        st.subheader("Gantt Chart")
        fig = create_gantt_chart(timeline, task_data, "Task Execution Timeline")
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
