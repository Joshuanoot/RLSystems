from nicegui import ui
from nicegui.events import ValueChangeEventArguments

def show(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    ui.notify(f'{name}: {event.value}')

from nicegui import ui

ui.button('Run', on_click=lambda: ui.notify('Click'))
ui.button('stop', on_click=lambda: ui.notify('Click'))
ui.radio(['10', '25', '50'], value='A', on_change=show).props('inline')
with ui.row():
    ui.input('Text input', on_change=show)
    ui.select(['One', 'Two'], value='One', on_change=show)
ui.link('And many more...', '/documentation').classes('mt-8')

def on_edit_button_click():
    file_path = "testedit.py"  # Specific file to edit
    old_word = "50"  # Replace with the word you want to replace
    new_word = entry.get()

    try:
        # Read the entire content of the file
        with open(file_path, 'r') as file:
            content = file.read()

        # Replace the old word with the new word
        updated_content = content.replace(old_word, new_word)

        # Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.write(updated_content)

        ui.notify("File successfully edited!")

    except Exception as e:
        error_message = f"Error editing the file: {str(e)}"
        ui.notify(error_message)

# Create the UI components
entry = ui.input("New Word")
ui.button("Edit File", on_click=on_edit_button_click)

def on_run_button_click():
    global process
    if process and process.poll() is None:
        # Terminate the existing subprocess if it's still running
        process.terminate()
        process.wait()  # Wait for the process to finish

    file_path = filedialog.askopenfilename(title="Select a Python file", filetypes=[("Python files", "*.py")])
    if file_path:
        process = subprocess.Popen(["python", file_path, "12"])

with ui.header().classes(replace='row items-center') as header:
    ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
    with ui.tabs() as tabs:
        ui.tab('A')
        ui.tab('Instellingen')
        ui.tab('C')

with ui.footer(value=False) as footer:
    ui.label('Footer')

with ui.left_drawer().classes('bg-blue-100') as left_drawer:
    ui.label('Side menu')

with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(on_click=footer.toggle, icon='contact_support').props('fab')

ui.run()
