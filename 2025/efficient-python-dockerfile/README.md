# Stages Of An Efficient Dockerfile

**Before running each dockerfile, place it in the leadspotr directory and the run the commands below in the same directory**

## Build commands

### Build `Dockerfile.01`

```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --no-cache \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             -f Dockerfile.01_original . -t 01_original
```
**Running the image**
```
docker run -p 8080:8080 01_original
```
### Build `Dockerfile.02_betterimg`
```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             --no-cache \
             -f Dockerfile.02_betterimg . -t 02_betterimg
```
**Running the image**
```
docker run -p 8080:8080 02_betterimg
```
### Build `Dockerfile.03_imgtag`
```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             --no-cache \
             -f Dockerfile.03_imgtag . -t 03_imgtag
```
**Running the image**
```
docker run -p 8080:8080 03_imgtag
```
### Build `Dockerfile.04_limitdeps`
```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             --no-cache \
             -f Dockerfile.04_limitdeps . -t 04_limitdeps
```
**Running the image**
```
docker run -p 8080:8080 04_limitdeps
```
### Build `Dockerfile.05_cleandeps`
```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             -f Dockerfile.05_cleandeps . -t 05_cleandeps
```
**Running the image**
```
docker run -p 8080:8080 05_cleandeps
```
### Build `Dockerfile.06_uv`
```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             --no-cache \
             -f Dockerfile.06_uv . -t 06_uv
```
**Running the image**
```
docker run -p 8080:8080 06_uv
```
### Build `Dockerfile.07_multi`
```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             --target=production \
             -f Dockerfile.07_multi . -t 07_multi
```
**Running the image**
```
docker run -p 8080:8080 07_multi
```

### Build `Dockerfile.08_bettercopy`
```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             --target=production \
             -f Dockerfile.08_bettercopy . -t 08_bettercopy
```
**Running the image**
```
docker run -p 8080:8080 08_bettercopy
```

### Build `Dockerfile.09_mountsecrets`
If you run into problems here, run the following commands before in your terminal:

```
export DB_PASSWORD="mydbpassword"
export DB_USER="mydbuser"
export DB_NAME="mydbname"
export DB_HOST="mydbhost"
export ACCESS_TOKEN_SECRET_KEY="mysecretkey"
```

```
docker build --secret id=DB_PASSWORD,env=DB_PASSWORD \
             --secret id=DB_USER,env=DB_USER \
             --secret id=DB_NAME,env=DB_NAME \
             --secret id=DB_HOST,env=DB_HOST \
             --secret id=ACCESS_TOKEN_SECRET_KEY,env=ACCESS_TOKEN_SECRET_KEY \
             --target=production \
             --no-cache \
             -f Dockerfile.09_mountsecrets . -t 09_mountsecrets
```
**Running the image**
```
docker run -p 8080:8080 09_mountsecrets 

```


### Build `Dockerfile.10_final`
If you run into problems here, run the following commands before in your terminal:
```
export DB_PASSWORD="mydbpassword"
export DB_USER="mydbuser"
export DB_NAME="mydbname"
export DB_HOST="mydbhost"
export ACCESS_TOKEN_SECRET_KEY="mysecretkey"
```

```
docker build --secret id=DB_PASSWORD \
             --secret id=DB_USER \
             --secret id=DB_NAME \
             --secret id=DB_HOST \
             --secret id=ACCESS_TOKEN_SECRET_KEY \
             --target=production \
             -f Dockerfile.10_final . -t 10_final
```
**Running the image**
```
docker run -p 8080:8080 10_final
```

### Build `Dockerfile.11_final_v2`

This iteration:

- **Multi‑stage build:** deterministic, layered design separating build and runtime.
- **Reproducible**: base images pinned by digest (`sha256:`) and `uv` dependency locking.
- **Secure**: runs as a non‑root numeric user within a minimal runtime base.
- **Signal‑safe**: managed by `tini` PID 1 and a lightweight shell entrypoint.
- **Configurable**: all runtime options (port, host, workers, secrets) sourced from environment vars.
- **Secretes**: Moved from build time to run time.

#### Build

```bash
docker build --no-cache --target production \
--build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
--build-arg GIT_COMMIT=$(git rev-parse HEAD) \
-f Dockerfile.11_final_v2 . -t 11_final_v2
```

You can override the pinned digest when you want to update Python security patches:

```bash
docker build \
--no-cache \
--target production \
--build-arg PYTHON_VERSION=3.13.9 \
--build-arg PYTHON_BASE_DIGEST=sha256:<new_bookworm_digest> \
--build-arg PYTHON_SLIM_DIGEST=sha256:<new_slim_digest> \
--build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
--build-arg GIT_COMMIT=$(git rev-parse HEAD) \
-f Dockerfile.11_final_v2 \
-t 11_final_v2 .
```

#### Running the image

```bash
export DB_PASSWORD="mydbpassword"
export DB_USER="mydbuser"
export DB_NAME="mydbname"
export DB_HOST="mydbhost"
export ACCESS_TOKEN_SECRET_KEY="mysecretkey"

docker run \
-p 8080:8080 \
-e DB_PASSWORD \
-e DB_USER \
-e DB_NAME \
-e DB_HOST \
-e ACCESS_TOKEN_SECRET_KEY \
--security-opt no-new-privileges:true \
--read-only \
--tmpfs /tmp:rw,noexec,nosuid,nodev \
--cap-drop=ALL \
11_final_v2
```

**Why these flags matter**

- `--target production` selects the hardened final stage from the multi-stage Dockerfile.
- `--build-arg BUILD_DATE` records the build timestamp for traceability in image metadata.
- `--build-arg GIT_COMMIT` bakes in the source revision so you can tie running containers back to code.
- `--build-arg PYTHON_VERSION`, `PYTHON_BASE_DIGEST`, `PYTHON_SLIM_DIGEST` let you override pinned digests when patching Python, while keeping reproducibility explicit.
- `-e DB_*` and `-e ACCESS_TOKEN_SECRET_KEY` pass secrets at runtime instead of baking them into the image.
- `--security-opt no-new-privileges:true` blocks privilege escalation inside the container.
- `--read-only` mounts the container filesystem as read-only to limit tampering; combine with `--tmpfs /tmp:rw,noexec,nosuid,nodev` to provide a safe scratch space.
- `--cap-drop=ALL` removes Linux capabilities not needed by the app, shrinking the attack surface.

**Inspect Container**

```bash
docker inspect --format '{{json .Config.Labels}}' 11_final_v2
```

```bash
docker run --rm 11_final_v2 bash -c "cat dependencies.txt"
```
