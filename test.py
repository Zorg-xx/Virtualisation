from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
import time

def startService(net):
  for host in net.hosts:
    if host.name=="wst":
      print("Starting Web Service target")
      host.cmd('python -m SimpleHTTPServer 80 &')
      print("Web Service Started")


def attack(net):
  for host in net.hosts:
    if host.name=="dosL":
      dosl=host
    if host.name=="wst":
      targ=host
  print("Starting attack service")
  for i in range(100):
    dosl.cmd('wget -o - %s &' % targ.IP())
  print("attack done")
  
def generateTraffic(net):
  print("Traffic generation :")
  net.pingAll()
  print("\n")
if __name__=="__main__":
  topo=Topo()
  ##------SUBNET 1
  s1=topo.addSwitch("s1")
  webServTarg=topo.addHost("wst")
  tg1=topo.addHost("tg1")
  tg2=topo.addHost("tg2")
  topo.addLink(webServTarg,s1)
  topo.addLink(tg1,s1)
  topo.addLink(tg2,s1)

  ##------SUBNET 2
  s2=topo.addSwitch("s2")
  webCli1=topo.addHost("wc1")
  webCli2=topo.addHost("wc2")
  dosLaunch=topo.addHost("dosL")
  topo.addLink(s2,webCli1)
  topo.addLink(s2,webCli2)
  topo.addLink(s2,dosLaunch)

  ##--------Switch to Switch
  topo.addLink(s2,s1)

  ##-------CONTROLLEUR
  opFlowSwitch= RemoteController('c','192.168.122.118',6633)
  net=Mininet(topo=topo,controller=opFlowSwitch)
  print("Starting Network")
  net.start()
  print("Network started\n")
  #net.pingAll()
  startService(net)
  generateTraffic(net)
  time.sleep(2)
  attack(net)
  net.stop()
