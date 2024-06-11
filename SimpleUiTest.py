from nicegui import ui
from nicegui.events import ValueChangeEventArguments
import subprocess
from tkinter import filedialog, Tk
import os

# Set the page title
ui.page.title = 'RLSystems'

# Hide the root Tkinter window
root = Tk()
root.withdraw()

process = None

# Add custom CSS for the background color and remove borders
ui.add_style("""
*,
*::before,
*::after {
    box-sizing: border-box;
}

html, body {
    width: 100%;
    height: 100%;
    overflow: hidden;
    margin: 0;
    padding: 0;
    border: none;
    background-color: #D5A021; /* Change to desired color */
}

/* Remove any margins, padding, and borders from the top and left */
body, html {
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
}

.splitter-content {
    width: calc(100% - 120px); /* Adjust width to account for left panel */
    height: calc(100% - 70px); /* Adjust height to account for footer */
    overflow: hidden;
    padding: 16px; /* Add some padding for better visual */
    border: none;
    box-shadow: none;
    margin-left: 120px; /* Adjust margin to account for left panel */
    position: relative; /* Added to position absolute elements within it */
}

.splitter-vertical {
    border-left: none;
    border-right: none;
    box-shadow: none;
}

.empty-bar {
    height: 70px;
    background-color: #A49694; /* Change to desired color */
    width: 100%; /* Make the bar full width */
    position: absolute;
    bottom: 0px; /* Adjust the distance from the bottom */
    left: 0;
    z-index: 1; /* Ensure the empty bar stays above other elements */
}

/* Additional CSS to ensure no borders */
.nicegui-splitter,
.nicegui-splitter-vertical,
.nicegui-tab,
.nicegui-tab-panel {
    border: none !important;
    box-shadow: none !important;
}

.tab-with-image {
    display: flex;
    flex-direction: column; /* Stack items vertically */
    align-items: center; /* Center items horizontally */
    text-align: center; /* Center text horizontally */
}

.icon {
    width: 100px; /* Increased width */
    height: 100px; /* Increased height */
    margin-bottom: 8px; /* Space between icon and text */
}

.nicegui-tab {
    border-bottom: 1px solid #ddd; /* Optional: Add a bottom border to the tabs */
}

.splitter-content {
    background-color: #EDE7D9; /* Change to desired color */
    overflow: hidden; /* Remove scrollbar */
}

/* Ensure there are no borders on these specific elements */
.splitter, .nicegui-splitter, .nicegui-tab, .nicegui-tab-panel, .splitter-content {
    border-top: none !important;
    border-left: none !important;
    border-right: none !important;
    border-bottom: none !important;
    box-shadow: none !important;
}

/* Removing default margin and padding for all elements */
body > *,
html > * {
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    box-shadow: none !important;
}

/* Additional reset for all elements */
* {
    margin: 0;
    padding: 0;
    border: 0;
    outline: 0;
    background: transparent;
    box-shadow: none;
}

/* Remove borders from the overall splitter */
.q-splitter {
    border: none;
}

/* Remove borders from the panels inside the splitter */
.q-splitter__panel {
    border: none;
}

/* Ensure the separator has no borders */
.q-splitter__separator {
    border: none;
}

/* Remove any other borders or padding */
.q-splitter__separator-area {
    border: none;
    padding: 0;
    margin: 0;
}

/* Ensure tabs and other elements have no borders */
.q-tabs,
.q-tab,
.q-tabs__content,
.q-tab__indicator,
.q-icon {
    border: none;
}

/* Remove the border from the main container */
.nicegui-content {
    border: none;
    padding: 0;
    margin: 0;
}

/* Hide the default tab text */
.q-tab .q-tab__label {
    display: none;
}

/* Custom styles for absolute positioning with pixel values */
.absolute-position {
    position: absolute;
}

/* Set the left splitter panel to be fixed and cover the full height */
.left-splitter-panel {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    width: 120px; /* Adjust the width as needed */
    z-index: 2; /* Ensure it overlaps the footer */
    background-color: #D5A021; /* Ensure background color matches */
    overflow-y: auto; /* Allow scrolling if content is too tall */
}
""")

def show(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    ui.notify(f'{name}: {event.value}')

def on_run_button_click():
    global process
    if process and process.poll() is None:
        process.terminate()
        process.wait()  # Wait for the process to finish

    file_path = filedialog.askopenfilename(title="Select a Python file", filetypes=[("Python files", "*.py")])
    if file_path:
        ui.notify("Running the selected file...", type='info')
        process = subprocess.Popen(["python", file_path])

# Path to the image file
instellingen_image_path = r'C:\Users\joshu\Downloads\RLSystems-main\RLSystems-main\SettingsV1.2.png'  # Ensure the path is correctly escaped
start_image_path = r'C:\Users\joshu\Downloads\RLSystems-main\RLSystems-main\StartIconV1.1.png'  # Ensure the path is correctly escaped
home_image_path = r'C:\Users\joshu\Downloads\RLSystems-main\RLSystems-main\HomeIcon.png'  # Ensure the path is correctly escaped

image_path = r'C:\Users\joshu\Downloads\RLSystems-main\RLSystems-main\BackgroundImage.png'  # Example image path

# Check if the image file exists
if not os.path.exists(image_path):
    print(f"Image not found: {image_path}")

with ui.splitter(value=0).classes('w-full h-screen').style('height: 100vh; width: 100vw;') as splitter:  # Set initial splitter position to 0
    with ui.column().classes('left-splitter-panel'):
        with ui.tabs(value='Home').props('vertical').classes('w-full') as tabs:  # Set initial value to 'Home'
            with ui.tab('Home').classes('tab-with-image'):
                ui.image(home_image_path).classes('icon')
            with ui.tab('Starts').classes('tab-with-image'):
                ui.image(start_image_path).classes('icon')
            with ui.tab('Instellingen').classes('tab-with-image'):
                ui.image(instellingen_image_path).classes('icon')
    with splitter.after:
        with ui.tab_panels(tabs, value='Home').props('vertical').classes('w-full h-full'):  # Set initial value to 'Home'
            with ui.tab_panel('Home').classes('splitter-content'):

                # Apply CSS class for positioning here
                with ui.column().classes('absolute-position').style('top: 235px; right: 150px;'):  # Use inline style for pixel positioning
                    ui.image(image_path).style('width: 1000px; height: 1000px;')  # Set fixed width and height

            with ui.tab_panel('Starts').classes('splitter-content'):
                ui.label('Starts').classes('text-h4')
                ui.label('Content of Starts')
                ui.label('User Actions').classes('mt-4 mb-2 font-bold text-lg')
                ui.button('Run', on_click=lambda: ui.notify('Run Clicked')).props('icon=play_arrow')
                ui.button('Stop', on_click=lambda: ui.notify('Stop Clicked')).props('icon=stop')

                ui.label('Choose a Value').classes('mt-4 mb-2 font-bold text-lg')
                ui.radio(['10', '25', '50'], value='50', on_change=show).props('inline')

                with ui.row():
                    ui.input('Text input', on_change=show)
                    ui.select(['One', 'Two'], value='One', on_change=show)

                ui.link('And many more...', '/documentation').classes('mt-8')

                ui.label('Run Python Script').classes('mt-4 mb-2 font-bold text-lg')
                ui.button("Select and Run Python File", on_click=on_run_button_click).props('icon=play_circle')

            with ui.tab_panel('Instellingen').classes('splitter-content'):
                ui.label('Instellingen').classes('text-h4')
                ui.label('Content of Instellingen')

    with ui.html(tag='div').classes('empty-bar'):
        pass  # Add the empty bar at the bottom of the splitter

with ui.footer(value=False) as footer:
    ui.label('Footer')

ui.run(host='0.0.0.0', port=8080)  # Run on all available IPs
