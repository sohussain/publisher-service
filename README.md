# description[![Build status](https://badge.buildkite.com/0b019e592c98cbecab22cfb3a822cb7910ee8c391f1349378d.svg?branch=master)](https://buildkite.com/hazenai/publisher-tbd)

This service receives message from aggregator service on queue. Its responsibility is to publish the message to remote endpoint.


### Build Image and Run Container
```
DOCKER_BUILDKIT=1 docker build --target x86_64_development -t publisher:latest . 
docker run -it --name=publisher --net=host -v $SHARED_STORAGE:/packages publisher:latest

```

### Resource Consumption
```
Image Size = 120MB
Memory Consumption = 20MB
```

### Run Tests (Exit on first failed test)
```
py.test --stepwise tests

```
 
### Run Tests with Coverage Report
```
coverage run --source='publisher,config' -m py.test tests
coverage report

```

### Test Coverage Report
```

Name                                           Stmts   Miss  Cover
------------------------------------------------------------------
config/config_reader/config_factory.py             7      0   100%
config/config_reader/iconfig.py                    5      1    80%
config/config_reader/ini_parser.py                17      2    88%
publisher/dataPublisher/__init__.py                0      0   100%
publisher/dataPublisher/publishRemote.py          20     20     0%
publisher/eventHandler/__init__.py                 0      0   100%
publisher/eventHandler/aggregator_handler.py      30     30     0%
publisher/main.py                                 49     49     0%
publisher/package_queue.py                        20      3    85%
publisher/queue/__init__.py                        0      0   100%
publisher/queue/queue.py                          43     12    72%
publisher/utilities/encoder.py                    29      6    79%
publisher/utilities/singleton_meta.py              6      0   100%
------------------------------------------------------------------
TOTAL                                            226    123    46%

```