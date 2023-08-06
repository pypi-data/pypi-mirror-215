# How to run test

## Prequisite install

- **virtualenv** with **python3.10**
- **mosquitto**

```bash
pip3 install virtualenv
sudo apt install mosquitto
```

## Run pytest with virtualenv

### Test all

```bash
./run_test.sh basic utils super -ra
```

### Test utils

```bash
./run_test.sh utils -ra
```

### Test big thing

```bash
./run_test.sh basic -ra
```

### Test super thing

```bash
./run_test.sh super -ra
```
