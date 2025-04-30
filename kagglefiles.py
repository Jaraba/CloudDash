import kagglehub

# Download latest version
path = kagglehub.dataset_download("ashishraut64/global-methane-emissions")

print("Path to dataset files:", path)
