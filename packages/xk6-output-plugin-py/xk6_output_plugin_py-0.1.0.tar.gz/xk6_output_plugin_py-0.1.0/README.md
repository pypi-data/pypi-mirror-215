# xk6-output-plugin-py

Python plugin SDK for [xk6-output-plugin](https://github.com/szkiba/xk6-output-plugin).

## Documentation

**pip**

```bash
pip install xk6-output-plugin-py
```

**poetry**
```bash
poetry add xk6-output-plugin-py
```

## Example

```python
import datetime
import logging

from xk6_output_plugin_py.output import serve, Output, Info, MetricType, ValueType

class Example(Output):
  def Init(self, params):
    logging.info("init")

    return Info(description="example-py plugin")

  def Start(self):
    logging.info("start")

  def Stop(self):
    logging.info("stop")

  def AddMetrics(self, metrics):
    logging.info("metrics")
    for metric in metrics:
      logging.info(
        metric.name,
        extra={
          "metric.type": MetricType.Name(metric.type),
          "metric.contains": ValueType.Name(metric.contains),
        },
      )

  def AddSamples(self, samples):
    logging.info("samples")
    for sample in samples:
      t = datetime.datetime.fromtimestamp(
        sample.time / 1000.0, tz=datetime.timezone.utc
      )

      logging.info(
        sample.metric,
        extra={"sample.time": t, "sample.value": sample.value},
      )

if __name__ == "__main__":
  serve(Example())
```

<details>
  <summary>Output</summary>

```plain
          /\      |‾‾| /‾‾/   /‾‾/   
     /\  /  \     |  |/  /   /  /    
    /  \/    \    |     (   /   ‾‾\  
   /          \   |  |\  \ |  (‾)  | 
  / __________ \  |__| \__\ \_____/ .io

INFO[0000] init                                          plugin=example.py
INFO[0000] start                                         plugin=example.py
  execution: local
     script: script.js
     output: example-py plugin

  scenarios: (100.00%) 1 scenario, 1 max VUs, 10m30s max duration (incl. graceful stop):
           * default: 1 iterations for each of 1 VUs (maxDuration: 10m0s, gracefulStop: 30s)

INFO[0001] metrics                                       plugin=example.py
INFO[0001] http_reqs                                     metric.contains=DEFAULT metric.type=COUNTER plugin=example.py
INFO[0001] http_req_duration                             metric.contains=TIME metric.type=TREND plugin=example.py
INFO[0001] http_req_blocked                              metric.contains=TIME metric.type=TREND plugin=example.py
INFO[0001] http_req_connecting                           metric.contains=TIME metric.type=TREND plugin=example.py
INFO[0001] http_req_tls_handshaking                      metric.contains=TIME metric.type=TREND plugin=example.py
INFO[0001] http_req_sending                              metric.contains=TIME metric.type=TREND plugin=example.py
INFO[0001] http_req_waiting                              metric.contains=TIME metric.type=TREND plugin=example.py
INFO[0001] http_req_receiving                            metric.contains=TIME metric.type=TREND plugin=example.py
INFO[0001] http_req_failed                               metric.contains=DEFAULT metric.type=RATE plugin=example.py
INFO[0001] samples                                       plugin=example.py
INFO[0001] http_reqs                                     plugin=example.py sample.time="2023-06-23T07:14:09.985000+00:00" sample.value=1
INFO[0001] http_req_duration                             plugin=example.py sample.time="2023-06-23T07:14:09.985000+00:00" sample.value=124.175733
INFO[0001] http_req_blocked                              plugin=example.py sample.time="2023-06-23T07:14:09.985000+00:00" sample.value=142.170447
INFO[0001] http_req_connecting                           plugin=example.py sample.time="2023-06-23T07:14:09.985000+00:00" sample.value=124.043583
INFO[0001] http_req_tls_handshaking                      plugin=example.py sample.time="2023-06-23T07:14:09.985000+00:00" sample.value=0
INFO[0001] http_req_sending                              plugin=example.py sample.time="2023-06-23T07:14:09.985000+00:00" sample.value=0.091421
INFO[0001] http_req_waiting                              plugin=example.py sample.time="2023-06-23T07:14:09.985000+00:00" sample.value=124.004817
INFO[0001] http_req_receiving                            plugin=example.py sample.time="2023-06-23T07:14:09.985000+00:00" sample.value=0.079495
INFO[0001] http_req_failed                               plugin=example.py sample.time="2023-06-23T07:14:09.985000+00:00" sample.value=0
INFO[0001] http_reqs                                     plugin=example.py sample.time="2023-06-23T07:14:10.362000+00:00" sample.value=1
INFO[0001] http_req_duration                             plugin=example.py sample.time="2023-06-23T07:14:10.362000+00:00" sample.value=127.37244
INFO[0001] http_req_blocked                              plugin=example.py sample.time="2023-06-23T07:14:10.362000+00:00" sample.value=249.034715
INFO[0001] http_req_connecting                           plugin=example.py sample.time="2023-06-23T07:14:10.362000+00:00" sample.value=123.502855
INFO[0001] http_req_tls_handshaking                      plugin=example.py sample.time="2023-06-23T07:14:10.362000+00:00" sample.value=125.451159
INFO[0001] http_req_sending                              plugin=example.py sample.time="2023-06-23T07:14:10.362000+00:00" sample.value=0.083551
INFO[0001] http_req_waiting                              plugin=example.py sample.time="2023-06-23T07:14:10.362000+00:00" sample.value=127.117785
INFO[0001] http_req_receiving                            plugin=example.py sample.time="2023-06-23T07:14:10.362000+00:00" sample.value=0.171104
INFO[0001] http_req_failed                               plugin=example.py sample.time="2023-06-23T07:14:10.362000+00:00" sample.value=0
INFO[0002] metrics                                       plugin=example.py
INFO[0002] vus                                           metric.contains=DEFAULT metric.type=GAUGE plugin=example.py
INFO[0002] vus_max                                       metric.contains=DEFAULT metric.type=GAUGE plugin=example.py
INFO[0002] data_sent                                     metric.contains=DATA metric.type=COUNTER plugin=example.py
INFO[0002] data_received                                 metric.contains=DATA metric.type=COUNTER plugin=example.py
INFO[0002] iteration_duration                            metric.contains=TIME metric.type=TREND plugin=example.py
INFO[0002] iterations                                    metric.contains=DEFAULT metric.type=COUNTER plugin=example.py
INFO[0002] samples                                       plugin=example.py
INFO[0002] vus                                           plugin=example.py sample.time="2023-06-23T07:14:10.718000+00:00" sample.value=1
INFO[0002] vus_max                                       plugin=example.py sample.time="2023-06-23T07:14:10.718000+00:00" sample.value=1
INFO[0002] data_sent                                     plugin=example.py sample.time="2023-06-23T07:14:11.363000+00:00" sample.value=542
INFO[0002] data_received                                 plugin=example.py sample.time="2023-06-23T07:14:11.363000+00:00" sample.value=17310
INFO[0002] iteration_duration                            plugin=example.py sample.time="2023-06-23T07:14:11.363000+00:00" sample.value=1643.740944
INFO[0002] iterations                                    plugin=example.py sample.time="2023-06-23T07:14:11.363000+00:00" sample.value=1
INFO[0002] stop                                          plugin=example.py

     data_received..................: 17 kB 11 kB/s
     data_sent......................: 542 B 330 B/s
     http_req_blocked...............: avg=195.6ms  min=142.17ms med=195.6ms  max=249.03ms p(90)=238.34ms p(95)=243.69ms
     http_req_connecting............: avg=123.77ms min=123.5ms  med=123.77ms max=124.04ms p(90)=123.98ms p(95)=124.01ms
   ✓ http_req_duration..............: avg=125.77ms min=124.17ms med=125.77ms max=127.37ms p(90)=127.05ms p(95)=127.21ms
       { expected_response:true }...: avg=125.77ms min=124.17ms med=125.77ms max=127.37ms p(90)=127.05ms p(95)=127.21ms
   ✓ http_req_failed................: 0.00% ✓ 0       ✗ 2  
     http_req_receiving.............: avg=125.29µs min=79.49µs  med=125.29µs max=171.1µs  p(90)=161.94µs p(95)=166.52µs
     http_req_sending...............: avg=87.48µs  min=83.55µs  med=87.48µs  max=91.42µs  p(90)=90.63µs  p(95)=91.02µs 
     http_req_tls_handshaking.......: avg=62.72ms  min=0s       med=62.72ms  max=125.45ms p(90)=112.9ms  p(95)=119.17ms
     http_req_waiting...............: avg=125.56ms min=124ms    med=125.56ms max=127.11ms p(90)=126.8ms  p(95)=126.96ms
     http_reqs......................: 2     1.21664/s
     iteration_duration.............: avg=1.64s    min=1.64s    med=1.64s    max=1.64s    p(90)=1.64s    p(95)=1.64s   
     iterations.....................: 1     0.60832/s
     vus............................: 1     min=1     max=1
     vus_max........................: 1     min=1     max=1


running (00m01.6s), 0/1 VUs, 1 complete and 0 interrupted iterations
default ✓ [======================================] 1 VUs  00m01.6s/10m0s  1/1 iters, 1 per VU
```
</details>