import gradio as gr
from real_time_scheduling import Task, rm_schedule, dm_schedule, fcfs_schedule, sjf_schedule, edf_schedule, llf_schedule, create_gantt_chart
import plotly.io as pio

# Define a function to simulate scheduling
def simulate_scheduling(algorithm, num_tasks, task_parameters, simulation_time):
    title = "Unknown Scheduling Algorithm"  # Default title
    # Convert task parameters to integers
    periods = task_parameters[:, 0].astype(int)
    execution_times = task_parameters[:, 1].astype(int)
    deadlines = task_parameters[:, 2].astype(int)
    arrival_times = task_parameters[:, 3].astype(int)

    task_data = [
        Task(i+1, periods[i], execution_times[i], deadlines[i], arrival_times[i])
        for i in range(num_tasks)
    ]

    if algorithm == "First Come First Served (FCFS)":
        timeline = fcfs_schedule(task_data, simulation_time)
        title = "First Come First Served Scheduling"
    elif algorithm == "Shortest Job First (SJF)":
        timeline = sjf_schedule(task_data, simulation_time)
        title = "Shortest Job First Scheduling"
    elif algorithm == "Rate Monotonic (RM)":
        timeline = rm_schedule(task_data, simulation_time)
        title = "Rate Monotonic Scheduling"
    elif algorithm == "Deadline Monotonic (DM)":
        timeline = dm_schedule(task_data, simulation_time)
        title = "Deadline Monotonic Scheduling"
    elif algorithm == "Earliest Deadline First (EDF)":
        timeline = edf_schedule(task_data, simulation_time)
        title = "Earliest Deadline First Scheduling"
    elif algorithm == "Least Laxity First (LLF)":
        timeline = llf_schedule(task_data, simulation_time)
        title = "Least Laxity First Scheduling"
    else:
        timeline = fcfs_schedule(task_data, simulation_time)
        title = "First Come First Served Scheduling"

    gantt_chart = create_gantt_chart(timeline, task_data, title)
    pio.write_image(gantt_chart, "gantt_chart.png")
    return "gantt_chart.png"

# Create a Gradio interface
demo = gr.Interface(
    fn=simulate_scheduling,
    inputs=[
        gr.Radio(["First Come First Served (FCFS)", "Shortest Job First (SJF)", "Rate Monotonic (RM)", "Deadline Monotonic (DM)", "Earliest Deadline First (EDF)", "Least Laxity First (LLF)"], label="Scheduling Algorithm"),
        gr.Slider(1, 10, step=1, value=3, label="Number of Tasks"),
        gr.Dataframe(headers=["Period", "Execution Time", "Deadline", "Arrival Time"], type="numpy", row_count=3, col_count=4, label="Task Parameters"),
        gr.Slider(1, 100, step=1, value=20, label="Simulation Duration")
    ],
    outputs=gr.Image(type="filepath", label="Gantt Chart"),
    title="Real-Time Scheduling Simulator",
    description="Simulate various real-time scheduling algorithms and visualize the results as a Gantt chart."
)

# Launch the interface
demo.launch()
