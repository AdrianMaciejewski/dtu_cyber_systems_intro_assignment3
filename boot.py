from task1 import Task1 
from task2 import Task2
from task3 import Task3
from task4 import Task4
from task5 import Task5

from PinDefinitions import button_change_task

def run():
    tasks = [Task1(), Task2(), Task3(), Task4(), Task5()]
    running_task_index = 0
    print("Starting with task 1")

    was_button_pressed = False
    while True:
        isButtonPressed = button_change_task.value()
        
        if isButtonPressed and not was_button_pressed:
            tasks[running_task_index].end_task() # end current task
            running_task_index = (running_task_index + 1) % len(tasks)  # switch to the next task
            tasks[running_task_index].start_task() # start the next (already current) task
            print(f"Swithed to task {running_task_index+1}")
        tasks[running_task_index].run_iteration()

        was_button_pressed = isButtonPressed



if __name__ == "__main__":
    run()