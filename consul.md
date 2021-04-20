# consul

tsf用


控制台
http://127.0.0.1:8500/ui/


直接编辑k/v
https://cloud.tencent.com/document/product/649/16620

https://github.com/hashicorp/consul
go语言写的

consul agent -dev


```shell
.\consul.exe agent -dev
==> Starting Consul agent...
           Version: '1.9.4'
           Node ID: '050cc805-dae5-b71e-5383-f9fb266967b1'
         Node name: 'Wdidada'
        Datacenter: 'dc1' (Segment: '<all>')
            Server: true (Bootstrap: false)
       Client Addr: [127.0.0.1] (HTTP: 8500, HTTPS: -1, gRPC: 8502, DNS: 8600)
      Cluster Addr: 127.0.0.1 (LAN: 8301, WAN: 8302)
           Encrypt: Gossip: false, TLS-Outgoing: false, TLS-Incoming: false, Auto-Encrypt-TLS: false

==> Log data will now stream in as it occurs:

    2021-04-19T15:18:21.293+0800 [INFO]  agent.server.raft: initial configuration: index=1 servers="[{Suffrage:Voter ID:050cc805-dae5-b71e-5383-f9fb266967b1 Address:127.0.0.1:8300}]"
    2021-04-19T15:18:21.309+0800 [INFO]  agent.server.raft: entering follower state: follower="Node at 127.0.0.1:8300 [Follower]" leader=
    2021-04-19T15:18:21.311+0800 [INFO]  agent.server.serf.wan: serf: EventMemberJoin: Wdidada.dc1 127.0.0.1
    2021-04-19T15:18:21.313+0800 [INFO]  agent.server.serf.lan: serf: EventMemberJoin: Wdidada 127.0.0.1
    2021-04-19T15:18:21.313+0800 [INFO]  agent.router: Initializing LAN area manager
    2021-04-19T15:18:21.314+0800 [INFO]  agent.server: Adding LAN server: server="Wdidada (Addr: tcp/127.0.0.1:8300) (DC: dc1)"
    2021-04-19T15:18:21.314+0800 [INFO]  agent.server: Handled event for server in area: event=member-join server=Wdidada.dc1 area=wan
    2021-04-19T15:18:21.315+0800 [INFO]  agent: Started DNS server: address=127.0.0.1:8600 network=udp
    2021-04-19T15:18:21.320+0800 [INFO]  agent: Started DNS server: address=127.0.0.1:8600 network=tcp
    2021-04-19T15:18:21.324+0800 [INFO]  agent: Starting server: address=127.0.0.1:8500 network=tcp protocol=http
    2021-04-19T15:18:21.325+0800 [WARN]  agent: DEPRECATED Backwards compatibility with pre-1.9 metrics enabled. These metrics will be removed in a future version of Consul. Set `telemetry { disable_compat_1.9 = true }` to disable them.
    2021-04-19T15:18:21.325+0800 [INFO]  agent: Started gRPC server: address=127.0.0.1:8502 network=tcp
    2021-04-19T15:18:21.328+0800 [INFO]  agent: started state syncer
==> Consul agent running!
    2021-04-19T15:18:21.379+0800 [WARN]  agent.server.raft: heartbeat timeout reached, starting election: last-leader=
    2021-04-19T15:18:21.379+0800 [INFO]  agent.server.raft: entering candidate state: node="Node at 127.0.0.1:8300 [Candidate]" term=2
    2021-04-19T15:18:21.381+0800 [DEBUG] agent.server.raft: votes: needed=1
    2021-04-19T15:18:21.381+0800 [DEBUG] agent.server.raft: vote granted: from=050cc805-dae5-b71e-5383-f9fb266967b1 term=2 tally=1
    2021-04-19T15:18:21.382+0800 [INFO]  agent.server.raft: election won: tally=1
    2021-04-19T15:18:21.383+0800 [INFO]  agent.server.raft: entering leader state: leader="Node at 127.0.0.1:8300 [Leader]"
    2021-04-19T15:18:21.384+0800 [INFO]  agent.server: cluster leadership acquired
    2021-04-19T15:18:21.384+0800 [INFO]  agent.server: New leader elected: payload=Wdidada
    2021-04-19T15:18:21.384+0800 [DEBUG] agent.server: Cannot upgrade to new ACLs: leaderMode=0 mode=0 found=true leader=127.0.0.1:8300
    2021-04-19T15:18:21.389+0800 [DEBUG] agent.server.autopilot: autopilot is now running
    2021-04-19T15:18:21.389+0800 [DEBUG] agent.server.autopilot: state update routine is now running
    2021-04-19T15:18:21.389+0800 [INFO]  agent.leader: started routine: routine="federation state anti-entropy"
    2021-04-19T15:18:21.392+0800 [INFO]  agent.leader: started routine: routine="federation state pruning"
    2021-04-19T15:18:21.393+0800 [DEBUG] connect.ca.consul: consul CA provider configured: id=07:80:c8:de:f6:41:86:29:8f:9c:b8:17:d6:48:c2:d5:c5:5c:7f:0c:03:f7:cf:97:5a:a7:c1:68:aa:23:ae:81 is_primary=true
    2021-04-19T15:18:21.404+0800 [INFO]  agent.server.connect: initialized primary datacenter CA with provider: provider=consul
    2021-04-19T15:18:21.405+0800 [INFO]  agent.leader: started routine: routine="intermediate cert renew watch"
    2021-04-19T15:18:21.407+0800 [INFO]  agent.leader: started routine: routine="CA root pruning"
    2021-04-19T15:18:21.409+0800 [DEBUG] agent.server: successfully established leadership: duration=24.9989ms
    2021-04-19T15:18:21.410+0800 [INFO]  agent.server: member joined, marking health alive: member=Wdidada
    2021-04-19T15:18:21.540+0800 [DEBUG] agent: Skipping remote check since it is managed automatically: check=serfHealth
    2021-04-19T15:18:21.546+0800 [INFO]  agent: Synced node info
    2021-04-19T15:18:21.548+0800 [DEBUG] agent: Node info in sync
    2021-04-19T15:18:21.560+0800 [INFO]  agent.server: federation state anti-entropy synced
    2021-04-19T15:18:23.453+0800 [DEBUG] agent: Skipping remote check since it is managed automatically: check=serfHealth
    2021-04-19T15:18:23.462+0800 [DEBUG] agent: Node info in sync
    2021-04-19T15:18:49.024+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&token=<hidden> from=127.0.0.1:1243 latency=0s
    2021-04-19T15:18:49.055+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services from=127.0.0.1:1243 latency=0s
    2021-04-19T15:18:49.058+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services from=127.0.0.1:1244 latency=0s
    2021-04-19T15:18:49.075+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/health/service/consul?token=<hidden> from=127.0.0.1:1244 latency=4.003ms
    2021-04-19T15:18:49.075+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/health/service/consul?token=<hidden> from=127.0.0.1:1243 latency=4.003ms
    2021-04-19T15:19:51.237+0800 [DEBUG] agent: Skipping remote check since it is managed automatically: check=serfHealth
    2021-04-19T15:19:51.240+0800 [DEBUG] agent: Node info in sync
    2021-04-19T15:19:57.223+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/kv/config/provider-demo/?recurse&token=<hidden> from=127.0.0.1:1315 latency=0s
    2021-04-19T15:19:57.301+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/kv/config/application/?recurse&token=<hidden> from=127.0.0.1:1315 latency=0s
    2021-04-19T15:20:06.161+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/kv/route/?recurse&token=&nsType=DEF_AND_GLOBAL&wait=55s<hidden> from=127.0.0.1:1315 latency=0s
    2021-04-19T15:20:06.166+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/kv/affinity/data?token=&nsType=DEF_AND_GLOBAL&wait=55s<hidden> from=127.0.0.1:1315 latency=0s
    2021-04-19T15:20:07.001+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&token=<hidden> from=127.0.0.1:1315 latency=0s
    2021-04-19T15:20:07.005+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/kv/config/?recurse&wait=55s from=127.0.0.1:1322 latency=0s
    2021-04-19T15:20:07.067+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/kv/lane/info/?recurse&token=&wait=55s<hidden> from=127.0.0.1:1315 latency=1.0032ms
    2021-04-19T15:20:07.067+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/kv/circuitbreaker/provider-demo?recurse&token=&wait=55s<hidden> from=127.0.0.1:1322 latency=0s
    2021-04-19T15:20:07.067+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/kv/ratelimit/provider-demo/data?token=&wait=55s<hidden> from=127.0.0.1:1323 latency=0s
    2021-04-19T15:20:07.067+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/kv/authority/provider-demo/data?token=&wait=55s<hidden> from=127.0.0.1:1324 latency=0s
    2021-04-19T15:20:07.144+0800 [DEBUG] agent: Service tag will not be discoverable via DNS due to invalid characters. Valid characters include all alpha-numerics and dashes.: tag=secure=false
    2021-04-19T15:20:07.146+0800 [DEBUG] agent: Node info in sync
    2021-04-19T15:20:07.148+0800 [INFO]  agent: Synced service: service=provider-demo-18081
    2021-04-19T15:20:07.149+0800 [DEBUG] agent: Check in sync: check=service:provider-demo-18081
    2021-04-19T15:20:07.149+0800 [DEBUG] agent: Node info in sync
    2021-04-19T15:20:07.150+0800 [DEBUG] agent: Service in sync: service=provider-demo-18081
    2021-04-19T15:20:07.150+0800 [DEBUG] agent: Check in sync: check=service:provider-demo-18081
    2021-04-19T15:20:07.151+0800 [DEBUG] agent.http: Request finished: method=PUT url=/v1/agent/service/register?token=<hidden> from=127.0.0.1:1324 latency=6.9996ms
    2021-04-19T15:20:07.195+0800 [DEBUG] agent: Check status updated: check=service:provider-demo-18081 status=passing
    2021-04-19T15:20:07.196+0800 [DEBUG] agent: Node info in sync
    2021-04-19T15:20:07.196+0800 [DEBUG] agent: Service in sync: service=provider-demo-18081
    2021-04-19T15:20:07.199+0800 [INFO]  agent: Synced check: check=service:provider-demo-18081
    2021-04-19T15:20:07.200+0800 [DEBUG] agent.http: Request finished: method=PUT url=/v1/agent/check/pass/service:provider-demo-18081?token=<hidden> from=127.0.0.1:1322 latency=4.9973ms
    2021-04-19T15:20:07.201+0800 [DEBUG] agent: Node info in sync
    2021-04-19T15:20:07.207+0800 [DEBUG] agent: Service in sync: service=provider-demo-18081
    2021-04-19T15:20:07.209+0800 [DEBUG] agent: Check in sync: check=service:provider-demo-18081
    2021-04-19T15:20:08.035+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&index=11&token=<hidden> from=127.0.0.1:1315 latency=1.0046ms
    2021-04-19T15:20:08.395+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services from=127.0.0.1:1334 latency=0s
    2021-04-19T15:20:11.135+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&index=19&token=<hidden> from=127.0.0.1:1334 latency=2.0920453s
    2021-04-19T15:20:14.250+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&index=19&token=<hidden> from=127.0.0.1:1334 latency=2.1059896s
    2021-04-19T15:20:17.316+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&index=19&token=<hidden> from=127.0.0.1:1334 latency=2.0609928s
    2021-04-19T15:20:20.396+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&index=19&token=<hidden> from=127.0.0.1:1334 latency=2.0761053s
    2021-04-19T15:20:21.315+0800 [DEBUG] agent.router.manager: Rebalanced servers, new active server: number_of_servers=1 active_server="Wdidada.dc1 (Addr: tcp/127.0.0.1:8300) (DC: dc1)"
    2021-04-19T15:20:21.317+0800 [DEBUG] agent.router.manager: Rebalanced servers, new active server: number_of_servers=1 active_server="Wdidada (Addr: tcp/127.0.0.1:8300) (DC: dc1)"
    2021-04-19T15:20:23.409+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&index=19&token=<hidden> from=127.0.0.1:1334 latency=2.003102s
    2021-04-19T15:20:26.536+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&index=19&token=<hidden> from=127.0.0.1:1334 latency=2.11799s
    2021-04-19T15:20:27.220+0800 [DEBUG] agent: Check status updated: check=service:provider-demo-18081 status=passing
    2021-04-19T15:20:27.381+0800 [DEBUG] agent: Node info in sync
    2021-04-19T15:20:27.384+0800 [DEBUG] agent: Service in sync: service=provider-demo-18081
    2021-04-19T15:20:27.385+0800 [DEBUG] agent: Check in sync: check=service:provider-demo-18081
    2021-04-19T15:20:27.386+0800 [DEBUG] agent.http: Request finished: method=PUT url=/v1/agent/check/pass/service:provider-demo-18081?token=<hidden> from=127.0.0.1:1334 latency=165.9987ms
    2021-04-19T15:20:29.801+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&index=19&token=<hidden> from=127.0.0.1:1334 latency=2.0389984s
    2021-04-19T15:20:32.980+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&index=19&token=<hidden> from=127.0.0.1:1334 latency=2.043s
    2021-04-19T15:20:36.090+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&index=19&token=<hidden> from=127.0.0.1:1334 latency=2.0690041s
    2021-04-19T15:20:39.231+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&index=19&token=<hidden> from=127.0.0.1:1334 latency=2.1209987s
    2021-04-19T15:20:39.615+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/kv/config/consumer-demo/?recurse&token=<hidden> from=127.0.0.1:1368 latency=0s
    2021-04-19T15:20:39.687+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/kv/config/application/?recurse&token=<hidden> from=127.0.0.1:1368 latency=0s
    2021-04-19T15:20:42.325+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&index=19&token=<hidden> from=127.0.0.1:1334 latency=2.0799992s
    2021-04-19T15:20:45.360+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&index=19&token=<hidden> from=127.0.0.1:1334 latency=2.0326021s
    2021-04-19T15:20:47.196+0800 [DEBUG] agent: Check status updated: check=service:provider-demo-18081 status=passing
    2021-04-19T15:20:47.196+0800 [DEBUG] agent: Node info in sync
    2021-04-19T15:20:47.197+0800 [DEBUG] agent: Service in sync: service=provider-demo-18081
    2021-04-19T15:20:47.197+0800 [DEBUG] agent: Check in sync: check=service:provider-demo-18081
    2021-04-19T15:20:47.198+0800 [DEBUG] agent.http: Request finished: method=PUT url=/v1/agent/check/pass/service:provider-demo-18081?token=<hidden> from=127.0.0.1:1375 latency=2.0003ms
    2021-04-19T15:20:48.387+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&index=19&token=<hidden> from=127.0.0.1:1334 latency=2.0010004s
    2021-04-19T15:20:50.911+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/kv/route/default_namespace/?recurse&token=&nsType=DEF_AND_GLOBAL&wait=55s<hidden> from=127.0.0.1:1368 latency=0s
    2021-04-19T15:20:50.916+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/kv/affinity/default_namespace/data?token=&nsType=DEF_AND_GLOBAL&wait=55s<hidden> from=127.0.0.1:1368 latency=0s
    2021-04-19T15:20:51.389+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/kv/config/?recurse&wait=55s from=127.0.0.1:1368 latency=0s
    2021-04-19T15:20:51.391+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&token=<hidden> from=127.0.0.1:1380 latency=0s
    2021-04-19T15:20:51.429+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&index=19&token=<hidden> from=127.0.0.1:1334 latency=2.0390019s
    2021-04-19T15:20:51.444+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/kv/authority/default_namespace/consumer-demo/data?token=&wait=55s<hidden> from=127.0.0.1:1368 latency=0s
    2021-04-19T15:20:51.445+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/kv/lane/info/?recurse&token=&wait=55s<hidden> from=127.0.0.1:1380 latency=1.0161ms
    2021-04-19T15:20:51.452+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/kv/ratelimit/default_namespace/consumer-demo/data?token=&wait=55s<hidden> from=127.0.0.1:1382 latency=0s
    2021-04-19T15:20:51.452+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/kv/circuitbreaker/default_namespace/consumer-demo?recurse&token=&wait=55s<hidden> from=127.0.0.1:1381 latency=3.0013ms
    2021-04-19T15:20:51.532+0800 [DEBUG] agent: Service tag will not be discoverable via DNS due to invalid characters. Valid characters include all alpha-numerics and dashes.: tag=secure=false
    2021-04-19T15:20:51.533+0800 [DEBUG] agent: Node info in sync
    2021-04-19T15:20:51.535+0800 [DEBUG] agent: Service in sync: service=provider-demo-18081
    2021-04-19T15:20:51.536+0800 [INFO]  agent: Synced service: service=consumer-demo-18083
    2021-04-19T15:20:51.536+0800 [DEBUG] agent: Check in sync: check=service:provider-demo-18081
    2021-04-19T15:20:51.537+0800 [DEBUG] agent: Check in sync: check=service:consumer-demo-18083
    2021-04-19T15:20:51.538+0800 [DEBUG] agent.http: Request finished: method=PUT url=/v1/agent/service/register?token=<hidden> from=127.0.0.1:1381 latency=5.9986ms
    2021-04-19T15:20:51.538+0800 [DEBUG] agent: Node info in sync
    2021-04-19T15:20:51.542+0800 [DEBUG] agent: Service in sync: service=consumer-demo-18083
    2021-04-19T15:20:51.544+0800 [DEBUG] agent: Service in sync: service=provider-demo-18081
    2021-04-19T15:20:51.545+0800 [DEBUG] agent: Check in sync: check=service:provider-demo-18081
    2021-04-19T15:20:51.546+0800 [DEBUG] agent: Check in sync: check=service:consumer-demo-18083
    2021-04-19T15:20:51.589+0800 [DEBUG] agent: Check status updated: check=service:consumer-demo-18083 status=passing
    2021-04-19T15:20:51.591+0800 [DEBUG] agent: Node info in sync
    2021-04-19T15:20:51.592+0800 [DEBUG] agent: Service in sync: service=provider-demo-18081
    2021-04-19T15:20:51.593+0800 [DEBUG] agent: Service in sync: service=consumer-demo-18083
    2021-04-19T15:20:51.593+0800 [DEBUG] agent: Check in sync: check=service:provider-demo-18081
    2021-04-19T15:20:51.596+0800 [INFO]  agent: Synced check: check=service:consumer-demo-18083
    2021-04-19T15:20:51.598+0800 [DEBUG] agent.http: Request finished: method=PUT url=/v1/agent/check/pass/service:consumer-demo-18083?token=<hidden> from=127.0.0.1:1381 latency=8.9951ms
    2021-04-19T15:20:51.599+0800 [DEBUG] agent: Node info in sync
    2021-04-19T15:20:51.602+0800 [DEBUG] agent: Service in sync: service=provider-demo-18081
    2021-04-19T15:20:51.603+0800 [DEBUG] agent: Service in sync: service=consumer-demo-18083
    2021-04-19T15:20:51.604+0800 [DEBUG] agent: Check in sync: check=service:provider-demo-18081
    2021-04-19T15:20:51.605+0800 [DEBUG] agent: Check in sync: check=service:consumer-demo-18083
    2021-04-19T15:20:51.708+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/health/service/provider-demo?token=&nsType=DEF_AND_GLOBAL&wait=55s<hidden> from=127.0.0.1:1381 latency=0s
    2021-04-19T15:20:52.407+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&index=19&token=<hidden> from=127.0.0.1:1368 latency=0s
    2021-04-19T15:20:52.635+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&index=19&token=<hidden> from=127.0.0.1:1334 latency=0s
    2021-04-19T15:20:52.725+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/health/service/provider-demo?token=&nsType=DEF_AND_GLOBAL&wait=55s<hidden> from=127.0.0.1:1396 latency=1.9983ms
    2021-04-19T15:20:52.938+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services from=127.0.0.1:1396 latency=998.7µs
    2021-04-19T15:20:55.544+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&index=24&token=<hidden> from=127.0.0.1:1396 latency=2.1010782s
    2021-04-19T15:20:55.679+0800 [DEBUG] agent.http: Request finished: method=GET url=/v1/catalog/services?wait=2s&index=24&token=<hidden> from=127.0.0.1:1334 latency=2.0170279s
```
