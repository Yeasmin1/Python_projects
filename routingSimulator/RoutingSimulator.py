# Routing protocol simulator

class Router:

    def __init__(self,routerName):
        self.__routerName = routerName
        self.__connections = []
        self.__routingTable = {}


    def print_info(self):
        print("  %s"% self.__routerName)
        print("    N: %s" % self.connections_printing() )
        print("    R: %s" % self.routing_table_printing())


    def add_neighbour(self, routerObject):
        if routerObject in self.__connections:
            pass
        else:
            self.__connections.append(routerObject)


    def add_network(self,address,distance):
        self.__routingTable[address] = distance


    def receive_routing_table(self, sendingRouterObj):
        for key,value in sendingRouterObj.__routingTable.items():
            if key in self.__routingTable:
                pass
            else:
               self.__routingTable[key] = int(value) + 1


    def has_route(self, networkName):
        if networkName in self.__routingTable:
            if int(self.__routingTable[networkName]) == 0:
                print("Router is an edge router for the network.")
            else:
                print("Network %s is %d hops away" % (networkName,
                                                      int(self.__routingTable[
                                                              networkName])))
        else:
            print("Route to the network is unknown.")


    def connections_printing(self):
        """
        :return: This function return the neighbour routers in sorted str
        format for the given router.
        """
        neighbours = ""
        if len(self.__connections) == 0:
            return neighbours
        else:
            for item in sorted(self.__connections):
                neighbours += item.get_router_name()
                neighbours += ", "
            neighbours = neighbours[:-2]
            return neighbours


    def routing_table_printing(self):
        """
        :return: sorted str format routing table of the given router.
        """
        routing = ""
        if len(self.__routingTable) == 0:
            return ""
        else:
            for k,v in sorted(self.__routingTable.items()):
                routing  += k
                routing += ":"
                routing += str(v)
                routing += ", "
            routing = routing[:-2]
            return routing


    def get_router_name(self):
        """
        :return: router name.
        """
        return self.__routerName


    def find_neighbours(self):
        """
        :return: return neighbours router in list format.
        """
        return self.__connections


    def __eq__(self, other):
        if self.__routerName == other.__routerName:
            return True
        else:
            return False


    def __gt__(self, other):
        if self.__routerName > other.__routerName:
            return True
        else:
            return False


    def __lt__(self, other):
       if self.__routerName < other.__routerName:
           return True
       else:
           return False


def get_router_from_router_list(routerName, routerList):
    """This function takes router's objects name attributes value and list
    of router object.
      :return:router object which mathches the router name attribute and if no
     matches are found then null reurned
    """
    temporaryRouter = Router(routerName)
    if temporaryRouter in routerList:
      for item in routerList:
        if item.get_router_name() == routerName:
            return item
    else:
        return None


def file_opener(fileNameToOpen, routerList):
   """This function takes as input a file name and router object list.
   :return: routers object list.
    """
   try:
      infile = open(fileNameToOpen, "r")
      lines = infile.readlines()
      infile.close()
      for line in lines:
          line = line.strip("\n")
          routername,neighbour,routingTable = line.split("!")
          newRouter  = Router(routername)
          if newRouter in routerList:
              print("Name is taken.")
          else:
             routerList.append(newRouter)

          neighbourList = neighbour.split(";")
          for item in neighbourList:
              if len(item)> 0:
                    neighbourRouterObj = get_router_from_router_list(item, routerList)
                    if neighbourRouterObj is None :
                        continue
                    newRouter.add_neighbour(neighbourRouterObj)
                    neighbourRouterObj.add_neighbour(newRouter)

          routingTablelist = routingTable.split(";")
          for item in routingTablelist:
              valuesList = item.split(":")
              if len(valuesList) == 2:
                  newRouter.add_network(valuesList[0],valuesList[1])

   except IOError:
                print("Error: the file could not be read or "
                      "there is something wrong with it.")
                return -1

   except ValueError :
                print("Error: the file could not be read "
                      "or there is something wrong with it.")
                return -1

   return routerList

def help_text():
    print("Erroneous command!")
    print("Enter one of these commands:")
    print("NR (new router)")
    print("P (print)")
    print("C (connect)")
    print("NN (new network)")
    print("PA (print all)")
    print("S (send routing tables)")
    print("RR (route request)")
    print("Q (quit)")

def main():
    routerFile = input("Network file: ")
    routerList = []
    if routerFile != "":
       routerList = file_opener(routerFile,routerList)
       if routerList == -1:
           return

    while True:
        command = input("> ")
        command = command.upper()

        if command == "P":
            routerName = input("Enter router name: ")
            returnedRouterObject = get_router_from_router_list(routerName,routerList)
            if returnedRouterObject is None:
                print("Router was not found.")
            else:
                returnedRouterObject.print_info()

        elif command == "PA":
            sortingRouterList = sorted(routerList)
            for item in sortingRouterList:
                item.print_info()

        elif command == "S":
           sendingRouter = input("Sending router: ")
           sendingRouterObj = get_router_from_router_list(sendingRouter,routerList)
           if sendingRouterObj is None:
               continue

           neighboursRouterObjList = sendingRouterObj.find_neighbours()
           for neighboursRouterObj in neighboursRouterObjList:
               neighboursRouterObj.receive_routing_table(sendingRouterObj)

        elif command == "C":
            firstRouter = input("Enter 1st router: ")
            secondRouter = input("Enter 2nd router: ")
            firstRouterObj = get_router_from_router_list\
                (firstRouter,routerList)
            secondRouterObj = get_router_from_router_list(secondRouter,
                                                         routerList)
            if firstRouterObj is None or secondRouterObj is None:
                continue
            firstRouterObj.add_neighbour(secondRouterObj)
            secondRouterObj.add_neighbour(firstRouterObj)

        elif command == "RR":
            connectedRouterName = input("Enter router name: ")
            networkName = input("Enter network name: ")
            connectedRouterObj = get_router_from_router_list\
                (connectedRouterName,routerList)
            if connectedRouterObj is None:
               continue
            connectedRouterObj.has_route(networkName)

        elif command == "NR":
            routerName = input("Enter a new name: ")
            newRouter  = Router(routerName)
            if newRouter in routerList:
                print("Name is taken.")
            else:
               routerList.append(newRouter)

        elif command == "NN":
             routerName = input("Enter router name: ")
             network = input("Enter network: ")
             distance = int(input("Enter distance: "))
             firstRouterObj = get_router_from_router_list(routerName,routerList)
             firstRouterObj.add_network(network,distance)

        elif command == "help":
            help_text()

        elif command == "Q":
            print("Simulator closes.")
            return

        else:
            help_text()


main()
