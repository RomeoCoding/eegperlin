import mne
import matplotlib.pyplot as plt
import numpy as np

# --- Configuration ---
data_path = 'C:\Users\matro\OneDrive - Technion\Research Papers\Biofeedback & Generative art\Data' # <<<<<<<<< IMPORTANT: CHANGE THIS TO YOUR DOWNLOAD PATH
subject_id = 'S001'
run_id = 'R01' # Starting with the Eyes Open/Closed run

edf_file = f"{data_path}{subject_id}/{subject_id}{run_id}.edf"
event_file = f"{data_path}{subject_id}/{subject_id}{run_id}.event" # Not always explicitly needed for simple runs, but good to know it exists

print(f"Attempting to load: {edf_file}")

# --- Load the EDF file ---
try:
    # Read the EDF file
    raw = mne.io.read_raw_edf(edf_file, preload=True, verbose='WARNING')
    print("EDF file loaded successfully!")

    # --- Basic Info ---
    print("\n--- Raw Info ---")
    print(raw.info) # General information about the recording
    print(f"Channels: {raw.ch_names}")
    print(f"Sampling frequency: {raw.info['sfreq']} Hz")
    print(f"Duration: {raw.times[-1]:.2f} seconds")

    # --- Event Information ---
    # The EEGMMIDB dataset has specific events encoded.
    # Event IDs:
    # 0: Rest 
    # 1: Open and close left fist 
    # 2: Open and close right fist 
    # 3: Open and close both fists 
    # 4: Open and close both feet 
    # This dataset uses 4s of motor imagery.

    # Find events in the raw data (these are usually markers for different tasks)
    events, event_id = mne.events_from_annotations(raw)
    print("\n--- Events found ---")
    print(events) # Array of [sample_index, previous_event_id, current_event_id]
    print(event_id) # Dictionary mapping event names to IDs

    # --- Plotting Raw Data (M1.3: Basic Inspection) ---
    print("\nPlotting raw data... Close the plot to continue.")
    # Plotting first 5 channels for a short duration
    raw.plot(duration=5, n_channels=5, scalings='auto', title=f"Raw Data - {subject_id} Run {run_id}")
    plt.show()

    # --- Plotting PSD (M1.4: Initial Power Analysis) ---
    print("\nPlotting Power Spectral Density... Close the plot to continue.")
    raw.plot_psd(fmax=50, average=True, picks='eeg', show=False) # Plot PSD for EEG channels
    plt.title(f"PSD - {subject_id} Run {run_id}")
    plt.show()

except FileNotFoundError:
    print(f"Error: The file {edf_file} was not found. Please check your 'data_path' and ensure the file exists.")
except Exception as e:
    print(f"An error occurred: {e}")