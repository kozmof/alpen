## Design
### Install
```
pip3 install janome
pip3 install msgpack
pip3 install langdetect
```

### Doc-build proceess
- get build target docs
- add domains
    - auto assign
    - manual assign
- make payload
- generate tsx

### Doc structure
- doc [user]
    - domain [user|auto(Tf-Idf, cos similarity)]
    - lang [auto(langdetect)]
    - tag [user]