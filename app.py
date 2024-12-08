import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import mne
from scipy.io import loadmat
from mne.preprocessing import ICA
import function_app as fa



# Load .mat file
def load_mat_file(file):
    try:
        return loadmat(file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# Plot heatmap
def plot_heatmap(df):
    plt.figure(figsize=(12, 8))
    sns.heatmap(df.corr(), annot=True, cmap="viridis", fmt=".2f")
    plt.title("Heatmap of Correlation")
    st.pyplot(plt)

# Plot line chart
def plot_line_chart(df):
    plt.figure(figsize=(12, 6))
    for column in df.columns:
        plt.plot(df[column], label=column)
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.title("Line Chart of EEG Data")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# Process and visualize EEG data
def process_eeg_data(df, sampling_freq):
    ch_names = [str(i) for i in df.columns]
    info = mne.create_info(ch_names=ch_names, ch_types=['eeg'] * len(ch_names), sfreq=sampling_freq)
    montage = mne.channels.make_standard_montage('standard_1020')
    info.set_montage(montage)
    raw = mne.io.RawArray(df.values.T, info)

    st.write("### Power Spectral Density (PSD)")
    raw.compute_psd(fmax=sampling_freq / 2).plot(picks="data", exclude="bads", show=False)
    st.pyplot(plt)

    st.write("### Time-Series Plot")
    scalings = {'eeg': 1000}
    raw.plot(start=120, duration=60, scalings=scalings, title='Scaled EEG Data', show=False, block=False)
    st.pyplot(plt)

    st.write("### Frequency Slice cho kênh đầu AF3")
    psd = raw.compute_psd(fmin=0, fmax=60, n_fft=128)
    psds, freqs = psd.get_data(return_freqs=True)
    plt.figure(figsize=(10, 6))
    plt.plot(freqs, psds[0])
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power Spectral Density')
    plt.title('Frequency Slice of EEG Data')
    plt.grid(True)
    st.pyplot(plt)

    st.write("### Independent Component Analysis (ICA)")
    ica = ICA(n_components=14, random_state=97, max_iter=800)
    ica.fit(raw)
    ica.plot_components()
    st.pyplot(plt)

# Streamlit App
st.title("EEG Data Visualization and Analysis")

uploaded_file = st.file_uploader("Thả một file a .mat để tiến hành visualize.", type="mat")

if uploaded_file is not None:
    data = load_mat_file(uploaded_file)
    if data:
        matfile = fa.MatlabData(data)
        df = matfile.data

        st.write("### Preview of Uploaded Data")
        st.dataframe(df.head())

        if df.isnull().any().any():
            st.warning("The dataset contains missing values.")

        st.write("### Heatmap of Correlations")
        plot_heatmap(df.iloc[:, 3:17])

        st.write("### Line Chart")
        plot_line_chart(df.iloc[:, 3:17])

        st.write("### Additional EEG Visualizations")
        process_eeg_data(df.iloc[:, 3:17], matfile.sampFreq)
