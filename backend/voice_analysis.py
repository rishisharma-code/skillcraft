import librosa
import numpy as np
import tempfile
import os

def extract_voice_features(file_input):
    """
    Extract MFCC voice features (13 values) for fatigue detection.
    Works with both file paths and Flask uploaded files.
    """

    temp_path = None

    try:
        # Handle Flask file upload
        if hasattr(file_input, "filename"):
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            file_input.save(temp_file.name)
            temp_path = temp_file.name
            file_path = temp_path
        else:
            file_path = file_input

        # Load audio (mono, max 10 sec)
        audio, sr = librosa.load(file_path, sr=None, mono=True, duration=10)

        # Check if audio is valid
        if audio is None or len(audio) == 0:
            return None

        # Normalize audio safely
        audio = librosa.util.normalize(audio)

        # Extract MFCC features (13)
        mfcc = librosa.feature.mfcc(
            y=audio,
            sr=sr,
            n_mfcc=13
        )

        # Take mean across time axis
        features = np.mean(mfcc, axis=1)

        # Ensure correct shape
        if features.shape[0] != 13:
            return None

        return features.astype(float)

    except Exception as e:
        print("❌ Voice processing error:", e)
        return None

    finally:
        # Delete temp file safely
        if temp_path:
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except Exception as e:
                print("⚠️ Temp file cleanup error:", e)