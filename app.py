import streamlit as st
from real_time_scheduling import Task, rm_schedule, dm_schedule, fcfs_schedule, sjf_schedule, edf_schedule, create_gantt_chart

def main():
    st.title("Real-Time Scheduling Simulator")
    st.markdown("### Select Scheduling Algorithm")
    
    algorithm = st.radio(
        "Choose scheduling algorithm:",
        ["First Come First Served (FCFS)", "Shortest Job First (SJF)", "Rate Monotonic (RM)", "Deadline Monotonic (DM)", "Earliest Deadline First (EDF)"]
    )
    
    st.markdown("### Input Task Parameters")
    
    task_data = []
    num_tasks = st.number_input("Number of Tasks", min_value=1, max_value=10, value=3)
    
    for i in range(num_tasks):
        st.markdown(f"#### Task {i+1}")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            period = st.number_input(f"Period (P{i+1})", min_value=1, value=5, key=f"period_{i}")
        with col2:
            execution_time = st.number_input(f"Execution Time (C{i+1})", min_value=1, value=2, key=f"exec_{i}")
        with col3:
            deadline = st.number_input(f"Deadline (D{i+1})", min_value=1, value=5, key=f"deadline_{i}")
        with col4:
            arrival_time = st.number_input(f"Arrival Time (A{i+1})", min_value=0, value=0, key=f"arrival_{i}")
        
        task_data.append(Task(i+1, period, execution_time, deadline, arrival_time))
    
    simulation_time = st.number_input("Simulation Duration", min_value=1, value=20)
    
    if st.button("Run Simulation"):
        if algorithm == "Rate Monotonic (RM)":
            timeline = rm_schedule(task_data, simulation_time)
            title = "Rate Monotonic Scheduling"
        elif algorithm == "Deadline Monotonic (DM)":
            timeline = dm_schedule(task_data, simulation_time)
            title = "Deadline Monotonic Scheduling"
        elif algorithm == "Shortest Job First (SJF)":
            timeline = sjf_schedule(task_data, simulation_time)
            title = "Shortest Job First Scheduling"
        elif algorithm == "Earliest Deadline First (EDF)":
            timeline = edf_schedule(task_data, simulation_time)
            title = "Earliest Deadline First Scheduling"
        else:
            timeline = fcfs_schedule(task_data, simulation_time)
            title = "First Come First Served Scheduling"
        
        st.subheader("Gantt Chart")
        fig = create_gantt_chart(timeline, task_data, title)
        st.plotly_chart(fig)
        
        # Display task parameters
        st.subheader("Task Parameters")
        task_info = []
        for task in task_data:
            task_info.append({
                "Task": f"T{task.id}",
                "Period": task.period,
                "Execution Time": task.execution_time,
                "Deadline": task.deadline,
                "Arrival Time": task.arrival_time
            })
        st.table(task_info)

if __name__ == "__main__":
    main()
