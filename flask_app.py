from flask import Flask, render_template, request, jsonify
import plotly.figure_factory as ff
import plotly.utils
import json
from real_time_scheduling import Task, fcfs_schedule, sjf_schedule, rm_schedule, dm_schedule, edf_schedule, llf_schedule

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule', methods=['POST'])
def schedule():
    data = request.get_json()
    
    # Create Task objects from the request data
    tasks = [Task(
        task['id'],
        task['period'],
        task['execution_time'],
        task['deadline'],
        task['arrival_time']
    ) for task in data['tasks']]
    
    simulation_time = data['simulation_time']
    algorithm = data['algorithm']
    
    # Select scheduling algorithm
    if algorithm == 'First Come First Served (FCFS)':
        timeline = fcfs_schedule(tasks, simulation_time)
    elif algorithm == 'Shortest Job First (SJF)':
        timeline = sjf_schedule(tasks, simulation_time)
    elif algorithm == 'Rate Monotonic (RM)':
        timeline = rm_schedule(tasks, simulation_time)
    elif algorithm == 'Deadline Monotonic (DM)':
        timeline = dm_schedule(tasks, simulation_time)
    elif algorithm == 'Earliest Deadline First (EDF)':
        timeline = edf_schedule(tasks, simulation_time)
    else:  # Least Laxity First (LLF)
        timeline = llf_schedule(tasks, simulation_time)
    
    # Prepare data for Gantt chart
    df = []
    for task_id, start, finish in timeline:
        df.append(dict(
            Task=f'Task {task_id}' if task_id != 'Idle' else 'Idle',
            Start=start,
            Finish=finish,
            Resource=f'Task {task_id}' if task_id != 'Idle' else 'Idle'
        ))
    
    # Create Gantt chart using plotly
    fig = ff.create_gantt(
        df,
        index_col='Resource',
        show_colorbar=True,
        group_tasks=True,
        showgrid_x=True,
        showgrid_y=True
    )
    
    # Update layout
    fig.update_layout(
        title=f'{algorithm} Schedule',
        xaxis_title='Time',
        height=400,
        font=dict(size=10)
    )
    
    # Convert the figure to JSON
    gantt_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify({
        'gantt_chart': gantt_json,
        'schedule': timeline
    })

if __name__ == '__main__':
    app.run(debug=True)
