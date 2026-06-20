# consul

## 源代码仓库地址
https://github.com/hashicorp/consul
不是https://github.com/consul/consul
go语言写的

github repo
https://github.com/edidada/testconsul

curl http://127.0.0.1:8500/v1/catalog/services


==> Multiple private IPv4 addresses found. Please configure one with 'bind' and/or 'advertise'.
https://blog.csdn.net/xujiamin0022016/article/details/106822637


[root@10-23-29-39 ucloudscripts]# systemctl start consul
Warning: consul.service changed on disk. Run 'systemctl daemon-reload' to reload units.




[root@10-23-29-39 ucloudscripts]# /usr/bin/consul agent  -server -ui -client 0.0.0.0 -bind 10.23.29.39 -config-dir=/etc/consul.d/
==> Starting Consul agent...
           Version: '1.9.5'
           Node ID: '121a0330-e98a-b5ea-39fa-dcfbc2a841ed'
         Node name: '10-23-29-39'
        Datacenter: 'dc1' (Segment: '<all>')
            Server: true (Bootstrap: false)
       Client Addr: [0.0.0.0] (HTTP: 8500, HTTPS: -1, gRPC: -1, DNS: 8600)
      Cluster Addr: 10.23.29.39 (LAN: 8301, WAN: 8302)
           Encrypt: Gossip: false, TLS-Outgoing: false, TLS-Incoming: false, Auto-Encrypt-TLS: false

==> Log data will now stream in as it occurs:

    2021-04-21T22:40:01.677+0800 [WARN]  agent: The 'ui' field is deprecated. Use the 'ui_config.enabled' field instead.
    2021-04-21T22:40:01.688+0800 [WARN]  agent.auto_config: The 'ui' field is deprecated. Use the 'ui_config.enabled' field instead.
    2021-04-21T22:40:01.705+0800 [INFO]  agent.server.raft: initial configuration: index=0 servers=[]
    2021-04-21T22:40:01.706+0800 [INFO]  agent.server.serf.wan: serf: EventMemberJoin: 10-23-29-39.dc1 10.23.29.39
    2021-04-21T22:40:01.706+0800 [INFO]  agent.server.serf.lan: serf: EventMemberJoin: 10-23-29-39 10.23.29.39
    2021-04-21T22:40:01.706+0800 [INFO]  agent.router: Initializing LAN area manager
    2021-04-21T22:40:01.707+0800 [INFO]  agent: Started DNS server: address=0.0.0.0:8600 network=udp
    2021-04-21T22:40:01.707+0800 [INFO]  agent.server.raft: entering follower state: follower="Node at 10.23.29.39:8300 [Follower]" leader=
    2021-04-21T22:40:01.707+0800 [INFO]  agent.server: Adding LAN server: server="10-23-29-39 (Addr: tcp/10.23.29.39:8300) (DC: dc1)"
    2021-04-21T22:40:01.707+0800 [INFO]  agent.server: Handled event for server in area: event=member-join server=10-23-29-39.dc1 area=wan
    2021-04-21T22:40:01.708+0800 [INFO]  agent: Started DNS server: address=0.0.0.0:8600 network=tcp
    2021-04-21T22:40:01.708+0800 [INFO]  agent: Starting server: address=[::]:8500 network=tcp protocol=http
    2021-04-21T22:40:01.708+0800 [WARN]  agent: DEPRECATED Backwards compatibility with pre-1.9 metrics enabled. These metrics will be removed in a future version of Consul. Set `telemetry { disable_compat_1.9 = true }` to disable them.
    2021-04-21T22:40:01.708+0800 [INFO]  agent: started state syncer
==> Consul agent running!
    2021-04-21T22:40:08.514+0800 [WARN]  agent.server.raft: no known peers, aborting election
    2021-04-21T22:40:08.730+0800 [ERROR] agent.anti_entropy: failed to sync remote state: error="No cluster leader"



https://blog.csdn.net/chenchong08/article/details/77885989

consul UI用127可以访问，指定ip无法访问
./consul agent -dev    只能127.0.0.1可以访问
./consul agent -dev  -client 0.0.0.0 -ui  指定ip可以访问
https://www.consul.io/docs/agent/options.html


netstat -nultp | grep 8500
tcp6       0      0 :::8500                 :::*                    LISTEN      61504/consul 



[root@10-23-29-39 consul.d]# netstat -nultp | grep 8500
tcp        0      0 127.0.0.1:8500          0.0.0.0:*               LISTEN      61932/consul  


上面的不行，下面的只能127.0.0.1访问


tsf用


yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
yum -y install consul


[root@10-23-29-39 consul.d]# rpm -ql consul
/etc/consul.d/consul.hcl
/usr/bin/consul
/usr/lib/systemd/system/consul.service



控制台
http://127.0.0.1:8500/ui/


windows卡不开

直接编辑k/v
https://cloud.tencent.com/document/product/649/16620




windows 启动
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

问题，consul在windows上 打不开ui
consul agent -dev -ui打开默认ui 
  -ui
     Enables the built-in static web UI server.
http://127.0.0.1:8500/ui/


[root@10-23-29-39 ~]# curl localhost:8500/v1/catalog/nodes
[
    {
        "ID": "bb040849-996c-d6d1-e09c-44d9f370eed8",
        "Node": "10-23-29-39",
        "Address": "127.0.0.1",
        "Datacenter": "dc1",
        "TaggedAddresses": {
            "lan": "127.0.0.1",
            "lan_ipv4": "127.0.0.1",
            "wan": "127.0.0.1",
            "wan_ipv4": "127.0.0.1"
        },
        "Meta": {
            "consul-network-segment": ""
        },
        "CreateIndex": 11,
        "ModifyIndex": 12
    }
]
[root@10-23-29-39 ~]# dig @127.0.0.1 -p 8600 Judiths-MBP.node.consul

; <<>> DiG 9.11.4-P2-RedHat-9.11.4-26.P2.el7_9.4 <<>> @127.0.0.1 -p 8600 Judiths-MBP.node.consul
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 33368
;; flags: qr aa rd; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;Judiths-MBP.node.consul.   IN  A

;; AUTHORITY SECTION:
consul.         0   IN  SOA ns.consul. hostmaster.consul. 1618911844 3600 600 86400 0

;; Query time: 0 msec
;; SERVER: 127.0.0.1#8600(127.0.0.1)
;; WHEN: Tue Apr 20 17:44:04 CST 2021
;; MSG SIZE  rcvd: 102


### 退出
[root@10-23-29-39 ~]# consul leave
Graceful leave complete


```shell
PS C:\Users\edidada> consul agent -dev -ui
==> Starting Consul agent...
           Version: '1.9.4'
           Node ID: 'f42af06f-d5b6-5787-3cdc-70a01b9d47f2'
         Node name: 'Wdidada'
        Datacenter: 'dc1' (Segment: '<all>')
            Server: true (Bootstrap: false)
       Client Addr: [127.0.0.1] (HTTP: 8500, HTTPS: -1, gRPC: 8502, DNS: 8600)
      Cluster Addr: 127.0.0.1 (LAN: 8301, WAN: 8302)
           Encrypt: Gossip: false, TLS-Outgoing: false, TLS-Incoming: false, Auto-Encrypt-TLS: false

==> Log data will now stream in as it occurs:

    2021-04-20T17:53:03.076+0800 [INFO]  agent.server.raft: initial configuration: index=1 servers="[{Suffrage:Voter ID:f42af06f-d5b6-5787-3cdc-70a01b9d47f2 Address:127.0.0.1:8300}]"
    2021-04-20T17:53:03.089+0800 [INFO]  agent.server.raft: entering follower state: follower="Node at 127.0.0.1:8300 [Follower]" leader=
    2021-04-20T17:53:03.090+0800 [INFO]  agent.server.serf.wan: serf: EventMemberJoin: Wdidada.dc1 127.0.0.1
    2021-04-20T17:53:03.090+0800 [INFO]  agent.server.serf.lan: serf: EventMemberJoin: Wdidada 127.0.0.1
    2021-04-20T17:53:03.091+0800 [INFO]  agent.router: Initializing LAN area manager
    2021-04-20T17:53:03.091+0800 [INFO]  agent.server: Adding LAN server: server="Wdidada (Addr: tcp/127.0.0.1:8300) (DC: dc1)"
    2021-04-20T17:53:03.091+0800 [INFO]  agent.server: Handled event for server in area: event=member-join server=Wdidada.dc1 area=wan
    2021-04-20T17:53:03.091+0800 [INFO]  agent: Started DNS server: address=127.0.0.1:8600 network=udp
    2021-04-20T17:53:03.092+0800 [INFO]  agent: Started DNS server: address=127.0.0.1:8600 network=tcp
    2021-04-20T17:53:03.093+0800 [INFO]  agent: Starting server: address=127.0.0.1:8500 network=tcp protocol=http
    2021-04-20T17:53:03.094+0800 [WARN]  agent: DEPRECATED Backwards compatibility with pre-1.9 metrics enabled. These metrics will be removed in a future version of Consul. Set `telemetry { disable_compat_1.9 = true }` to disable them.
    2021-04-20T17:53:03.094+0800 [INFO]  agent: Started gRPC server: address=127.0.0.1:8502 network=tcp
    2021-04-20T17:53:03.094+0800 [INFO]  agent: started state syncer
==> Consul agent running!
    2021-04-20T17:53:03.132+0800 [WARN]  agent.server.raft: heartbeat timeout reached, starting election: last-leader=
    2021-04-20T17:53:03.132+0800 [INFO]  agent.server.raft: entering candidate state: node="Node at 127.0.0.1:8300 [Candidate]" term=2
    2021-04-20T17:53:03.132+0800 [DEBUG] agent.server.raft: votes: needed=1
    2021-04-20T17:53:03.133+0800 [DEBUG] agent.server.raft: vote granted: from=f42af06f-d5b6-5787-3cdc-70a01b9d47f2 term=2 tally=1
    2021-04-20T17:53:03.133+0800 [INFO]  agent.server.raft: election won: tally=1
    2021-04-20T17:53:03.133+0800 [INFO]  agent.server.raft: entering leader state: leader="Node at 127.0.0.1:8300 [Leader]"
    2021-04-20T17:53:03.133+0800 [INFO]  agent.server: cluster leadership acquired
    2021-04-20T17:53:03.134+0800 [INFO]  agent.server: New leader elected: payload=Wdidada
    2021-04-20T17:53:03.134+0800 [DEBUG] agent.server: Cannot upgrade to new ACLs: leaderMode=0 mode=0 found=true leader=127.0.0.1:8300
    2021-04-20T17:53:03.136+0800 [INFO]  agent.leader: started routine: routine="federation state anti-entropy"
    2021-04-20T17:53:03.136+0800 [INFO]  agent.leader: started routine: routine="federation state pruning"
    2021-04-20T17:53:03.136+0800 [DEBUG] agent.server.autopilot: autopilot is now running
    2021-04-20T17:53:03.138+0800 [DEBUG] agent.server.autopilot: state update routine is now running
    2021-04-20T17:53:03.138+0800 [DEBUG] connect.ca.consul: consul CA provider configured: id=07:80:c8:de:f6:41:86:29:8f:9c:b8:17:d6:48:c2:d5:c5:5c:7f:0c:03:f7:cf:97:5a:a7:c1:68:aa:23:ae:81 is_primary=true
    2021-04-20T17:53:03.152+0800 [INFO]  agent.server.connect: initialized primary datacenter CA with provider: provider=consul
    2021-04-20T17:53:03.153+0800 [INFO]  agent.leader: started routine: routine="intermediate cert renew watch"
    2021-04-20T17:53:03.154+0800 [INFO]  agent.leader: started routine: routine="CA root pruning"
    2021-04-20T17:53:03.156+0800 [DEBUG] agent.server: successfully established leadership: duration=21.9994ms
    2021-04-20T17:53:03.156+0800 [INFO]  agent.server: member joined, marking health alive: member=Wdidada
    2021-04-20T17:53:03.163+0800 [DEBUG] agent: Skipping remote check since it is managed automatically: check=serfHealth
    2021-04-20T17:53:03.164+0800 [INFO]  agent: Synced node info
    2021-04-20T17:53:03.165+0800 [DEBUG] agent: Node info in sync
    2021-04-20T17:53:03.205+0800 [INFO]  agent.server: federation state anti-entropy synced
    2021-04-20T17:53:05.813+0800 [DEBUG] agent: Skipping remote check since it is managed automatically: check=serfHealth
    2021-04-20T17:53:05.817+0800 [DEBUG] agent: Node info in sync
    2021-04-20T17:53:12.331+0800 [INFO]  agent.server: server starting leave
    2021-04-20T17:53:12.333+0800 [INFO]  agent.server.serf.wan: serf: EventMemberLeave: Wdidada.dc1 127.0.0.1
    2021-04-20T17:53:12.334+0800 [INFO]  agent.server: Handled event for server in area: event=member-leave server=Wdidada.dc1 area=wan
    2021-04-20T17:53:12.334+0800 [INFO]  agent.router.manager: shutting down
    2021-04-20T17:53:15.334+0800 [INFO]  agent.server.serf.lan: serf: EventMemberLeave: Wdidada 127.0.0.1
    2021-04-20T17:53:15.337+0800 [INFO]  agent.server: Removing LAN server: server="Wdidada (Addr: tcp/127.0.0.1:8300) (DC: dc1)"
    2021-04-20T17:53:15.342+0800 [WARN]  agent.server: deregistering self should be done by follower: name=Wdidada
    2021-04-20T17:53:18.337+0800 [INFO]  agent.server: Waiting to drain RPC traffic: drain_time=5s
    2021-04-20T17:53:22.075+0800 [ERROR] agent: Coordinate update error: error="No cluster leader"
    2021-04-20T17:53:23.138+0800 [DEBUG] agent.server.autopilot: will not remove server as its removal would be unsafe due to affectingas removal of a majority or servers is not safe: id=f42af06f-d5b6-5787-3cdc-70a01b9d47f2
    2021-04-20T17:53:23.339+0800 [INFO]  agent: Requesting shutdown
    2021-04-20T17:53:23.340+0800 [INFO]  agent.server: shutting down server
    2021-04-20T17:53:23.344+0800 [DEBUG] agent.leader: stopping routine: routine="intermediate cert renew watch"
    2021-04-20T17:53:23.347+0800 [DEBUG] agent.leader: stopping routine: routine="CA root pruning"
    2021-04-20T17:53:23.344+0800 [DEBUG] agent.server.usage_metrics: usage metrics reporter shutting down
    2021-04-20T17:53:23.347+0800 [DEBUG] agent.leader: stopped routine: routine="intermediate cert renew watch"
    2021-04-20T17:53:23.353+0800 [DEBUG] agent.leader: stopping routine: routine="federation state anti-entropy"
    2021-04-20T17:53:23.353+0800 [DEBUG] agent.leader: stopped routine: routine="CA root pruning"
    2021-04-20T17:53:23.369+0800 [DEBUG] agent.leader: stopping routine: routine="federation state pruning"
    2021-04-20T17:53:23.374+0800 [DEBUG] agent.leader: stopped routine: routine="federation state pruning"
    2021-04-20T17:53:23.369+0800 [DEBUG] agent.leader: stopped routine: routine="federation state anti-entropy"
    2021-04-20T17:53:23.374+0800 [DEBUG] agent.server.autopilot: state update routine is now stopped
    2021-04-20T17:53:23.375+0800 [INFO]  agent.router.manager: shutting down
    2021-04-20T17:53:23.376+0800 [INFO]  agent: consul server down
    2021-04-20T17:53:23.383+0800 [DEBUG] agent.server.autopilot: autopilot is now stopped
    2021-04-20T17:53:23.387+0800 [INFO]  agent: shutdown complete
    2021-04-20T17:53:23.389+0800 [DEBUG] agent.http: Request finished: method=PUT url=/v1/agent/leave from=127.0.0.1:14875 latency=11.0580034s
    2021-04-20T17:53:23.389+0800 [INFO]  agent: Stopping server: protocol=DNS address=127.0.0.1:8600 network=tcp
    2021-04-20T17:53:23.400+0800 [INFO]  agent: Stopping server: protocol=DNS address=127.0.0.1:8600 network=udp
    2021-04-20T17:53:23.402+0800 [INFO]  agent: Stopping server: address=127.0.0.1:8500 network=tcp protocol=http
    2021-04-20T17:53:23.906+0800 [INFO]  agent: Waiting for endpoints to shut down
    2021-04-20T17:53:23.908+0800 [INFO]  agent: Endpoints down
    2021-04-20T17:53:23.912+0800 [INFO]  agent: Exit code: code=0
```


### spring cloud

consul有两个功能，一个是consul作为注册中心，另一个是consul作为配置中心。
https://www.cnblogs.com/linjiqin/p/9718223.html

根据上面的博客写个demo


https://spring.io/projects/spring-cloud-consul/


### 配置中心，注册中心对比

consul
nacos
eureka
zk

是的，Spring Cloud 中的 ZooKeeper（ZK）可以作为配置中心，用于集中管理应用程序的配置信息，实现配置的动态更新和分布式共享。

具体而言，可以通过 Spring Cloud 的 `spring-cloud-starter-zookeeper-config` 依赖来集成 ZooKeeper 作为配置中心。您需要在应用程序中添加该依赖，并在 `bootstrap.properties` 或 `bootstrap.yml` 配置文件中指定以下配置项：

```yaml
spring.cloud.zookeeper.enabled=true
spring.cloud.zookeeper.connect-string=localhost:2181 # ZooKeeper 的连接地址
spring.cloud.zookeeper.config.root=/config # 配置文件在 ZooKeeper 中的根节点路径
spring.cloud.zookeeper.config.enabled=true # 启用 ZooKeeper 作为配置中心
```

然后，您可以在 ZooKeeper 的 `/config` 节点下创建配置文件，并在应用程序中通过 `@Value`、`@ConfigurationProperties` 等注解来获取配置信息。例如：

```yaml
# 在 ZooKeeper 中创建配置文件 /config/myapp.yml
server:
  port: 8080
```

```java
@Component
@ConfigurationProperties(prefix = "server")
public class MyAppConfig {
    private int port;
    // getter 和 setter 方法
}
```

在上述例子中，`MyAppConfig` 类使用 `@ConfigurationProperties` 注解来获取 `server.port` 配置项的值，该配置项存储在 ZooKeeper 的 `/config/myapp.yml` 文件中。当 `/config/myapp.yml` 文件发生变化时，应用程序会自动重新加载配置，并更新 `MyAppConfig` 对象的值。

需要注意的是，使用 ZooKeeper 作为配置中心时，要确保 ZooKeeper 的稳定性和可靠性，并避免出现 ZooKeeper 故障导致应用程序无法正常启动或运行的情况。同时，也要注意配置文件的安全性和权限控制，防止敏感信息泄露或被非法访问。


在微服务架构中，配置中心和注册中心都是非常重要的组件，它们分别负责应用程序配置信息的管理和服务实例的注册与发现。下面是四种常见的微服务框架中，配置中心和注册中心的比较：
1. Consul
Consul 是一个分布式的、高可用的服务发现和配置管理平台。它提供了服务注册与发现、健康检查、KV 存储、分布式锁等功能，并且支持多数据中心、跨平台、跨云等特性。在 Consul 中，配置中心和注册中心是集成在一起的，使用 Consul 可以实现统一的配置管理和服务发现。
2. Nacos
Nacos 是一个开源的分布式服务注册和配置中心，它提供了服务注册与发现、配置管理、流量管理等功能，并且支持多数据中心、多语言、多协议等特性。在 Nacos 中，配置中心和注册中心是集成在一起的，使用 Nacos 可以实现统一的配置管理和服务发现。
3. Eureka
Eureka 是 Netflix 开源的一个服务注册和发现框架，它提供了服务注册与发现、健康检查等功能，并且支持集群部署、自我保护、自动剔除等特性。在 Eureka 中，注册中心主要负责服务实例的注册和发现，而配置管理则需要借助其他的配置中心组件，例如 Spring Cloud Config。
4. ZooKeeper
ZooKeeper 是一个分布式的、高可用的协调服务框架，它提供了分布式锁、命名服务、配置管理等功能，并且支持多语言、多协议等特性。在 ZooKeeper 中，配置管理和注册中心可以分别使用不同的节点或路径来实现，例如使用 `/config` 节点来存储应用程序配置信息，使用 `/services` 节点来存储服务实例信息。
总之，不同的微服务框架中，配置中心和注册中心的实现方式和特性都有所不同，您可以根据实际情况进行选择和定制。无论您选择哪种框架，都需要注意其稳定性、可靠性和安全性，以确保应用程序的正常运行。
