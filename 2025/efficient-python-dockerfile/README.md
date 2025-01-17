# Stages Of An Efficient Dockerfile

**Before running each dockerfile, place it in the leadspotr directory and the run the commands below in the same directory**

## Build commands

### Build `01_Dockerfile.Original`

```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             -f 01_Dockerfile.Original . -t 01_original
```

### Build `02_Dockerfile.RightBaseImage`
```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             -f 02_Dockerfile.RightBaseImage . -t 02_rightbaseimage
```

### Build `03_Dockerfile.SpecificTag`
```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             -f 03_Dockerfile.SpecificTag . -t 03_specifictag
```


### Build `04_Dockerfile.UnnecessaryDependencies`
```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             -f 04_Dockerfile.UnnecessaryDependencies . -t 04_unnecessarydependencies
```

### Build `05_Dockerfile.CleanUpDependencies`
```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             -f 05_Dockerfile.CleanUpDependencies . -t 05_cleanupdependencies
```



### Build `06_Dockerfile.UseUV`
* Remember to restructure the `pyproject.toml` file, so it matches with what UV expects
* Solution is the `uv_pyproject.toml`
```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             -f 06_Dockerfile.UseUV . -t 06_useuv
```

### Build `07_Dockerfile.UseMultiStage`
* Remember to restructure the `pyproject.toml` file, so it matches with what UV expects
* Solution is the `uv_pyproject.toml`
```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             --target=production \
             -f 07_Dockerfile.UseMultiStage . -t 07_usemultistage
```

### Build `08_Dockerfile.NoWildcardCopy`
```
docker build --build-arg DB_HOST=mydbhost \
             --build-arg DB_USER=mydbuser \
             --build-arg DB_PASSWORD=mydbpassword \
             --build-arg DB_NAME=mydbname \
             --build-arg ACCESS_TOKEN_SECRET_KEY=mysecretkey \
             --target=production \
             -f 08_Dockerfile.NoWildcardCopy . -t 08_nowildcardcopy
```


### Build `09_Dockerfile.MountSecrets`
```
docker build --secret id=DB_PASSWORD \
            --secret id=DB_USER \
            --secret id=DB_NAME \
            --secret id=DB_HOST \
            --secret id=ACCESS_TOKEN_SECRET_KEY \
            --target=production \
            -f 09_Dockerfile.MountSecrets . -t 09_mountsecrets
```