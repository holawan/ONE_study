Regarding `onecc` dockerizing, I'm considered about how to include the `-O` function.

As far as I know, in the ONE project, the optimization option is written in the configure file one by one and `onecc` is executed. Because of this inconvenience, the `-O` option is configured to suit the purpose, and then the `-O` option is applied to suit the intention.

When referring to the `_get_optimization_list` function in [utils.py](https://github.com/Samsung/ONE/blob/master/compiler/one-cmds/utils.py) , it is understood that the option should be placed in the folder after creating the "optimization" folder in the location below.

```
#utils.py 
    [one hierarchy]
    one
    ├── backends
    ├── bin
    ├── doc
    ├── include
    ├── lib
    ├── optimization
    └── test
```

When the Debian package is installed, we can use `onecc`. However, to use the `-O` option, I need to create an "optimization" folder in the "/usr/share/one" location and create a file in the `O*.cfg` format in this location. I'm thinking about how to share this as a volume in the Dockerizing process.

I'd appreciate it if you could leave a good opinion.

related issue : [#9712](https://github.com/Samsung/ONE/issues/9712)

/cc [@Samsung/ootpg](https://github.com/orgs/Samsung/teams/ootpg)