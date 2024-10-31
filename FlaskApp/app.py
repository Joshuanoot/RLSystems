from flask import Flask, request, jsonify, render_template
import subprocess
import threading
import os
import time

app = Flask(__name__)

# Global variable to hold the thread
script_thread = None
# Global variable to control the script execution
stop_event = threading.Event()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-file', methods=['POST'])
def run_file():
    global script_thread, stop_event
    data = request.get_json()
    file_path = data.get('file_path')

    # Validate the file path
    if not os.path.isfile(file_path):
        return jsonify({'error': 'File not found'}), 404

    # Reset the stop event
    stop_event.clear()

    try:
        # Run the Python script in a separate thread
        script_thread = threading.Thread(target=run_script, args=(file_path,))
        script_thread.start()
        return jsonify({'output': 'Script running...'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stop-script', methods=['POST'])
def stop_script():
    global script_thread, stop_event

    try:
        # Debugging: Controleer de status van script_thread en stop_event
        if script_thread is None:
            print("Debug: script_thread is None")
        elif not script_thread.is_alive():
            print("Debug: script_thread is niet actief")
        
        # Controleer of er daadwerkelijk een actieve thread is om te stoppen
        if script_thread is None or not script_thread.is_alive():
            return jsonify({'message': 'No active script to stop'}), 400

        # Zet het stop-event en log deze actie
        print("Debug: stop_event wordt gezet")
        stop_event.set()
        
        # Wacht tot de thread stopt en log het resultaat
        script_thread.join(timeout=2)
        
        # Controleer of de thread daadwerkelijk is gestopt
        if script_thread.is_alive():
            print("Debug: script_thread is nog steeds actief na timeout")
            return jsonify({'message': 'Failed to stop the script'}), 500

        # Reset de script_thread naar None en log dit
        script_thread = None
        print("Debug: script_thread succesvol gestopt")
        return jsonify({'message': 'Script stopped successfully'}), 200

    except Exception as e:
        # Log de specifieke fout
        error_message = f"Error stopping script: {str(e)}"
        print("Debug: " + error_message)  # Log naar de console
        return jsonify({'error': error_message}), 500


def run_script(file_path):
    global stop_event
    try:
        # Start het subprocess
        process = subprocess.Popen(
            ['python3', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        def monitor_process():
            while process.poll() is None:
                # Als de stop_event gezet is, probeer te stoppen
                if stop_event.is_set():
                    print("Debug: Terminating process")
                    process.terminate()
                    try:
                        # Wacht kort zodat het proces de kans krijgt om normaal te stoppen
                        process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        print("Debug: Killing process as terminate() was unsuccessful")
                        process.kill()
                    break
                time.sleep(0.5)

        # Start een thread om het proces te monitoren
        monitor_thread = threading.Thread(target=monitor_process)
        monitor_thread.start()

        # Lees de output terwijl de monitor_thread het proces bewaakt
        for line in process.stdout:
            print(line.decode('utf-8').strip())

        # Wacht op de monitor_thread om te eindigen
        monitor_thread.join()

        # Haal de resterende output op
        output, error = process.communicate()
        if output:
            print(output.decode('utf-8'))
        if error:
            print(error.decode('utf-8'))

    except Exception as e:
        print(f"Error running script: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
