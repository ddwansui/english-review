# Rebuild a PyTorch Kokoro checkpoint from the MLX safetensors shipped with KokoroTTS.app.
import sys, torch
from safetensors.torch import load_file
from kokoro import KModel
R = "/Applications/KokoroTTS.app/Contents/Resources/"
CONFIG = R + "KokoroSwift_KokoroSwift.bundle/Contents/Resources/Resources/config.json"
out = sys.argv[1]
torch.save({}, out + ".empty")
model = KModel(config=CONFIG, model=out + ".empty")
src = load_file(R + "kokoro-v1_0.safetensors")
result, missing, reshaped = {}, [], 0
for top in ["bert", "bert_encoder", "predictor", "decoder", "text_encoder"]:
    expected = getattr(model, top).state_dict()
    sub = {}
    for key, ref in expected.items():
        tensor = src.get(f"{top}.{key}")
        if tensor is None:
            # The MLX export omits instance-norm affine parameters; PyTorch's defaults (1, 0) are what it assumes.
            if key.endswith(("norm.weight", "norm.bias")):
                sub[key] = ref.clone(); continue
            missing.append(f"{top}.{key}"); continue
        if tensor.shape != ref.shape:
            if tensor.dim() == 3 and tensor.permute(0, 2, 1).shape == ref.shape:
                tensor = tensor.permute(0, 2, 1).contiguous(); reshaped += 1
            elif tensor.numel() == ref.numel():
                tensor = tensor.reshape(ref.shape); reshaped += 1
            else:
                missing.append(f"{top}.{key} shape {tuple(tensor.shape)} vs {tuple(ref.shape)}"); continue
        sub[key] = tensor.to(ref.dtype)
    result[top] = sub
unused = len(src) - sum(len(v) for v in result.values())
print("missing", len(missing), missing[:8]); print("reshaped", reshaped, "unused source keys", unused)
torch.save(result, out)
