import torchreid

print(f"torchreid版本: {torchreid.__version__}")
model = torchreid.models.build_model('osnet_x0_25', num_classes=100)
print(f"ReID模型加载成功: {type(model).__name__}")