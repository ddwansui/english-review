# Offline Kokoro synthesis: card texts in, AAC (.m4a) files out. Usage: speak.py OUT_DIR VOICE id=text ...
import sys, subprocess, numpy as np, soundfile as sf, torch, spacy
# misaki would download spaCy's tagger; a blank English pipeline keeps this fully offline.
spacy.util.is_package = lambda name: True
spacy.load = lambda name, **kwargs: spacy.blank("en")
from kokoro import KModel, KPipeline
R = "/Applications/KokoroTTS.app/Contents/Resources/"
import os; HERE = os.path.dirname(os.path.abspath(__file__))
out_dir, voice_name, items = sys.argv[1], sys.argv[2], sys.argv[3:]
model = KModel(repo_id="hexgrad/Kokoro-82M", config=R + "KokoroSwift_KokoroSwift.bundle/Contents/Resources/Resources/config.json",
               model=HERE + "/kokoro-v1_0.pth").eval()
pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M", model=model)
voice = torch.from_numpy(np.load(R + "voices.npz")[voice_name])
for item in items:
    card_id, text = item.split("=", 1)
    audio = [chunk.audio.numpy() for chunk in pipeline(text, voice=voice, speed=0.95) if chunk.audio is not None]
    wav = f"{out_dir}/{card_id}.wav"
    sf.write(wav, np.concatenate(audio), 24000)
    subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", "-b", "64000", wav, f"{out_dir}/{card_id}.m4a"], check=True)
    print(card_id, round(sum(len(a) for a in audio) / 24000, 2), "s")
