# Stages Of An Efficient Dockerfile

**Before running each dockerfile, place it in the leadspotr directory and the run the commands below in the same directory**

## Build commands

### Build `Dockerfile.01`

```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             -f Dockerfile.01_original . -t 01_original
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

### Build `Dockerfile.03_imgtag`
```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             -f Dockerfile.03_imgtag . -t 03_imgtag
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

### Build `Dockerfile.05_cleandeps`
```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             --no-cache \
             -f Dockerfile.05_cleandeps . -t 05_cleandeps
```



### Build `Dockerfile.06_uv`
* Remember to restructure the `pyproject.toml` file, so it matches with what UV expects
* Solution is the `uv_pyproject.toml`
```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             --no-cache \
             -f Dockerfile.06_uv . -t 06_uv
```

### Build `Dockerfile.07_multi`
* Remember to restructure the `pyproject.toml` file, so it matches with what UV expects
* Solution is the `uv_pyproject.toml`
```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             --target=production \
             --no-cache \
             -f Dockerfile.07_multi . -t 07_multi
```

### Build `Dockerfile.08_bettercopy`
```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             --target=production \
             --no-cache \
             -f Dockerfile.08_bettercopy . -t 08_bettercopy
```


### Build `09_Dockerfile.MountSecrets`
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
             --no-cache \
             -f 09_Dockerfile.MountSecrets . -t 09_mountsecrets
```


### Build `10_Dockerfile.Final`
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
             --no-cache \
             -f 10_Dockerfile.Final . -t 10_final
```

### Running the docker images
```
docker run -p 8080:8080 01_original
```