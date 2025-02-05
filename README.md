# Geodesic Tissue Analysis for Arkitekt

## Build

### Docker
```bash
docker build --no-cache -f .arkitekt_next/flavours/vanilla/Dockerfile .
```

### Arkitekt-Next
```bash
arkitekt-next kabinet build --flavour vanilla
```

## Run
First start the docker container with the following command:
```bash
docker run --init -it --rm -p 5901:5901 -p 6080:6080 --shm-size=512M <container id> -vnc
```

Open a browser on localhost:6080 and connect via the VNC.
Inside the container you can run the App with this command:
```bash
arkitekt-next run prod --url <server>
```
