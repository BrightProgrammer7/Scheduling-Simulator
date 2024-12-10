import plotly.graph_objects as go

class Task:
    def __init__(self, id, period, execution_time, deadline):
        self.id = id
        self.period = period
        self.execution_time = execution_time
        self.deadline = deadline
        self.remaining_time = execution_time
        self.next_release = 0

def rm_schedule(tasks, simulation_time):
    timeline = []
    current_time = 0
    ready_queue = []
    
    while current_time < simulation_time:
        # Check for task releases
        for task in tasks:
            if current_time >= task.next_release:
                ready_queue.append(task)
                task.next_release += task.period
        
        # Sort by priority (shorter period = higher priority)
        ready_queue.sort(key=lambda x: x.period)
        
        if ready_queue:
            current_task = ready_queue[0]
            timeline.append((current_task.id, current_time, current_time + 1))
            current_task.remaining_time -= 1
            
            if current_task.remaining_time <= 0:
                ready_queue.pop(0)
                current_task.remaining_time = current_task.execution_time
        else:
            timeline.append(("Idle", current_time, current_time + 1))
        
        current_time += 1
    
    return timeline


def dm_schedule(tasks, simulation_time):
    timeline = []
    current_time = 0
    ready_queue = []
    
    while current_time < simulation_time:
        # Check for task releases
        for task in tasks:
            if current_time >= task.next_release:
                ready_queue.append(task)
                task.next_release += task.period
        
        # Sort by priority (shorter deadline = higher priority)
        ready_queue.sort(key=lambda x: x.deadline)
        
        if ready_queue:
            current_task = ready_queue[0]
            timeline.append((current_task.id, current_time, current_time + 1))
            current_task.remaining_time -= 1
            
            if current_task.remaining_time <= 0:
                ready_queue.pop(0)
                current_task.remaining_time = current_task.execution_time
        else:
            timeline.append(("Idle", current_time, current_time + 1))
        
        current_time += 1
    
    return timeline


def fcfs_schedule(tasks, simulation_time):
    timeline = []
    current_time = 0
    
    for task in tasks:
        # Check for task releases
        while current_time < task.next_release:
            timeline.append(("Idle", current_time, current_time + 1))
            current_time += 1
        
        # Execute the task
        for _ in range(task.execution_time):
            timeline.append((task.id, current_time, current_time + 1))
            current_time += 1
        
    return timeline


def create_gantt_chart(timeline, tasks, title):
    fig = go.Figure()
    colors = ['blue', 'orange', 'green', 'red', 'purple', 'cyan', 'magenta', 'yellow', 'pink', 'brown']
    
    # Reverse the tasks list to display in opposite order
    tasks_reversed = list(reversed(tasks))
    
    for idx, task in enumerate(tasks_reversed):
        task_timeline = [(t[1], t[2]) for t in timeline if t[0] == task.id]
        for start, end in task_timeline:
            fig.add_trace(go.Bar(
                x=[end - start],
                y=[f'Task {task.id}'],
                base=start,
                orientation='h',
                name=f'Task {task.id}',
                marker=dict(color=colors[idx % len(colors)])
            ))
    
    # Customize layout
    fig.update_layout(
        title=title,
        xaxis_title='Time',
        yaxis_title='Tasks',
        barmode='stack',
        height=400,
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )
    return fig


# Example usage
if __name__ == '__main__':
    tasks = [
        Task(1, 20, 3, 20),
        Task(2, 5, 2, 5),
        Task(3, 10, 2, 10)
    ]
    simulation_time = 100
    timeline_rm = rm_schedule(tasks, simulation_time)
    timeline_dm = dm_schedule(tasks, simulation_time)
    timeline_fcfs = fcfs_schedule(tasks, simulation_time)
    fig_rm = create_gantt_chart(timeline_rm, tasks, 'Rate Monotonic Scheduling')
    fig_dm = create_gantt_chart(timeline_dm, tasks, 'Deadline Monotonic Scheduling')
    fig_fcfs = create_gantt_chart(timeline_fcfs, tasks, 'First Come First Served Scheduling')
    fig_rm.show()
    fig_dm.show()
    fig_fcfs.show()
