podman build --tag pythonweb:offsechelpers -f ./Dockerfile
podman run -p 8000:8000 -it localhost/pythonweb:offsechelpers
