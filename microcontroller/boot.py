import uasyncio

from Task1 import Task1 
from Task2 import Task2
from Task3 import Task3
from Task4 import Task4
from Task5 import Task5

from PinDefinitions import button_change_task

from server import Server

async def run_board():
    tasks = [Task1(), Task2(), Task3(), Task4()]# , Task5()
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
        await uasyncio.sleep_ms(1)

async def run_server():
    await Server().start()

async def run():
    loop = uasyncio.get_event_loop()
    loop.create_task(run_board())
    loop.create_task(run_server())
    loop.run_forever()


if __name__ == "__main__":
    uasyncio.run(run())